'''
Created on Nov 23, 2014
@author: Mohammed Hamdy
'''

from twisted.internet.protocol import Factory
from twisted.protocols import basic
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
import logging
import psycopg2 as dbconnector
from wlw_crawler.protocol.common import ClientToServerSignals, ServerToClientSignals, SERVER_PORT
from wlw_crawler.database.connection import DatabaseConnection, initializeWLWTables, \
  suffixLimitsChanged
from wlw_crawler.lib.loggers import logFromServer

class WLWServerProtocol(basic.LineReceiver):
  
  def lineReceived(self, line):
    if ClientToServerSignals.isHelloMessage(line):
      self.factory.addClient(self)
    elif ClientToServerSignals.isReadyMessage(line):
      self.factory.setClientReady(self)
    elif ClientToServerSignals.isItemMessage(line): # client sent a new parsed record
      self.factory.gotItem(line, self)
      
  def connectionMade(self):
    basic.LineReceiver.connectionMade(self)
    self.client_address = self.transport.getPeer().host
    self.identifier = self.client_address
      
  def connectionLost(self, reason):
    self.factory.removeClient(self)
  

class WLWServerProtocolFactory(Factory):
  
  protocol = WLWServerProtocol
  
  def __init__(self):
    self._client_infos = []
    self._db_connection = DatabaseConnection()
    self._suffix_generator = self._suffixRange()
    logFromServer("server started", logging.INFO)
    self._initializeCrawling()
    
  def _initializeCrawling(self):
    cursor = self._db_connection.getCursor()
    if suffixLimitsChanged(cursor):
      logFromServer("suffix range changed. reinitializing tables. please wait...",
                    logging.INFO)
      initializeWLWTables()
      logFromServer("reinitialization finished", logging.INFO)
    else:
      cursor.execute("SELECT COUNT(*) FROM suffix")
      total_row_count = cursor.fetchone()[0]
      cursor.execute("SELECT COUNT(*) FROM suffix WHERE crawled=false")
      non_crawled_count = cursor.fetchone()[0]
      if non_crawled_count == 0:
        logFromServer("crawling finished last time. starting fresh", logging.INFO)
        logFromServer("reinitializing tables. please wait...",
                    logging.INFO)
        initializeWLWTables()
        logFromServer("reinitialization finished", logging.INFO)
      elif non_crawled_count < total_row_count:
        logFromServer("resuming crawling on {} suffixes".format(non_crawled_count),
                      logging.INFO)
    
  def addClient(self, connection):
    new_client_info = {"connection":connection, "identifier":connection.identifier,
                        "returned_item_messages":[], "assigned_suffixes":[]}
    self._client_infos.append(new_client_info)
    logFromServer("client '{}' has been registered. current client count is {}"\
                  .format(new_client_info["identifier"], len(self._client_infos)), 
                  logging.INFO)
    
  def removeClient(self, connection):
    client_info = self._getClientInfoByConnection(connection)
    self._client_infos.remove(client_info)
    logFromServer("client '{}' has disconnected. current client count is {}"\
                  .format(client_info["identifier"], len(self._client_infos)), logging.WARN)
    if len(self._client_infos) == 0: # all clients shutdown
      logFromServer("server is shutting down. bye!", logging.INFO)
      reactor.stop() # shutdown server too
    
  def setClientReady(self, connection):
    """
    called when a client has sent a ready signal
    if a client is ready and we have more ranges, we send it one
    if we don't have more ranges for the client, we tell it to shutdown
    """
    client_info = self._getClientInfoByConnection(connection)
    self._insertClientRecords(client_info)
    logFromServer("client '{}' is now ready".format(client_info["identifier"]),
                  logging.INFO)
    try:
      next_suffix_batch = next(self._suffix_generator)
    except StopIteration:
      # all IPs consumed
      logFromServer("crawling finished. shutting down client '{}'".\
                    format(client_info["identifier"]), logging.INFO)
      client_info["connection"].sendLine(ServerToClientSignals.makeShutdownMessage())
      logFromServer("shutdown signal sent to '{}'".format(client_info["identifier"])
                  , logging.INFO)
    else:
      client_info["assigned_suffixes"] = next_suffix_batch
      client_info["connection"].sendLine(ServerToClientSignals.\
                                       makeRangeMessage(next_suffix_batch))
      logFromServer("range {} : {} sent to {}"\
                    .format(next_suffix_batch[0],
                     next_suffix_batch[-1], client_info["identifier"]), logging.INFO)
  
  def gotItem(self, itemLine, connection):
    client_info = self._getClientInfoByConnection(connection)
    client_info["returned_item_messages"].append(itemLine)
    
  def _suffixRange(self):
    batch_size = 10
    cursor = self._db_connection.getCursor()
    cursor.execute("SELECT suffix FROM suffix WHERE crawled=FALSE")
    non_crawled_count = cursor.rowcount 
    while non_crawled_count > 0:
      suffix_tuples = cursor.fetchmany(size=batch_size)
      if len(suffix_tuples) < batch_size:
        # cursor exhausted. search more non-crawled suffixes
        cursor.execute("SELECT suffix FROM suffix WHERE crawled=FALSE")
        non_crawled_count = cursor.rowcount
      if len(suffix_tuples) != 0: # like when suffixes exhausted
        suffixes = [str(st[0]) for st in suffix_tuples]
        yield suffixes
        
  def _insertClientRecords(self, clientInfo):
    cursor = self._db_connection.getCursor()
    insert_query = "INSERT INTO wlw (company, address, email, fax, phone, website" +\
        " VALUES (%(company)s, %(address)s, %(email)s, %(fax)s, %(phone)s, " +\
        " %(website)s);"
    returned_record_count = len(clientInfo["returned_item_messages"])
    logFromServer("{} records returned from client '{}' [{} suffixes were sent]. committing them..."\
                  .format(returned_record_count, clientInfo["identifier"],
                  len(clientInfo["assigned_suffixes"])), logging.INFO)
    try:
      for record_line in clientInfo["returned_item_messages"]:
        new_record = ClientToServerSignals.itemFromMessage(record_line)
        cursor.execute(insert_query, new_record)
    except dbconnector.DataError as de:
        logFromServer("Couldn't insert new record into database due to {}"\
                      .format(str(de)), logging.ERROR)
        self._db_connection.rollback()
    else:
      assigned_suffixes = clientInfo.get("assigned_suffixes")
      if assigned_suffixes: # clients don't always have suffixes, like when starting up
        for suffix in assigned_suffixes:
          cursor.execute("UPDATE suffix SET crawled=TRUE WHERE suffix=%s", (suffix,))
        self._db_connection.commit()

  def _getClientInfoByConnection(self, connection):
    for client_info in self._client_infos:
      if client_info["identifier"] == connection.identifier:
        return client_info
    return {}


def main(factoryInstance):
  endpoint = TCP4ServerEndpoint(reactor, SERVER_PORT)
  endpoint.listen(factoryInstance)
  reactor.run()

if __name__ == "__main__":
  main(WLWServerProtocolFactory())
