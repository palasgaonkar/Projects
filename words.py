#!/usr/bin/env python
# -*- coding: ascii -*-
import itertools
import enchant


""" Without duplicate letters. """

# letters = {'o': 2, 'p': 1, 'e': 1, 'n': 4, 'd': 3}
# wordValueMultiplier = {'o': 2, 'e': 3}
# maxValue = 0
# maxValueWord = None
# dictionary = enchant.Dict("en_US")
#
#
# for length in xrange(1, len(letters.keys())):
#     for combo in itertools.combinations(letters.keys(), length+1):
#         for word in itertools.permutations(combo):
#             if dictionary.check(''.join(word)):
#                 value = 0
#                 for letter in word:
#                     value += letters.get(letter)
#                 for letter in word:
#                     if letter in wordValueMultiplier.keys():
#                         value *= wordValueMultiplier.get(letter)
#                 if maxValue < value:
#                     maxValue = value
#                     maxValueWord = ''.join(word)
# print maxValueWord, maxValue


""" With duplicate letters. """

letters = {'q': 10, 'i': 1, 'a': 1, 'g': 6, 'h': 3, 'b': 4, 'n': [{2: 3}], 'm': [{4: 2}], 'e': [{2: 1}, {1: 1}],
           'o': [{1: 1}, {1: 1}], 's': [{3: 1}, {2: 1}]}
maxValue = 0
maxValueWord = None
dictionary = enchant.Dict("en_US")


availableLetters = []
for key, val in letters.iteritems():
    if type(letters.get(key)) != list:
        availableLetters.append(key)
    else:
        for i in xrange(len(val)):
            availableLetters.append(key)
for length in xrange(1, len(availableLetters)):
    for combo in itertools.combinations(availableLetters, length+1):
        for word in itertools.permutations(combo):
            wordValueMultiplier = []
            visited = []
            if dictionary.check(''.join(word)):
                value = 0
                for letter in word:
                    if letter not in visited:
                        if type(letters.get(letter)) != list:
                            value += letters.get(letter)
                        elif len(letters.get(letter)) == 1:
                            value += letters.get(letter)[0].keys()[0]
                            wordValueMultiplier.append(letters.get(letter)[0].values()[0])
                        elif len(letters.get(letter)) == word.count(letter):
                            for option in letters.get(letter):
                                value += option.keys()[0]
                                wordValueMultiplier.append(option.values()[0])
                                visited.append(letter)
                        else:
                            for i in xrange(''.join(word).count(letter)):
                                selection = sorted([dict(zip(a.values(), a.keys()))for a in letters.get(letter)],
                                                   reverse=True)[i]
                                value += selection.values()[0]
                                wordValueMultiplier.append(selection.keys()[0])
                            visited.append(letter)
                for mul in wordValueMultiplier:
                    value *= mul
                if maxValue < value:
                    maxValue = value
                    maxValueWord = ''.join(word)
                    print maxValueWord, maxValue, wordValueMultiplier

print maxValueWord, maxValue
