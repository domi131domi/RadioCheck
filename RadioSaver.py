import requests
import time
import config
from datetime import datetime
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--url', action="store", dest='url', default=None)
parser.add_argument('--time', action="store", dest='time', default=None)
parser.add_argument('--outFile', action="store", dest='outFile', default=None)
args = parser.parse_args()

#stream_url = 'http://195.150.20.245/rmf_fm'

if args.url is None:
    url = input("url do radia: ")
else:
    url = str(args.url)
if args.time is None:
    hours = float(input("czas w h: "))
else:
    hours = float(args.time)
if args.outFile is None:
    name = input("Nazwa pliku wyjściowego: ")
else:
    name = str(args.outFile)

seconds = hours * 60 * 60
r = requests.get(url, stream=True)
start = datetime.utcnow()

with open(name, 'wb') as f:
    for block in r.iter_content(1024):
        f.write(block)
        now = datetime.utcnow()
        if (now - start).seconds > seconds:
            break

os.rename(name, name+'_'+start.strftime("%Y_%m_%d_%H_%M_%S")+'_'+now.strftime("%Y_%m_%d_%H_%M_%S")+'.mp3')
