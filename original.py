#!/usr/bin/env python
# -*- coding: ascii -*-

"""
company.module
~~~~~~~~~~~~~


This script contains methods to perform CRUD operations on Company collection.
Generic methods are inherited and conditions specific to company are carried out.

"""
__author__ = "Vishal Palasgaonkar"
__copyright__ = "Copyright 2013, Searce"
__credits__ = ["Vishal Palasgaonkar"]
__version__ = "1.0.0"
__maintainer__ = "Vishal Palasgaonkar"
__email__ = "vishal.palasgaonkar@searce.com"
__status__ = "Development"

import json

from bson import ObjectId
from django.http import HttpResponse

from lib.log import logging
from generic import authenticate, authorise, Create, Update, Delete, Read, List, GenericCRUD


def checkCompanyRequestType(request):
    """
        This function performs URL matching and calls the particular function.
    """
    if request.method == 'POST':
        c = CreateCompany(request)
        return c.insert()
    elif request.method == 'GET':
        l = ListCompany(request)
        return l.list()
    else:
        return HttpResponse("Invalid Request method " + request.method, content_type='application/text')


def checkCompanyReadRequest(request, id):
    """
        This function performs URL matching and calls the particular function.
    """
    if request.method == 'GET':
        l = ReadCompany(request, id)
        return l.read()
    elif request.method == 'PUT':
        u = UpdateCompany(request, id)
        return u.update()

#    elif request.method == 'DELETE':
#        d = DeleteCompany(request, id)
#        return d.delete()


class CreateCompany(Create):
    @authenticate
    #@authorise("createCompany")
    def __init__(self, request):
        """
            This constructor sets collection name, creates an object of database
            and calls insert method.
        """
        super(CreateCompany, self).__init__(request)
        self.collection = "Company"

    def getTemplateId(self):
        """
            This method returns the ObjectId of default company template.
        """
        return self.isDuplicate({"profileName": "default", "docType": "company"},
                                self.getCookieData('user')['organization'] + 'Template')["_id"]

    def modifyDocument(self):
        """
            This method receives input data, manages conditions and data
            manipulation specific to company creation.
        """
        try:
            self.doc = json.loads(self.request.raw_post_data)
            #self.doc["parentCompany"] = ObjectId(self.doc.get("parentCompany", ""))
            #self.doc["organization"] = ObjectId(self.doc.get("organization", ""))
        except Exception, e:
            logging.error(e)
            return self.response("Error in create request retrieval.", 412)

    def insert(self):
        """
            This method after validating for duplication, inserts company data in
            the database collection.
        """
        try:
            self.modifyDocument()
            temp = self.getTemplateId() if not self.doc.get("templateId") else ObjectId(self.doc.get("templateId"))
            error = self.validate()
            if error:
                return self.response({"msg": error}, 412)
            self.separate()
            self.doc["templateId"] = temp
            if self.isDuplicate({"companyName": self.doc["companyName"]}):
                raise Exception("Company exists!", 412)
            self.createSessionDetails()
            self.doc.update({"organization": ObjectId(self.getCookieData('user')['organizationId'])})
            id = self.insertDocument(self.doc)
            return self.response({"msg": "Company created", "id": id})
        except Exception, e:
            logging.error(e)
            return self.response({"msg": "Company could not be created"}, 412)


class ReadCompany(Read):
    include = []
    exclude = ['']

    @authenticate
    #@authorise("readCompany")
    def __init__(self, request, id):
        """
            This constructor sets collection name, creates an object of database
            and calls read method.
        """
        super(ReadCompany, self).__init__(request)
        self.collection = "Company"
        self.id = id

    def read(self):
        """
            This method after validating company exists, reads company data from the
            database collection.
        """
        try:
            if not self.isDuplicate({"_id": ObjectId(self.id)}):
                raise Exception("Company does not exist!", 412)
            self.readDocument(self.id)
            readData = self.doc
            self.readDocument(readData['templateId'], self.getCookieData('user')['organization'] + 'Template')
            self.merge(readData)
            return self.response(self.doc)
        except Exception, e:
            logging.error(e)
            return self.response({"msg": "Error in Company data read."}, 412)


class UpdateCompany(GenericCRUD):
    include = []
    exclude = [""]

    @authenticate
    #@authorise("updateCompany")
    def __init__(self, request, id):
        """
            This constructor sets collection name, creates an object of database
            and calls update method.
        """
        super(UpdateCompany, self).__init__(request)
        self.collection = "Company"
        self.id = id

    def modifyDocument(self):
        """
            This method receives input data, manages conditions and data
            manipulation specific to company update.
        """
        try:
            self.doc = json.loads(self.request.body)
        except Exception, e:
            logging.error(e)
            return self.response("Error in update request retrieval.", 412)

    def updateHistory(self):
        """
            This method updates user in organization history collection.
        """
        try:
            self.readDocument(ObjectId(self.id))
            orgName = self.isDuplicate({"_id": ObjectId(self.doc["organization"])}, "Organization")["organization"]
            collection = orgName[0].upper() + orgName[1:] + 'History'
            temp_doc = self.doc
            self.doc = {}
            self.updateSessionDetails()
            self.doc["oldDoc"] = temp_doc
            self.insertDocument(self.doc, collection)
        except Exception, e:
            logging.error(e)
            return self.response({"msg": "Company could not be updated in organization history."}, 412)

    def update(self):
        """
            This method after validating company exists, updates company data in the
            database collection.
        """
        try:
            if not self.isDuplicate({"_id": ObjectId(self.id)}):
                raise Exception("Company does not exist!", 412)
            self.updateHistory()
            self.modifyDocument()
            error = self.validate()
            if error:
                return self.response({"msg": error}, 412)
            self.separate()
            self.updateSessionDetails()
            self.updateDocument(self.doc, ObjectId(self.id))
            return self.response({"msg": "Company updated successfully."})
        except Exception, e:
            logging.error(e)
            return self.response({"msg": "Error in Company update."}, 412)


class ListCompany(List):
    include = []
    exclude = ['']

    @authenticate
    #@authorise("listCompany")
    def __init__(self, request):
        """
            This constructor sets collection name, creates an object of database
            and calls read method.
        """
        super(ListCompany, self).__init__(request)
        self.collection = "Company"

    def modifyDocument(self):
        """
            This method receives input data, manages conditions and data
            manipulation specific to company List operation.
        """
        try:
            for eachData, val in self.request.GET.iteritems():
                self.doc[eachData] = val
        except Exception, e:
            logging.error(e)
            return self.response("Error in list request retrieval.", 412)

    def list(self):
        """
            This method after validating group exists, lists group data from the
            database collection.
        """
        try:
            self.modifyDocument()
            pageNo = self.request.GET.get("pageNo", 0)
            pageLimit = self.request.GET.get("pageLimit", 0)
            #If no page and limit values provided, list whole document.
            self.listDocument(pageNo, pageLimit,
                              {"organization": ObjectId(self.getCookieData('user')['organizationId'])})
            temp = []
            [temp.append({"id": doc.get('id', ''), "title": doc.get('companyName', ''),
                          "fields": [{'label': "Parent Company", 'value': doc.get('parentCompany', '')},
                                     {'label': "City", 'value': doc.get('city', '')},
                                     {'label': "Company Country", 'value': doc.get('companyCountry', '')}]}) for doc in
             self.doc]
            return self.response(temp)
        except Exception, e:
            logging.error(e)
            return self.response({"msg": "Error in Company data list."}, 412)