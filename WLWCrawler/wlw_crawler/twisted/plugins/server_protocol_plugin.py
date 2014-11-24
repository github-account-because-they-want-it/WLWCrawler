'''
Created on Nov 9, 2014
@author: Mohammed Hamdy
usage : twistd whoisserver
'''
"""
The server didn't have to be a plugin since it doesn't need commandline
options but it's more straightforward to run and avoids the esoteric .tac
files.
"""
from zope.interface import implements
from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet

from wlw_crawler.protocol.wlw_server import WLWServerProtocolFactory
from wlw_crawler.protocol.common import SERVER_PORT

class ServerOptions(usage.Options):
  optParameters = []
  
class ServerServiceMaker(object):
  implements(IPlugin, IServiceMaker)
  
  tapname = "wlwserver"
  description = "wlw server manages the clients and assigns them pieces of work"
  options = ServerOptions
  
  def makeService(self, options):
    return internet.TCPServer(SERVER_PORT, WLWServerProtocolFactory())
  
service_maker = ServerServiceMaker()