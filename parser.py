#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import urllib.request
import time
import datetime
import csv
import sys, io, codecs

# for the adwords custom class
from collections import OrderedDict

## config file init
Config = configparser.ConfigParser()
Config.read("config.ini")

# dictwriter for utf8 output
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel_tab, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = io.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        #data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

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

## function for progress bar
def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration+0.0001))
    percent = min(int(count * block_size * 100 / total_size),100)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()

## calculate last time downloaded
timelastdownloaded = datetime.datetime.strptime(ConfigSectionMap("ConfigRoutes")['lastparsed'], '%Y.%m.%d').date()
filename = ConfigSectionMap("ConfigRoutes")['filename']
url = ConfigSectionMap("ConfigRoutes")['url']
print("we need the file from: "+url)
print("date of last update: "+timelastdownloaded.__str__())

print(datetime.date.today().strftime("%Y.%m.%d"))

## if file is older than one day, download it - otherwise we can spare the bandwith
if (timelastdownloaded < datetime.date.today()):
    print("File too old, retrieving new version")
    response = urllib.request.urlretrieve(url, 'argep.csv', reporthook)
    cgifile = open("config.ini", 'w')
    Config.set('ConfigRoutes', 'lastparsed', datetime.date.today().strftime("%Y.%m.%d")) 
    Config.write(cgifile) 
    cgifile.close()
else:
    print("File's okay we can use the current one")
    
## Let's open the dowloaded csv file - right now we don't store historic data
#
with open(filename, newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='|', quotechar='"')
    try:
        for row in spamreader:
            productid = row[0]
            name = row[1]
            price = row[3]
            imagelink = row[4]
            url = row[5]
            print(name.encode('utf-8'))
            
            # initializing the csv stuff
            output = "test.csv"
            with open(output, 'wb') as csvf:
                googlewriter = UnicodeWriter(csvf)

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
                print (header.items())
                googlewriter.writerow(header.keys())
                googlewriter.writerow(header.values())
                googlewriter.writerow(header2.values())
                
                product1["Ad Group"] = name
                product1["Max CPC"] = u'25'
                product2["Ad Group"] = name.string
                product2["Headline"] = name.string
                product2["Description Line 1"] = u'Kedvezmények és Ingyenes Szállítás.'
                product2["Description Line 2"] = u'Vásároljon jó áron a ClickShopban!'
                product3["Ad Group"] = name.string
                product3["Criterion Type"] = u'Phrase'
                # after this we need to do some magic. the second rows' 
                # "Display URL" attribute should have a format that looks 
                # something like this: ClickShop.hu/Product-clickshop-name-with-dashes
                dashed_name = name.string.replace(" ", "-")
                product2["Display URL"] = "ClickShop.hu/" + dashed_name
                product2["Destination URL"] = url

                googlewriter.writerow(product1.values())
                googlewriter.writerow(product2.values())
                googlewriter.writerow(product3.values())
                
 

    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))



