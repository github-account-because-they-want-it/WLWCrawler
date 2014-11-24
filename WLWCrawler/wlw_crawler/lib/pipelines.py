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
  
