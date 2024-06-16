import os
from urllib.request import Request, urlopen

# Enter the country name
country = input("Enter the country name: ")

# Removing leading and trailing spaces, and replacing spaces with underscores
country = country.strip()
country = country.replace(" ","_")

# Construt the URL
url = "https://en.wikipedia.org/wiki/"+country+"_national_cricket_team"

req = Request(url,headers ={'User-Agent':'Mozilla/5.0'})

try:
    webpage = urlopen(req).read()
except:
    print("Error. Unable to contact " + url)
    exit()

mydata = webpage.decode("utf8")
try:
    f=open('webpage.html','w',encoding="utf-8")
    f.write(mydata)
    f.close
except:
    print("Not able to write to file webpage.html")