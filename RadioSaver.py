import requests
import time

# stream_url = 'http://195.150.20.245/rmf_fm'

url = input("url do radia: ")
hours = float(input("czas w h: "))
seconds = hours * 60 * 60
r = requests.get(url, stream=True)
start = time.time()

with open('stream.mp3', 'wb') as f:
    for block in r.iter_content(1024):
        f.write(block)
        if time.time() - start > seconds:
            break