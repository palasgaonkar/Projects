#!/usr/bin/env python
# -*- coding: ascii -*-
import urllib2
import time
import Tkinter
import tkMessageBox
from BeautifulSoup import BeautifulSoup

top = Tkinter.Tk()


def success(data):
    heading = data[0]
    text = data[1]
    tkMessageBox.showinfo(heading, text)


count = 0
check = True
while check:
    count += 1
    response = urllib2.urlopen(
        'http://www.flipkart.com/moto-e/p/itmdvuwsybgnbtha?pid=MOBDVHC6XKKPZ3GZ&srno=t_1&query=moto+e')
    html = response.read()
    if "Buy Now" in html:
        success()
        check = False
    else:
        time.sleep(60)
        print str(count) + "\tMoto E Unavailable Now"
