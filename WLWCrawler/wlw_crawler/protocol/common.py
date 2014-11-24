'''
Created on Nov 23, 2014
@author: Mohammed Hamdy
'''

SERVER_PORT = 8642
MIN_SUFFIX = 0
MAX_SUFFIX = 2 * 1747486

class ClientToServerSignals(object):
  
  field_names = ["address", "company", "email", "fax", "phone", "website"]
  
  @classmethod
  def hello(cls):
    return "Hello!"
  
  @classmethod
  def isHelloMessage(cls, message):
    return message == "Hello!"
  
  @classmethod
  def messageFromItem(cls, item):
    message = 'Item:'
    for field_name in cls.field_names:
      message = message + item.get(field_name, '') + ','
    message = message.strip(',')
    return message
  
  @classmethod
  def itemFromMessage(cls, message):
    message = message[5:]
    item = dict(zip(cls.field_names, message.split(',')))
    return item
  
  @classmethod
  def isItemMessage(cls, message):
    return message.startswith("Item:")
  
  @classmethod
  def makeReadyMessage(cls):
    return "Ready".format()
  
  @classmethod
  def isReadyMessage(cls, message):
    return message.endswith("Ready")


class ServerToClientSignals(object):
  
  @classmethod
  def makeRangeMessage(cls, suffixRange):
    return "Take Range:" + ','.join(suffixRange)
  
  @classmethod
  def isRangeMessage(cls, message):
    return message.startswith("Take Range:")
  
  @classmethod
  def suffixesFromMessage(cls, message):
    suffix_str = message.split("Take Range:")[1]
    return suffix_str.split(',')
  
  @classmethod
  def makeShutdownMessage(cls):
    return "Shutdown"
  
  @classmethod
  def isShutdownMessage(cls, message):
    return message == "Shutdown"
