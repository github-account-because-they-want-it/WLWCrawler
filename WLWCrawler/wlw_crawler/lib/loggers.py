'''
Created on Nov 23, 2014
@author: Mohammed Hamdy
'''

import logging
from logging.handlers import TimedRotatingFileHandler
import os.path as path, os

log_dir = path.join(path.dirname(path.dirname(__file__)), "logs")

if not path.exists(log_dir):
  os.mkdir(log_dir)

client_logger = logging.getLogger(name="Client")
client_logger.setLevel(logging.DEBUG)
log_file_path = path.join(log_dir, "client_log.log")
client_handler = TimedRotatingFileHandler(log_file_path,
                    when='H', interval=24, backupCount=2)
client_format = logging.Formatter('%(levelname)s @ [%(asctime)s] :: %(message)s',
                                   datefmt="%Y-%m-%d %H:%M:%S")

client_handler.setFormatter(client_format)
client_logger.addHandler(client_handler)

def logFromClient(message, level):
  client_logger.log(level, message)

# ---------------- server logger ------------------ #

server_logger = logging.getLogger(name="Server")
server_logger.setLevel(logging.DEBUG)
log_file_path = path.join(log_dir, "server_log.log")
server_handler = TimedRotatingFileHandler(log_file_path,
                    when='H', interval=24, backupCount=2)
server_format = logging.Formatter('%(levelname)s @ [%(asctime)s] :: %(message)s',
                                   datefmt="%Y-%m-%d %H:%M:%S")

server_handler.setFormatter(server_format)
server_logger.addHandler(server_handler)

def logFromServer(message, level):
  server_logger.log(level, message)