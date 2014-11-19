
import urllib
import urllib2
import requests
from BeautifulSoup import BeautifulSoup

url = 'http://inzania.com/temp/kindle/books/'

# response = urllib2.urlopen(url)
# html = response.read()
# print html
# soup = BeautifulSoup(html)
# print soup.rawdata

# print "downloading with urllib"
# urllib.urlretrieve(url, "code.pdf")

# print "downloading with urllib2"
# f = urllib2.urlopen(url)
# data = f.read()
# with open("code2.zip", "wb") as code:
#     code.write(data)
#
# print "downloading with requests"
# r = requests.get(url)
# with open("code3.zip", "wb") as code:
#     code.write(r.content)

import urllib2


#connect to a URL
website = urllib2.urlopen('https://www.google.co.in/?gws_rd=ssl#q=python+download+all+files+from+url')

#read html code
html = website.read()

import re
#use re.findall to get all the links
links = re.findall('"((http|ftp)s?://.*?)"', html)

print links
