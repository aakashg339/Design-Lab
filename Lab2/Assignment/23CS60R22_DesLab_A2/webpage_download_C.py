import os
import random
import ply.lex as lex
import ply.yacc as yacc
import re
from urllib.request import Request, urlopen

# Get countries list from countryList.txt file by removing leading and trailing spaces
countries = []
try:
    with open('countryList.txt','r',encoding="utf-8") as f:
        for line in f:
            countries.append(line.strip())
except:
    print("Not able to read data from file countryList.txt")
    exit()

# Few country names might have spaces in them. Replace them with '_' and create another list
countries_seperated = []
for country in countries:
    countries_seperated.append(country.replace(' ','_'))

# Construct URL from the countries of the form https://en.wikipedia.org/wiki/United_States_at_the_2020_Summer_Olympics. 
urls = []
for country in countries_seperated:
    urls.append('https://en.wikipedia.org/wiki/'+country+'_at_the_2020_Summer_Olympics')

# Make a URL request for each country and store the data in a html file in folder 'countries'
directory = 'countries'
if not os.path.exists(directory):
    os.makedirs(directory)

for i in range(len(urls)):
    req = Request(urls[i],headers ={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(req).read()
    mydata = webpage.decode("utf8")
    try:
        f=open('countries/'+countries_seperated[i]+'.html','w',encoding="utf-8")
        f.write(mydata)
        f.close()
    except:
        print("Not able to write data for file ", countries_seperated[i])