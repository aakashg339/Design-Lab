import os
import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen
# https://en.wikipedia.org/wiki/United_States_at_the_2020_Summer_Olympics
req = Request('https://en.wikipedia.org/wiki/2020_Summer_Olympics',headers ={'User-Agent':'Mozilla/5.0'})
webpage = urlopen(req).read()
mydata = webpage.decode("utf8")
try:
    f=open('webpage.html','w',encoding="utf-8")
    f.write(mydata)
    f.close
except:
    print("Not able to write data for file webpage.html")