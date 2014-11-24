'''
Created on Nov 23, 2014
@author: Mohammed Hamdy
'''

'''
Created on Oct 28, 2014
@author: Mohammed Hamdy
'''
import os
# this must be set here, before the settings module is imported or it can be set 
# in the environment variable (which doesn't work on startup)
os.environ["SCRAPY_SETTINGS_MODULE"] = "wlw_crawler.settings"
from threading import Timer
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import logging
from wlw_crawler.protocol.common import ClientToServerSignals, ServerToClientSignals, SERVER_PORT
from wlw_crawler.lib.loggers import logFromClient
from visualscrape.engine import CrawlEngine
from visualscrape.lib.path import MainPage, URL, SpiderPath
from visualscrape.lib.signal import SpiderClosed
from wlw_crawler.lib.selectors import wlw_selector
from wlw_crawler.lib.support import wlw_url_generator

class WLWClientProtocol(LineReceiver):
  
  def connectionMade(self):
    # identify myself to server
    logFromClient("connected to server", logging.INFO)
    self.sendLine(ClientToServerSignals.hello())
    self.sendLine(ClientToServerSignals.makeReadyMessage())
    
  def lineReceived(self, line):
    if ServerToClientSignals.isRangeMessage(line):
      crawl_url_suffixes = ServerToClientSignals.suffixesFromMessage(line)
      logFromClient("suffixes ({} : {}) arrived from server".format(crawl_url_suffixes[0], crawl_url_suffixes[-1]),
                    logging.INFO)
      self.factory.suffixesArrived(crawl_url_suffixes)
      logFromClient("finished crawling job. requesting more...", logging.INFO)
      self.sendLine(ClientToServerSignals.makeReadyMessage())
      
    elif ServerToClientSignals.isShutdownMessage(line):
      logFromClient("got shutdown message from server. bye!", 
                    logging.INFO, self._name)
      self.transport.loseConnection()
      reactor.stop()
      
  def itemReceived(self, item):
    item_message = ClientToServerSignals.messageFromItem(item)
    self.sendLine(item_message)

class WLWClientProtocolFactory(ReconnectingClientFactory):
  
  def __init__(self, maxDelay=60):
    self.maxDelay = maxDelay
    self.data_queue = None
    self.event_queue = None
    # only one client connection is used
    self.url_generator = wlw_url_generator()
    self.client = None
    self.timer = Timer(30, self.check_queues)
    self.timer.start()
    logFromClient("client started", logging.INFO)
    
  def buildProtocol(self, addr):
    # http://twistedmatrix.com/trac/browser/tags/releases/twisted-14.0.2/twisted/internet/protocol.py#L320
    self.resetDelay()
    self.client = WLWClientProtocol()
    self.client.factory = self
    return self.client
  
  def set_event_queue(self, queue):
    self.event_queue = queue
    
  def set_data_queue(self, queue):
    self.data_queue = queue
    
  def check_queues(self):
    # check new spider items arrived and pass them to client which
    # should pass them to server
    finished = False
    # the queues are not assigned before the spider is initialized, which sometimes take a long time
    if not self.event_queue or not self.data_queue: return
    while not self.event_queue.empty():
      event = self.event_queue.get(block=False, timeout=0)
      if isinstance(event, SpiderClosed):
        finished = True
    while not self.data_queue.empty():
      new_item = self.data_queue.get(block=False, timeout=0)
      self.client.itemReceived(new_item)
    if not finished: Timer(1, self.check_queues).start()
    
  def suffixesArrived(self, urlSuffixes):
    self.url_generator.suffixesArrived(urlSuffixes)
    # empty queues before invalidating them in the new spider
    self.check_queues()
    wlw_path = SpiderPath()
    wlw_path.add_step(URL("https://www.wlw.de"))
    main_page = MainPage(itemSelector=wlw_selector)
    wlw_path.add_step(main_page)
    engine = CrawlEngine()
    engine.add_spider("WLWCrawler").set_path(wlw_path).register_handler(self).start()

def main(serverAddress):
  factory = WLWClientProtocolFactory()
  reactor.connectTCP(serverAddress, SERVER_PORT, factory)
  reactor.run()

if __name__ == "__main__":
  from argparse import ArgumentParser
  # let caller pass client name on commandline
  parser = ArgumentParser(description="whois client arguments")
  parser.add_argument("-a", "--address", default="127.0.0.1",
                      help="The server IP to which to connect")
  parsed_args = parser.parse_args()
  main(parsed_args.address)
  