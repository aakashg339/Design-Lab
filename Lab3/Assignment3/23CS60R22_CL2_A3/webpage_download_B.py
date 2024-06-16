import os
from urllib.request import Request, urlopen

# Getting player name from user
player_name = input("Enter player name: ")

# Performing preprocessing on player name. From each word removing leading and trailing spaces and seperating each word with underscore
player_name = player_name.strip()
player_name = player_name.replace(" ", "_")

# Creating the url for the player. For ex - https://en.wikipedia.org/wiki/Harry_Brook
url = "https://en.wikipedia.org/wiki/" + player_name

req = Request(url,headers ={'User-Agent':'Mozilla/5.0'})
try:
    webpage = urlopen(req).read()
except:
    print("Player name incorrect. Printing last searched player data")
    exit()
mydata = webpage.decode("utf8")

try:
    f=open('webpage_player.html','w',encoding="utf-8")
    f.write(mydata)
    f.close
except:
    print("Not able to write to file webpage.html")