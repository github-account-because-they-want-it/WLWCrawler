'''
Created on Nov 23, 2014
@author: Mohammed Hamdy
'''

class StripFaxFieldPipeline(object):
  
  def process_item(self, item, spider):
    if item.get("fax"):
      stripped_fax = item.get("fax").strip("Fax: ")
      item["fax"] = stripped_fax
    return item
  
class AddSuffixPipeline(object):
  """
  uses the private _scrapedurl item field to add the url
  suffix to item
  """
  
  def process_item(self, item, spider):
    url = item.get("_scrapedurl")
    suffix = url.split('-')[-1]
    item["suffix"] = suffix
    return item
  