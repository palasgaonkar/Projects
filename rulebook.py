#!/usr/bin/env python
# -*- coding: ascii -*-

"""
.module
~~~~~~~~~~~~~
This module takes nested rule conditions and converts them into MongoDB query.
"""
__author__ = "Vishal Palasgaonkar"
__copyright__ = "Copyright 2013, Searce"
__credits__ = ["Vishal Palasgaonkar"]
__version__ = "1.0.0"
__maintainer__ = "Vishal Palasgaonkar"
__email__ = "vishal.palasgaonkar@searce.com"
__status__ = "Development"


class RuleBook():
    include = []
    exclude = ['']

    def __init__(self):
        """
            This constructor sets collection name, creates an object of database.
        """
        self.condition = ''
        self.prefix = ''

    rules = {'notEqualTo': "$ne", 'lessThan': "$lt", 'greaterThan': "$gt", 'lessThanEqualTo': "$lte",
             'greaterThanEqualTo': "$gte", 'isInList': "$in", 'isNotInList': "$nin"}

    def ruleBook(self, condition, prefix=''):
        self.condition = condition
        self.prefix = prefix
        if self.condition:
            self.querify(self.condition)
            return self.condition
        else:
            return {}

    def regexRules(self, operator, name, value):
        """
            This method handles regex based rules.
        """
        regexLookup = {'contains': {'$regex': value, '$options': 'i'}, # case insensitive.
                       'doesNotContain': {'$regex': '^((?!' + value + ').)*$'},
                       'beginsWith': {'$regex': '^' + value, '$options': '-i'},
                       'doesNotBeginWith': {'$regex': '^(?!' + value + ').+', '$options': '-i'},
                       'endsWith': {'$regex': value + '$', '$options': '-i'},
                       'doesNotEndWith': {'$regex': '.*(?<!' + value + ')$', '$options': '-i'}}
        if operator in regexLookup.keys():
            return {self.prefix + name: regexLookup.get(operator)}

            # if operator == 'contains':
            #     return {self.prefix + name: {'$regex': value, '$options': 'i'}}  #case insensitive.
            # elif operator == 'doesNotContain':
            #     return {self.prefix + name: {'$regex': '^((?!' + value + ').)*$'}}
            # elif operator == 'beginsWith':
            #     return {self.prefix + name: {'$regex': '^' + value, '$options': '-i'}}
            # elif operator == 'doesNotBeginWith':
            #     return {self.prefix + name: {'$regex': '^(?!' + value + ').+', '$options': '-i'}}
            # elif operator == 'endsWith':
            #     return {self.prefix + name: {'$regex': value + '$', '$options': '-i'}}
            # elif operator == 'doesNotEndWith':
            #     return {self.prefix + name: {'$regex': '.*(?<!' + value + ')$', '$options': '-i'}}

    def multiValueRules(self, operator, name, value1, value2):
        """
            This method handles multivalued rules.
        """
        multiValueLookup = {'betweenInclusive': {'$gte': value1, '$lte': value2}, # case insensitive.
                            'betweenExclusive': {'$gt': value1, '$lt': value2}}
        if operator in multiValueLookup.keys():
            return {self.prefix + name: multiValueLookup.get(operator)}

            # if operator == 'betweenInclusive':
            #     return {self.prefix + name: {'$gte': value1, '$lte': value2}}
            # elif operator == 'betweenExclusive':
            #     return {self.prefix + name: {'$gt': value1, '$lt': value2}}

    def whereRules(self, operator, name1, name2):
        """
            This method handles field to field comparisons.
        """
        whereLookup = {
            'betweenInclusive': {'$where': 'this.' + self.prefix + name1 + ' == ' + 'this.' + self.prefix + name2}}
        if operator in whereLookup.keys():
            return whereLookup.get(operator)

            # if operator == 'equalTo':
            #     return {'$where': 'this.' + self.prefix + name1 + ' == ' + 'this.' + self.prefix + name2}

    def querify(self, doc):
        """
            This method converts json based rule structure to MongoDB query.
        """
        if type(doc) == dict:
            doc.pop('level', None)
            if doc.get('condition') == 'or':
                if doc.get('fields'):
                    doc['$or'] = doc.pop('fields')
                    doc.pop('condition', None)
                    for d in doc.get('$or'):
                        self.querify(d)
                doc.pop('condition', None)
                doc.pop('fields', None)
            elif doc.get('condition') == 'and':
                if doc.get('fields'):
                    doc['$and'] = doc.pop('fields')
                    doc.pop('condition', None)
                    for d in doc.get('$and'):
                        self.querify(d)
                doc.pop('condition', None)
                doc.pop('fields', None)
            elif doc.get('matchField'):
                doc.update(self.whereRules(doc.get('operator'), doc.get('name'), doc.get('matchField')))
                doc.pop("name", None)
                doc.pop("matchField", None)
            elif doc.get('operator') == 'equalTo':
                doc.update({self.prefix + doc.get('name'): doc.get('value')})
            elif self.rules.get(doc['operator']):
                doc.update({self.prefix + doc.get('name'): {self.rules.get(doc.get('operator')): doc.get('value')}})
            elif doc.get('operator') in ['contains', 'doesNotContain', 'beginsWith', 'doesNotBeginWith', 'endsWith',
                                         'doesNotEndWith']:
                doc.update(self.regexRules(doc.get('operator'), doc.get('name'), doc.get('value')))
            elif doc.get('operator') in ['betweenInclusive', 'betweenExclusive']:
                doc.update(
                    self.multiValueRules(doc.get('operator'), doc.get('name'), doc.get('value1'), doc.get('value2')))
                doc.pop("value1", None)
                doc.pop("value2", None)
            doc.pop("name", None)
            doc.pop("operator", None)
            doc.pop("value", None)


            # temp = {"condition": "and", "level": "0", "fields": [{"name": "tariffCode", "operator": "beginsWith", "value": "abc"}]}
            # c = RuleBook()
            # print c.ruleBook(temp)