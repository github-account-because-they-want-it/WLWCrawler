'''
Created on Nov 23, 2014
@author: Mohammed Hamdy
'''

class WLWURLGenerator(object):
  """
  Tells the spider about the urls to crawl. This is a singleton for easy sharing
  between the spider and client protocol
  """
  
  _instance = None
  
  @classmethod
  def getInstance(cls):
    if cls._instance is None:
      cls._instance = WLWURLGenerator()
    return cls._instance
  
  def __init__(self):
    self.base_url = "https://www.wlw.de/profile/saalefenster-dminus-ag-"
    self.available_suffixes = []
    
  def __iter__(self):
    return self
  
  def next(self):
    if len(self.available_suffixes) == 0:
      raise StopIteration
    return self.base_url + str(self.available_suffixes.pop(0))
  
  def suffixesArrived(self, newSuffixes):
    self.available_suffixes.extend(newSuffixes)
    
def wlw_url_generator():
  # this is here to avoid amending the spider to call getInstance
  # instead of the constructor
  return WLWURLGenerator.getInstance()
    
def filter_predicate(pageSource):
  return "Unfortunately we were unable to find the page you requested." not in pageSource
