# !/usr/bin/env python
# -*- coding: ascii -*-

# import smtplib
#
#
# FROMADDR = "vishalpalasgaonkar1@gmail.com"
# LOGIN = FROMADDR
# PASSWORD = ""
# TOADDRS = ["vishal.palasgaonkar@searce.com"]
# SUBJECT = "Test"
#
# msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
#        % (FROMADDR, ", ".join(TOADDRS), SUBJECT))
#
# msg += "Hi there"
#
# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.set_debuglevel(1)
# server.ehlo()
# server.starttls()
# server.login(LOGIN, PASSWORD)
# server.sendmail(FROMADDR, TOADDRS, msg)
# server.quit()


# class ModularTuple(tuple):
#     def __new__(cls, tup, size=100):
#         tup = (int(x) % size for x in tup)
#         return super(ModularTuple, cls).__new__(cls, tup)
#
# c = ModularTuple((1, 324, 23, 400))
# print c


# from copy import deepcopy
#
# def resetDefaults(f):
#     defaults = f.func_defaults
#     def resetter(*args, **kwds):
#         f.func_defaults = deepcopy(defaults)
#         return f(*args, **kwds)
#     return resetter
#
# # @resetDefaults
# def function(item, stuff=[]):
#     stuff.append(item)
#     print stuff
#
# function(1)
# function(2)

import itertools

cost = {}
weight = 100
items = [[1, 53, 98], [2, 98, 97], [3, 78, 3], [4, 72, 76], [5, 10, 9], [6, 46, 96]]
for item in items:
    item.append({item[1]: item[1] * item[2]})
items = list(zip(*items))
items[3] = {k: v for d in items[3] for k, v in d.items()}

for i in range(len(items)):
    for subset in itertools.combinations(items[1], i + 1):
        if sum(list(subset)) <= weight:
            cost.update({sum([items[3][sub] for sub in list(subset)]): list(subset)})
print max(cost), cost[max(cost)]

f = lambda p: p and [i + j for i in '0 1 ABC DEF GHI JKL MNO PRS TUV WXY'.split()[int(p[0])] for j in f(p[1:])] or [p]
print f('4155230')

