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
#print(name.encode('utf-8'))
# initializing the csv stuff
output = "test.csv"
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

with open(filename, newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='|', quotechar='"')
    try:
        for row in spamreader:
            dashed_name = ''
            if row[1] != "Termeknev":
                productid = row[0]
                name = row[1]
                price = row[3]
                imagelink = row[4]
                url = row[5]
                url = url.replace("?ref=argep", '') 
                descline1 = name


                price = int(price)
                formattedprice = format(price, ',d').replace(',','.') + " Ft."

                product1["Ad Group"] = name
                product2["Ad Group"] = name
                product3["Ad Group"] = name

                # we reduce the size of the full name so that it fits within adwords criteria
                ## adgroup can be as long as we need it
                # if the length of the name is more than 25 characters, we split it
                # and use the second, first, third and last word of the original name



# todo: descline1 túl hosszú bizonyos esetekben [x]
# csökkenteni mindig az utolsó előtti szavakkal [x]
# valamint max cpc másik sorba is kell (mindbe) [x]
# csekkolni, hogy mindenhol jól építjük-e fel a nevet meg a descline1-et

                w = name.split()
                w2 = w
                desclinelist = []
                counter = 1
                while len(name) >= 25:
                    desclinelist.insert(0,w2[-1])
                    del w2[-1]
                    name = " ".join(w2)
                    counter = counter + 1
                descline1 = " ".join(desclinelist)
#                if len(name) > 25:
#                    if len(w) > 3:
#                        name = w[0] + " " + w[1] + " " + w[2] + " " + w[len(w)-1]
#                        descline1 = ""
#                        for word in range(3, len(w)-2):
#                            descline1 += w[word] + " "
#                    elif len(w) == 3:
#                        name = w[0] + " " + w[1]
#                        descline1 = w[2]
#                    elif len(w) == 2:
#                        name = w[0] 
#                        descline1 = w[1]
##                    else:
##                        name = w[0] + " " + w[1]
#                    if len(name) > 25:
#                        descline1 += w[len(w)-1]
#                        if len(w) == 3:
#                            name = w[0] + " " + w[1] + " " + w[2]
#                        elif len(w) == 2:
#                            name = w[0] + " " + w[1]
#                        else:
#                            name = w[0]
#                        if len(name) > 25:
#                            if len(w) == 2:
#                                name = w[0] + " " + w[1]
#                            else:
#                                name = w[0] + " " + w[2]  

                
                product2["Headline"] = name

                splitteddesc = descline1.split()
                # ha nem férünk bele a korlátba, kigórjuk az utolsó előtti szót.
                if len(descline1) + len(formattedprice) > 34:
                    descline1 = descline1.replace(splitteddesc[len(splitteddesc)-2], " ")
                    # ha még mindig nem, akkor még egyet kiszedünk
                    if len(descline1) + len(formattedprice) > 34:
                        descline1 = descline1.replace(splitteddesc[len(splitteddesc)-3], "")
                        # ha még mindig nem, akkor még egyet kiszedünk
                        if len(descline1) + len(formattedprice) > 34:
                            descline1 = descline1.replace(splitteddesc[len(splitteddesc)-4], "")
                            # ha még mindig nem, akkor még egyet kiszedünk
                            if len(descline1) + len(formattedprice) > 34:
                                descline1 = descline1.replace(splitteddesc[len(splitteddesc)-1], "")
                                # ha még mindig nem, akkor még egyet kiszedünk
                                if len(descline1) + len(formattedprice) > 34:
                                    descline1 = descline1.replace(splitteddesc[len(splitteddesc)-5], "")

                product2["Description Line 1"] = descline1 + " " + formattedprice
# más legyen a szöveg, ha ingyen szállítunk és ha nem
                if(price) > 15000:
                    product2["Description Line 2"] = u'Minőségi új termék,Ingyen szállítás'
                else:
                    product2["Description Line 2"] = u'Minőségi új termék, kedvező áron'
                product3["Criterion Type"] = u'Exact'
                product3["Max CPC"] = u'25'
                product2["Max CPC"] = u'25'
                product3["Keyword"] = " ".join(w)
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
                count += 1
                if count > 10000:
                    print(count.__str__() + " " + name + " " + productid + " " + price.__str__() + " " + imagelink) 
                    break

                print(count.__str__())# + " " + name + " " + productid + " " + price + " " + imagelink) 

    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))


csvf.close()


