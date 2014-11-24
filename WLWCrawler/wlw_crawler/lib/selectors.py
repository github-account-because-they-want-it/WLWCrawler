'''
Created on Nov 18, 2014
@author: Mohammed Hamdy
'''

from visualscrape.lib.selector import ItemSelector, FieldSelector, KeyValueSelector

wlw_selector = ItemSelector([
                  KeyValueSelector("phone", FieldSelector("ul.profile-company-contact li:nth-child(1) a::text", FieldSelector.CSS)),
                  KeyValueSelector("website", FieldSelector("ul.profile-company-contact li:nth-child(3) a::text", FieldSelector.CSS)),
                  KeyValueSelector("company", FieldSelector("h1.profile-company-name::text", FieldSelector.CSS)),
                  KeyValueSelector("email", FieldSelector("ul.profile-company-contact li:nth-child(2) a::text", FieldSelector.CSS)),
                  KeyValueSelector("address", FieldSelector("div.profile-company-address::text", FieldSelector.CSS)),
                  KeyValueSelector("fax", FieldSelector("//div[starts-with(., 'Fax')]/text()", FieldSelector.XPATH)),
                  ])

