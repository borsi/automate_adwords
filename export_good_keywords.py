#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import urllib.request
import time
import datetime
import csv
import sys, io, codecs
import sqlite3

conn = sqlite3.connect('products.db')

c = conn.cursor()

# for the adwords custom class
from collections import OrderedDict

## config file init
Config = configparser.ConfigParser()
Config.read("config.ini")

## class for adwords type output
class AdwordsContainer:
    row = OrderedDict()
    def __init__(self, opt):
        if not opt:
            self.row = OrderedDict([
                (u'Campaign',u'Search - Top termékek'),
                (u'Campaign daily budget', u'10000'),
                (u'Networks',u'Google Search; Search Partners'),
                (u'Languages' , u'hu'), 
                (u'ID' , u''), 
                (u'Location' , u''), 
                (u'Ad Group' , u''), 
                (u'Max CPC' , u''), 
                (u'Display Network Max CPC' , u''),
                (u'Max CPM' , u''), 
                (u'CPA Bid' , u''), 
                (u'Display Network' , u''), 
                (u'Custom Bid Type' , u''),
                (u'Ad Group Type' , u''),
                (u'Flexible Reach' , u''),
                (u'Keyword' , u''),
                (u'Criterion Type' , u''),
                (u'First Page CPC1' , u''),
                (u'Top Of Page CPC' , u''),
                (u'Quality Score' , u''),
                (u'Bid Strategy Type' , u'Manual CPC'),
                (u'Bid Strategy Name' , u''),
                (u'Enhanced CPC' , u'Disabled'),
                (u'Viewable CPM' , u'Disabled'),
                (u'Bid Adjustment' , u''),
                (u'Headline' , u''),
                (u'Description Line 1' , u''),
                (u'Description Line 2' , u''),
                (u'Display URL' , u''),	
                (u'Destination URL' , ''),
                (u'Device Preference' , u''),
                (u'Start Date' , u''),
                (u'End Date' , ''),
                (u'Ad Schedule' , u'(Monday@100%[00:00-24:00]);(Tuesday@100%[00:00-24:00]);(Wednesday@100%[00:00-24:00]);(Thursday@100%[00:00-24:00]);(Friday@100%[00:00-24:00]);(Saturday@100%[00:00-24:00]);(Sunday@100%[00:00-24:00])'),
                (u'Campaign Status' , u'Active'),
                (u'AdGroup Status' , u''),
                (u'Status' , u''),
                (u'Approval Status' , u''),
                (u'Suggested Changes' , u''),
                (u'Comment' , u'')])
        else:
            self.row = OrderedDict([
                (u'Campaign',u'Search - Top termékek'),
                (u'Campaign daily budget', u''),
                (u'Networks',u'Google Search; Search Partners'),
                (u'Languages' , u''), 
                (u'ID' , u''), 
                (u'Location' , u''), 
                (u'Ad Group' , u''), 
                (u'Max CPC' , u''), 
                (u'Display Network Max CPC' , u''),
                (u'Max CPM' , u''), 
                (u'CPA Bid' , u''), 
                (u'Display Network' , u''), 
                (u'Custom Bid Type' , u''),
                (u'Ad Group Type' , u''),
                (u'Flexible Reach' , u''),
                (u'Keyword' , u''),
                (u'Criterion Type' , u''),
                (u'First Page CPC1' , u''),
                (u'Top Of Page CPC' , u''),
                (u'Quality Score' , u''),
                (u'Bid Strategy Type' , u''),
                (u'Bid Strategy Name' , u''),
                (u'Enhanced CPC' , u''),
                (u'Viewable CPM' , u''),
                (u'Bid Adjustment' , u''),
                (u'Headline' , u''),
                (u'Description Line 1' , u''),
                (u'Description Line 2' , u''),
                (u'Display URL' , u''),	
                (u'Destination URL' , ''),
                (u'Device Preference' , u''),
                (u'Start Date' , u''),
                (u'End Date' , ''),
                (u'Ad Schedule' , u''),
                (u'Campaign Status' , u'Active'),
                (u'AdGroup Status' , u''),
                (u'Status' , u''),
                (u'Approval Status' , u''),
                (u'Suggested Changes' , u''),
                (u'Comment' , u'')])

    def __getitem__(self, key):
        return self.row[key]

    def get(self, key, restval):
        return self.row[key]
    
    def __setitem__(self, key, value):
        self.row[key] = value

    def keys(self):
        return self.row.keys()

    def values(self):
        return self.row.values()

    def items(self):
        return self.row.items()


## reading and handling config file data
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

## Let's open the dowloaded csv file - right now we don't store historic data
#
#print(name.encode('utf-8'))
# initializing the csv stuff
output = "fixed_keywords"+datetime.date.today().strftime("%Y%m%d")+".csv"
csvf = open(output, 'w')
#googlewriter = UnicodeWriter(csvf)
# first row of header
header = AdwordsContainer(0)
# second row of header 
## diffs
header2 = AdwordsContainer(1)
# the product data in the adwords csv consist of
# three rows for whatever reason. this is the first row.
product1 = AdwordsContainer(1)
# second product row    
product2 = AdwordsContainer(1)
# third product row - the last one
# when writing in the rows, one needs to change
# the respective attributes
product3 = AdwordsContainer(1)
# Init csv headersj

googlewriter = csv.DictWriter(csvf, header.keys(), extrasaction='ignore', delimiter="\t")
print (header.items())
googlewriter.writeheader()
googlewriter.writerow(header)
googlewriter.writerow(header2)

count = 0

#    spamreader = csv.reader(csvfile, delimiter='|', quotechar='"')
# we have to change the input from csv file
# to the database
for row in conn.execute("SELECT * FROM Products WHERE isfixed"):
    productid = row[0]
    name = row[1]
    price = row[5]
    url = row[3]
    descline1 = name


    price = int(price)
    formattedprice = format(price, ',d').replace(',','.') + " Ft."

    product1["Ad Group"] = name
    product2["Ad Group"] = name
    product3["Ad Group"] = name

    product2["Headline"] = name

    product2["Description Line 1"] = descline1 + " " + formattedprice
# más legyen a szöveg, ha ingyen szállítunk és ha nem
    if(price) > 15000:
        product2["Description Line 2"] = u'Minőségi új termék,Ingyen szállítás'
    else:
        product2["Description Line 2"] = u'Minőségi új termék, kedvező áron'

    product3["Criterion Type"] = u'Exact'
    product3["Max CPC"] = u'25'
    product2["Max CPC"] = u'25'
    product3["Keyword"] = row[2]
    # after this we need to do some magic. the second rows' 
    # "Display URL" attribute should have a format that looks 
    # something like this: ClickShop.hu/Product-clickshop-name-with-dashes
    if len(name) > 22:
        name = name.replace(w[len(w)-2], "")
        if len(name) > 22:
            name = name.replace(w[len(w)-3], "")
            if len(name) > 22:
                name = name.replace(w[len(w)-4], "")
                if len(name) > 22:
                    name = name.replace(w[len(w)-1], "")
        dashed_name = name
        dashed_name = dashed_name.replace(" ", "-")
        if len(dashed_name) > 22:
            dashed_name[:-1]
    elif len(name) <= 22:
        dashed_name = name.replace(" ", "-")
        if len(dashed_name) > 22:
            dashed_name[:-1]
    else:
        dashed_name = name.replace(" ", "-")
        if len(dashed_name) > 22:
            dashed_name[:-1]

    product2["Display URL"] = "ClickShop.hu/" + dashed_name
    product2["Destination URL"] = url

    #googlewriter.writerow(product1)
    googlewriter.writerow(product2)
    googlewriter.writerow(product3)


csvf.close()
conn.close()

