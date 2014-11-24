'''
Created on Oct 24, 2014
@author: Mohammed Hamdy
'''

import psycopg2 as dbconnector, os.path as path
import  ConfigParser
from wlw_crawler.protocol.common import MIN_SUFFIX, MAX_SUFFIX

class DatabaseConnection(object):
  """
  Prepares database credentials and makes a valid database cursor to clients.
  Assumes database and tables are properly setup.
  """
  
  def __init__(self, databaseName="wlw"):
    self._db_username = ''
    self._db_password = ''
    self._db_connection = None
    db_cfg_path = path.join(path.dirname(__file__), "dbconfig.ini")
    self._readExistingCredentials(db_cfg_path)
    self._db_connection = dbconnector.connect("dbname={} user={} password={} host=localhost"\
                                   .format(databaseName, self._db_username, self._db_password))
    
  def getCursor(self, **kwargs):
    return self._db_connection.cursor(**kwargs)
  
  def commit(self):
    self._db_connection.commit()
    
  def rollback(self):
    self._db_connection.rollback()
    
  def _readExistingCredentials(self, credsFile):
    with open(credsFile, 'r') as db_cfg_file:
      parser = ConfigParser.ConfigParser()
      parser.readfp(db_cfg_file)
      self._db_username = parser.get("Credentials", "username")
      self._db_password = parser.get("Credentials", "password")
      

def suffixLimitsChanged(cursor):
  cursor.execute("SELECT MIN(suffix), MAX(suffix) FROM suffix")
  mn, mx = cursor.fetchone()
  return mn != MIN_SUFFIX or mx != MAX_SUFFIX
  
def initializeWLWTables():
  con = DatabaseConnection()
  cursor = con.getCursor()
  cursor.execute("DELETE FROM suffix WHERE TRUE")
  cursor.execute("DELETE FROM wlw WHERE TRUE")
  for i in range(MIN_SUFFIX, MAX_SUFFIX + 1):
    cursor.execute("INSERT INTO suffix (suffix, crawled) VALUES (%s, %s)", (i, False))
  con.commit()

if __name__ == "__main__":
  initializeWLWTables()
  