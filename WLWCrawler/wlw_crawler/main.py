'''
Created on Nov 23, 2014
@author: Mohammed Hamdy
'''

import os
# this must be set here, before the settings module is imported or in the env var
os.environ["SCRAPY_SETTINGS_MODULE"] = "wlw_crawler.settings"
from visualscrape.engine import CrawlEngine
from visualscrape.test.test_handler import PrintingHandler
from visualscrape.lib.path import MainPage, URL, SpiderPath
from wlw_crawler.lib.selectors import wlw_selector


def client_main():
  wlw_path = SpiderPath()
  wlw_path.add_step(URL("https://www.wlw.de"))
  main_page = MainPage(itemSelector=wlw_selector)
  wlw_path.add_step(main_page)
  engine = CrawlEngine()
  engine.add_spider("WLWCrawler").set_path(wlw_path).register_handler(PrintingHandler()).start()
  
if __name__ == "__main__":
  client_main()