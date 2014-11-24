'''
Created on Nov 9, 2014
@author: Mohammed Hamdy
usage : twistd whoisclient --address <server_address>
'''
from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet

from wlw_crawler.protocol.wlw_client import WLWClientProtocolFactory
from wlw_crawler.protocol.common import SERVER_PORT

class Options(usage.Options):
    optParameters = [["address", 'a', "127.0.0.1", 
                      "The server address to which the client will connect"]]


class ClientServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "wlwclient"
    description = "A client to crawl wlw pages"
    options = Options

    def makeService(self, options):
        return internet.TCPClient(options["address"], SERVER_PORT, 
                                  WLWClientProtocolFactory())

service_maker = ClientServiceMaker()
