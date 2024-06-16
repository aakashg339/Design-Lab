import os
from urllib.request import Request, urlopen
req = Request('https://en.wikipedia.org/wiki/2023%E2%80%932025_ICC_World_Test_Championship',headers ={'User-Agent':'Mozilla/5.0'})
webpage = urlopen(req).read()
mydata = webpage.decode("utf8")
try:
    f=open('webpage.html','w',encoding="utf-8")
    f.write(mydata)
    f.close
except:
    print("Not able to write to file webpage.html")