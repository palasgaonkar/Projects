#!/usr/bin/env python
# -*- coding: ascii -*-
import urllib2
import time
import Tkinter
import tkMessageBox
from BeautifulSoup import BeautifulSoup
import webbrowser

top = Tkinter.Tk()


def success(data):
    heading = data[0]
    text = data[1]
    top.mainloop()
    tkMessageBox.showinfo(heading, text)
    return

from time import sleep
wickets1 = -1
flag = 0
while True:
    response = urllib2.urlopen('https://www.google.co.in/?gws_rd=ssl#q=indian+cricket+team')
    html = response.read()
    soup = BeautifulSoup(html)
    print soup.rawdata

    for i, info in enumerate(soup.findAll('div', attrs={'class': 'livupd PR'})):
        score = info.string.strip()
        print score
        if 'India' in score or 'England' in score:
            for word in score.split(' '):
                if flag:
                    if int(word) > wickets1:
                        if wickets1 != -1:
                            webbrowser.open('https://www.google.co.in/?gws_rd=ssl#q=indian+cricket+team', new=1, autoraise=True)
                            # success(score.split(':'))
                        wickets1 = int(word)
                        flag = 0
                    else:
                        flag = 0
                if word == 'for':
                    flag = 1
    sleep(60)