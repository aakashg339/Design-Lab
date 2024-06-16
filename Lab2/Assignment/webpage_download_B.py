import os
import random
import ply.lex as lex
import ply.yacc as yacc
import re
from urllib.request import Request, urlopen
req = Request('https://en.wikipedia.org/wiki/2020_Summer_Olympics',headers ={'User-Agent':'Mozilla/5.0'})
webpage = urlopen(req).read()
mydata = webpage.decode("utf8")

# Extracting the sports names using regex. Below is the pattern used
#</span></span> <a href="/wiki/Marathon_swimming_at_the_2020_Summer_Olympics"
# pattern = re.compile(r'</span></span> <a href="/wiki/(.*?)_at_the_2020_Summer_Olympics"')
# matches = pattern.findall(mydata)

# Currently Working
matches = ['Diving', 'Badminton', 'Boxing', 'Fencing', 'Field_hockey', 'Sailing', 'Shooting', 'Surfing', 'Table_tennis', 'Taekwondo', 'Weightlifting', 'Wrestling']

# Randomly sepecting any five sports from the list of sports
random_sports = random.sample(matches,5)

# random_sports = ['Boxing', 'Weightlifting', 'Gymnastics', 'Table_tennis', 'Rowing', 'Wrestling', 'Triathlon', 'Tennis', 'Taekwondo', 
#                  'Sport_climbing', 'Shooting', 'Sailing', 'Rugby_sevens', 'Gymnastics', 'Archery', 'Artistic_swimming', 'Badminton', 'Diving']

# Creating the url for each sport of the form https://en.wikipedia.org/wiki/<sport_name>_at_the_2020_Summer_Olympics
url = []
for sport in random_sports:
    url.append('https://en.wikipedia.org/wiki/'+sport+'_at_the_2020_Summer_Olympics')

# Making a URL request for each sport and storing the data in a html file in folder 'sports'
directory = 'sports'
if not os.path.exists(directory):
    os.makedirs(directory)
for i in range(len(url)):
    req = Request(url[i],headers ={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(req).read()
    mydata = webpage.decode("utf8")
    try:
        f=open('sports/'+random_sports[i]+'.html','w',encoding="utf-8")
        f.write(mydata)
        f.close()
    except:
        print("Not able to write data for file ", random_sports[i])

# Storing the name of the 5 sports in file sports.txt
try:
    f = open('sports.txt','w',encoding="utf-8")
    for sport in random_sports:
        f.write(sport+'\n')
    f.close()
except:
    print("Not able to write data for file sports.txt")