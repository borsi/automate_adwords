import configparser
import urllib.request
import time
import datetime
import csv
import sys

## config file init
Config = configparser.ConfigParser()
Config.read("config.ini")

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
    
