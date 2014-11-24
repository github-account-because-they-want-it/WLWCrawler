'''
Created on Nov 23, 2014
@author: Mohammed Hamdy
'''

from visualscrape.lib.types import SpiderTypes

BOT_NAME = 'ScrapyCrawler'

SPIDER_MODULES = ['visualscrape.lib.scrapylib.crawlers']

NEWSPIDER_MODULE = 'NefsakLaptops.spiders'

SCRAPY_MANAGE_REACTOR = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'NefsakLaptops (+http://www.yourdomain.com)'
ITEM_PIPELINES = {"visualscrape.lib.scrapylib.pipeline.ItemPostProcessor": 1,
                  "visualscrape.lib.scrapylib.pipeline.FilterFieldsPipeline": 100,
                  "wlw_crawler.lib.pipelines.StripFaxFieldPipeline":101,
                  "visualscrape.lib.scrapylib.pipeline.PushToHandlerPipeline": 1000}

CONFIG_PATH = "D:/scraped_images/config" # this is a path used for spider configuration, like current progress
ITEM_LOADER = "visualscrape.lib.scrapylib.itemloader.DefaultItemLoader"

DOWNLOAD_FAVICON = True

USER_AGENT = "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0"

SITE_PARAMS = {"https://www.wlw.de/":
               {"REQUEST_DELAY":3, 
                "COOKIES_ENABLED": True,
                # currently, this setting is only supported on selenium, but it might be the default on Scrapy, which seems logical
                "IMAGES_ENABLED" : False, 
                "PREFERRED_SCRAPER": "visualscrape.lib.scrapylib.crawlers.ScrapyPageListCrawler",
                "URL_GENERATOR":"wlw_crawler.lib.support.wlw_url_generator",
                "FILTER_PREDICATE":"wlw_crawler.lib.support.filter_predicate"
               }
              }
