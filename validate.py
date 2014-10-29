#!/usr/bin/env python
# -*- coding: ascii -*-

"""
dayBook.module
~~~~~~~~~~~~~
This module retrieves DayBookF report files from server, parses it & stores each entry as document.
Then it retrieves InvAudit report from server, parses it & tags status as billed for each entry in it.
This module then fetches rules from database & applies tags according to them.
"""
__author__ = "Vishal Palasgaonkar"
__copyright__ = "Copyright 2013, Searce"
__credits__ = ["Vishal Palasgaonkar"]
__version__ = "1.0.0"
__maintainer__ = "Vishal Palasgaonkar"
__email__ = "vishal.palasgaonkar@searce.com"
__status__ = "Development"

import datetime
import os
import copy
import shutil
import imp
from operator import itemgetter

import xlrd
import pymongo
from bson import ObjectId

from ruleBook import RuleBook
from reportLog import logging


conf = imp.load_source('*', '/home/dev_api/config.py')
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
(MONGO_HOST, MONGO_DB, BASE_DOMAIN, SESSION_COOKIE_DOMAIN,
 MONGO_PORT, MONGO_UNAME, MONGO_PASSWD, USER_DB) = conf.getDetails(PROJECT_DIR)


class Parse():
    def __init__(self):
        """
            This constructor sets collection name, creates an object of database.
        """
        self.collection = 'Searce20140226092321RawData'
        self.doc = {}
        conn = pymongo.Connection(MONGO_HOST, MONGO_PORT)
        conn[MONGO_DB].authenticate(MONGO_UNAME, MONGO_PASSWD)
        self.dbObj = conn[MONGO_DB]
        self.time = datetime.datetime.utcnow()
        self.mapping = {}
        self.rule = [mapRule['details'] for mapRule in
                     self.dbObj['DefaultMetadata'].find({"type": "dayBookFShipmentMapping"})]

    def map(self, doc):
        """

        """
        finalData = {'shipmentFields': {}}
        for rule in self.rule:
            rule['dayBookFKey'] = doc['data'].pop(rule.get('dayBookFKey'), None)
            if rule.get('shipmentFieldsGroup'):
                finalData['shipmentFields'].setdefault(rule.get('shipmentFieldsGroup'), {}).update(
                    {rule.get('shipmentFieldsKey'): rule.get('dayBookFKey')})
                # if finalData['shipmentFields'].get(rule.get('shipmentFieldsGroup')):
                #     finalData['shipmentFields'][rule.get('shipmentFieldsGroup')].update({rule.get('shipmentFieldsKey'): rule.get('dayBookFKey')})
                # else:
                #     finalData['shipmentFields'].update({rule.get('shipmentFieldsGroup'): {rule.get('shipmentFieldsKey'): rule.get('dayBookFKey')}})
            else:
                finalData.update({'account':
                                      self.dbObj['Account'].find_one({'accountNumber': rule.get('dayBookFKey')})[
                                          '_id']})
                accountProfile = self.dbObj['Account'].find_one({'accountNumber': rule.get('dayBookFKey')})[
                    'templateId']
                finalData.update({'system':
                                      self.dbObj['System'].find_one({'accountProfile': accountProfile})['_id']})
                finalData.update({rule.get('shipmentFieldsKey'): rule.get('dayBookFKey')})
        finalData.update({'dayBookF': doc.pop('data')})
        finalData.update({"allocatedTo": doc['tag']['allocatedTo']})
        finalData['shipmentFields'].update({"status": "Ready for Processing", "IssueStatus": None})
        self.dbObj['Searce20140226092321ProcessData'].insert(finalData)


    def columnize(self, A, i):
        """
            This method converts a row in the document into a dictionary with first row forming the keys.
            It also converts any date value into DATE format.
        """
        doc = {}
        for index in xrange(len(A.row_values(0))):
            if 'DATE' in A.row_values(0)[index] and A.row_values(i)[index]:
                g, d = divmod(A.row_values(i)[index], 1)
                g = int(g)
                d = int(d)
                if d == 0:
                    d = '000000'
                doc.update({A.row_values(0)[index]: datetime.datetime.strptime(str(g) + str(d), '%Y%m%d%H%M%S')})
            else:
                doc.update({A.row_values(0)[index]: A.row_values(i)[index] if A.row_values(i)[index] else None})
        return doc

    def document(self, doc):
        """
            This method appends details to the document.
        """
        return {'data': doc, 'reportName': 'daybook',
                'receivedOn': self.time, 'sheet': 'A',
                'tag': {'status': 'unbilled'}}

    def parseXls(self):
        """
            This method parses xls format
        """
        logging.info("Script started")
        path = '/home/Searce.FTPUser/DayBookF/'
        for dayBookFile in os.listdir(path):
            if dayBookFile.endswith('.xls'):
                logging.info("File: " + dayBookFile + " found")
                outfile = xlrd.open_workbook(path + dayBookFile)
                A = outfile.sheet_by_index(0)
                for i in xrange(A.nrows - 1):
                    # Check if document is repeated.
                    if not self.dbObj[self.collection].find_one({"data.BOKPRT": A.row_values(i + 1)[5]}):
                        self.dbObj[self.collection].insert(self.document(self.columnize(A, i + 1)))
                logging.info("File: " + dayBookFile + " processed")
                shutil.move(path + dayBookFile, path + './archive/')
                logging.info("File: " + dayBookFile + " moved to archive")

        path = '/home/Searce.FTPUser/InvAudit/'
        for auditFile in os.listdir(path):
            if auditFile.endswith('.xls'):
                logging.info("File: " + auditFile + " found")
                infile = xlrd.open_workbook(path + auditFile)
                B = infile.sheet_by_index(0)
                col = B.col_values(7)
                self.dbObj[self.collection].update({"data.BOKPRT": {"$in": col}}, {'$set': {"tag.status": "billed"}},
                                                   upsert=False, multi=True)
                logging.info("File: " + auditFile + " processed")
                shutil.move(path + auditFile, path + './archive/')
                logging.info("File: " + auditFile + " moved to archive")

        self.collection = 'Searce20140226092321Rule'
        results = [result for result in self.dbObj[self.collection].find({'ruleType': 'metadata_dayBookF'})]
        for ind, val in enumerate(results):
            results[ind]["id"] = str(results[ind].pop("_id"))
        self.doc = results
        self.collection = 'Searce20140226092321RawData'
        r = RuleBook()
        rules = self.doc
        for rule in rules:
            ruleDef = copy.deepcopy(rule.get('ruleDef'))
            query = r.ruleBook(ruleDef, 'data.')
            query.update({'receivedOn': self.time})
            results = [result for result in self.dbObj[self.collection].find(query)]
            for ind, val in enumerate(results):
                results[ind]["id"] = str(results[ind].pop("_id"))
            self.doc = results
            for doc in self.doc:
                if rule.get('isField'):
                    for field in rule['ruleDef']['fields']:
                        doc['tag'].update({rule.get('labelType'): doc['data'][(field.get('matchField'))]})
                elif not rule.get('isField'):
                    for field in rule['ruleDef']['fields']:
                        doc['tag'].update({rule.get('labelType'): field.get('value')})
                self.dbObj[self.collection].update({"_id": ObjectId(doc.get('id'))}, {"$set": doc})
        logging.info("Rules applied")

        self.collection = 'Searce20140226092321Rule'
        results = [result for result in self.dbObj[self.collection].find({'ruleType': 'metadata_workFlow'})]
        if results:
            for res in results:
                userData = res
                self.collection = userData.get('source')['details']['collectionName'].replace('DBName',
                                                                                              'Searce20140226092321')
                r = RuleBook()
                query = r.ruleBook(userData.get('conditions'))
                query = {'$and': [query, {"tag.allocatedTo": {"$exists": False}}]}
                count = self.dbObj[self.collection].find(query).count()
                remainingCount = count
                if count == 0:
                    logging.info('No data satisfying the rule for workflow management.')
                userlist = sorted(userData.get('allocated'), key=itemgetter('work'), reverse=True)
                for i, user in enumerate(userlist):
                    emailId = self.dbObj['Users'].find_one({'_id': ObjectId(user.get('user'))})['email']
                    limit = int(round(int(user.get('work')) * count / 100))
                    if i == len(userlist) - 1:
                        limit = remainingCount
                    remainingCount -= limit
                    if limit:
                        self.doc = [result for result in self.dbObj[self.collection].find(query).skip(0).limit(limit)]
                        for ind, val in enumerate(results):
                            results[ind]["id"] = str(results[ind].pop("_id"))
                        if self.doc:
                            for doc in self.doc:
                                doc.setdefault('tag', {}).update({'allocatedTo': emailId})
                                # if doc.get('tag'):
                                #     doc['tag'].update({'allocatedTo': emailId})
                                # else:
                                #     doc.update({'tag': {'allocatedTo': emailId}})
                                self.dbObj[self.collection].update({"_id": ObjectId(doc.get('id'))}, doc)
                                self.map(doc)


c = Parse()
c.parseXls()