#!/usr/bin/bash

# usage : wlw_setup.sh [client|server] server_address

machine_type=$1

if [ machine_type=client ]; then
  echo "Add the wlw_crawler and VisualScrape project directories to sys.path in twistd.py"
  echo "Also add the plugin directory to sys.path in the same file"
  echo "Add the SCRAPY_SETTINGS_MODULE environment variable to the same file"
fi
