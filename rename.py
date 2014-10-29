#!/usr/bin/env python
# -*- coding: ascii -*-

import os
import itertools


# path = '/home/likewise-open/PUNESEZ/vishal.palasgaonkar/Pictures'
# os.chdir(path)
#
# print __file__
# print os.path.dirname(os.path.realpath(__file__)), os.path.realpath(__file__), os.getcwd()
#
# for fileName in os.listdir(path):
#     print fileName
#     name = fileName.split('.')[0]
#     newName = ''
#     for word in name.split('-'):
#         newName += word[0].upper()
#         newName += word[1:]
#     extension = fileName.split('.')[1]
#     print newName, extension
#     os.rename(fileName, '.'.join([newName, extension]))


path = '/usr/share/dict/words'
with open(path) as f:
    data = f.readlines()
    for word in data:
        if len(word) == 4:
            print word
            print ["".join(perm) if "".join(perm) in data else '' for perm in itertools.permutations(word)]
