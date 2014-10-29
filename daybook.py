#!/usr/bin/env python
# -*- coding: ascii -*-

"""
.module
~~~~~~~~~~~~~

This script handles rating according to tariff.

"""
__author__ = "Vishal Palasgaonkar"
__copyright__ = "Copyright 2013, Searce"
__credits__ = ["Vishal Palasgaonkar"]
__version__ = "1.0.0"
__maintainer__ = "Vishal Palasgaonkar"
__email__ = "vishal.palasgaonkar@searce.com"
__status__ = "Development"

import json
import datetime
import itertools
import operator
import math

from bson import ObjectId

from lib.log import logging
from generic import authenticate, GenericCRUD
from exceptions import NotFoundError, ValidationError, DuplicateError


def checkRatingRequest(request):
    """
        This function performs URL matching and calls the particular function.
    """
    if request.method == 'POST':
        l = getTariffValue(request)
        return l.read(request)


class getTariffValue(GenericCRUD):
    include = []
    exclude = ['']

    @authenticate
    #@authorise("listInvoice")
    def __init__(self, request):
        """
            This constructor sets collection name, creates an object of database
            and calls read method.
        """
        super(getTariffValue, self).__init__(request)
        self.orgName = self.getCookieData('user').get('organization')
        self.collection = self.orgName + 'ProcessData'
        self.shipment = {}
        self.finalRounding = {}
        self.ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.div}

    def untangle(self, data):
        """
            This method moves nested keys to uniform surface level.
        """
        for key, val in data.iteritems():
            if key in ['permission', 'dayBookF']:
                continue
            if type(data[key]) == dict:
                for k, v in data[key].iteritems():
                    self.shipment[k] = v
                    if type(data[key][k]) == dict:
                        self.untangle(data[key])
                self.shipment.pop(key, None)
            else:
                self.shipment[key] = val

    def rounding(self, method, roundingFactor, value):
        """
            This method does rounding according to method & factor provided.
        """
        factor = (10 ** roundingFactor)
        if method == 'Round Up':
            return math.ceil(value * factor) / factor
        if method == 'Round Down':
            return math.floor(value * factor) / factor
        if method == 'Round Off':
            return round(value, roundingFactor)

    def calculationCode(self, calculationCode, previousResult=0):
        """
            This method evaluates through the chain of calculation codes.
        """
        result = []
        for level in calculationCode.get('codeLevels'):
            # Check if operator1 & operand1/2 are available.
            if level.get('l1Field') and level.get('l2Field') and level.get('operand1'):
                # Use previous result if needed.
                level['l1Field'] = previousResult if str(level.get('l1Field')) == 'previousResult' else level.get('l1Field')
                level['l2Field'] = previousResult if str(level.get('l2Field')) == 'previousResult' else level.get('l2Field')

                # Fetch l1/l2 if not direct value and complete rounding.
                if type(level.get('l1Field')) not in [float, int]:
                    level['l1Field'] = int(self.shipment.get(level.get('l1Field')))
                level['l1Field'] = self.rounding(str(level.get('l1RoundingMethod')),
                                                 int(level.get('l1RoundingFactor')), level['l1Field'])
                if type(level.get('l2Field')) not in [float, int]:
                    level['l2Field'] = int(self.shipment.get(level.get('l2Field')))
                level['l2Field'] = self.rounding(str(level.get('l2RoundingMethod')),
                                                 int(level.get('l2RoundingFactor')), level['l2Field'])
                # Perform operation 1.
                temp = self.ops[str(level['operand1'])](level.get('l1Field'), level.get('l2Field'))

                # Check if operator2 & operand3 are available.
                if level.get('l3Field') and level.get('operand2'):
                    # Use previous result if needed.
                    level['l3Field'] = previousResult if str(level.get('l3Field')) == 'previousResult' else level.get('l3Field')

                    # Fetch l3 if not direct value and complete rounding.
                    if type(level.get('l3Field')) not in [float, int]:
                        level['l3Field'] = int(self.shipment.get(level.get('l3Field')))
                    level['l3Field'] = self.rounding(str(level.get('l3RoundingMethod')),
                                                     int(level.get('l3RoundingFactor')), level['l3Field'])
                    # Perform operation 2.
                    temp = self.ops[str(level['operand2'])](temp, level.get('l3Field'))

                result.append(self.rounding(str(level.get('resultRoundingMethod')),
                                            int(level.get('resultRoundingFactor')), temp))
            # If only 1 field provided.
            elif level.get('l1Field'):
                # Replace with previousResult if needed.
                level['l1Field'] = previousResult if str(level.get('l1Field')) == 'previousResult' else level.get('l1Field')

                # Fetch l1 if not direct value and complete rounding.
                if type(level.get('l1Field')) not in [float, int]:
                    level['l1Field'] = int(self.shipment.get(level.get('l1Field')))
                level['l1Field'] = self.rounding(str(level.get('l1RoundingMethod')),
                                                 int(level.get('l1RoundingFactor')), level['l1Field'])
                # Pass l1 as result without any operations.
                result.append(level.get('l1Field'))

            # Final result rounding.
            self.finalRounding = {'method': str(level.get('resultRoundingMethod')),
                                  'factor': int(level.get('resultRoundingFactor'))}
        # Fetch appropriate result from multiple results.
        if calculationCode.get('resultCriteria') == 'Greater':
            result = max(result)
        elif calculationCode.get('resultCriteria') == 'Lesser':
            result = min(result)
        else:
            result = result[0]
        if calculationCode.get('passToCode'):
            nextCode = self.isDuplicate({'_id': ObjectId(calculationCode['passToCode'])}, self.orgName+'Rule')
            if not nextCode:
                raise NotFoundError('Calculation code not found.')
            return self.calculationCode(nextCode, previousResult=result)
        return result

    def chargeMatch(self, pair, matchParameters):
        """
            This method matches charges according to weight breakages.
        """
        shipmentCharge = pair[0]
        tariffCharge = pair[1]
        if shipmentCharge.get('chargeCode') != tariffCharge.get('chargeName'):
            return 0
        for param in matchParameters.keys():
            if tariffCharge.get(param):
                if not tariffCharge.get(param)['to']:
                    tariffCharge.get(param)['to'] = float("inf")
                if tariffCharge.get(param)['to'] < matchParameters[param] or matchParameters[param] < tariffCharge.get(param)['from']:
                    return 0
        return 1

    def modifyDocument(self):
        """
            This method receives input data, manages conditions and data
            manipulation specific to Invoice update.
        """
        try:
            self.doc = json.loads(self.request.body)
        except Exception, e:
            logging.error(e)
            return self.response("Error in update request retrieval.")

    def listOperations(self, array, operation):
        """
            This method performs given operation on provided list.
        """
        if operation == 'MAX':
            return max(array)
        elif operation == 'MIN':
            return min(array)
        elif operation == 'SUM':
            return sum(array)
        elif operation == 'MUL':
            return reduce(lambda x, y: x * y, array)
        elif operation == 'AVERAGE':
            return sum(array) / float(len(array))

    def read(self, request):
        """
            This method after validating group exists, lists group data from the
            database collection.
        """
        try:
            time = datetime.datetime.now()
            self.modifyDocument()
            inputData = self.doc
            # Get the shipment.
            shipmentData = self.isDuplicate({'_id': ObjectId(self.doc.get('Id', ''))})
            if not shipmentData:
                raise NotFoundError('Shipment not found.')
            # Move nested keys to surface.
            self.untangle(shipmentData)
            self.collection = self.orgName + 'Template'
            account = self.isDuplicate({'_id': ObjectId(self.doc.get('accountId', ''))}, 'Account')
            # List all tariffConfiguration templates for given account & system.
            self.listDocument(0, 0, {'account': account.get('accountNumber'),
                                     'systemId': ObjectId(self.doc.get('systemId', ''))})
            from collections import defaultdict
            mainTemplates = defaultdict(set)
            otherTemplateIndices = []
            # Maintain dict with all docs matching identifiers with their lengths.
            for index, doc in enumerate(self.doc):
                length = len(doc['identifiers'])
                flag = 1
                # Match the identifiers.
                for key, val in doc['identifiers'].iteritems():
                    if self.shipment.get(key) != val:
                        flag = 0
                        break
                # Check if within effective & expiry date.
                if flag:
                    if not (doc.get('additionalTariffInfo').get('effectiveDate') <= self.shipment.get(
                            'shipmentDate') <= doc.get('additionalTariffInfo').get('expiryDate')):
                        flag = 0
                # Store Main tariffType & others separately.
                if flag:
                    if doc.get('tariffType') == 'Main':
                        mainTemplates[length].add(index)
                    else:
                        otherTemplateIndices.append({'length': length, 'position': index, 'type': doc.get('tariffType')})
            # Main tariffType template is required.
            if not mainTemplates:
                raise NotFoundError('No main template match found.')

            # Raise error if multiple max values.
            if len(mainTemplates.get(max(mainTemplates.keys()))) > 1:
                raise ValidationError('Multiple main templates found.')
            else:
                otherTemplateIndices.append({'position': list(mainTemplates.get(max(mainTemplates.keys())))[0]})

            # Select only the matched templates.
            templates = []
            for data in otherTemplateIndices:
                templates.append(self.doc[data.get('position')])

            # Fetch tariffs for all available templates & append charges.
            tariffCharges = []
            for template in templates:
                tempIn = template.get('parameters')
                tempOut = {}
                # Turn parameters to key: value format.
                for t in tempIn:
                    tempOut.update({t.get('key'): self.shipment.get(t.get('key'))})
                template['parameters'] = tempOut
                accountNumber = self.isDuplicate(ObjectId(inputData.get('accountId')), 'Account').get('accountNumber')
                tempOut.update({'templateId': ObjectId(template.get('id')), 'systemId': template.get('systemId'),
                                'account': accountNumber, 'effectiveDate': {'$lte': time}, 'expiryDate': {'$gte': time}})

                # Fetch tariff.
                if self.dbObj[self.orgName + 'Tariffs'].find(tempOut).count() > 1:
                    templateName = self.isDuplicate({'_id': ObjectId(template.get('id'))}).get('tariffName')
                    raise DuplicateError('Multiple lanes found for ' + templateName + ' tariff.')
                tariff = self.isDuplicate(tempOut, self.orgName + 'Tariffs')
                if not tariff:
                    continue
                    # raise NotFoundError('No tariff found.')
                tariffCharges = list(itertools.chain(tariffCharges, tariff.get('charges')))

            finalValue = {}
            # Cartesian product for list of charges from shipment & lane tariff.
            for element in itertools.product(inputData.get('charges'), tariffCharges):
                # Match charges.
                if self.chargeMatch(element, {"weight": self.shipment.get('chargeableWeight')}):
                    calculationCode = self.isDuplicate({'_id': ObjectId(element[1].get('method'))},
                                                       self.orgName + 'Rule')
                    if not calculationCode:
                        raise NotFoundError('Calculation code not found.')
                    previousResult = 0
                    if element[1].get('calculationOnCharge'):
                        calculationOnCharge = [finalValue.get(chargeName) for chargeName
                                               in element[1]['calculationOnCharge']]
                        previousResult = self.listOperations(calculationOnCharge, element[1].get('operand'))
                    result = self.calculationCode(calculationCode, previousResult)
                    # print result
                    if not result:
                        raise ValidationError('Calculation code invalid.')
                    # Multiply by value.
                    result *= element[1].get('value')

                    # Check min max conditions.
                    if element[1].get('min') and element[1].get('min') > result:
                        result = element[1].get('min')
                    if element[1].get('max') and element[1].get('max') < result:
                        result = element[1].get('max')
                    # Result rounding.
                    result = self.rounding(self.finalRounding.get('method'),
                                           self.finalRounding.get('factor'), result)
                    # toCurrency to be used later.
                    toCurrency = account.get('currency')
                    currencyConversion = self.isDuplicate({'details.currencyCode': element[1].get('currency'),
                                                           "type": "exchangeRate"}, self.orgName + 'Metadata')
                    if currencyConversion:
                        conversionRate = currencyConversion['details'].get('exchangeRate')
                        # Currency conversion & final rounding.
                        result *= conversionRate
                        result = self.rounding(self.finalRounding.get('method'),
                                               self.finalRounding.get('factor'), result)
                    finalValue.update({element[1].get('chargeName'): result})
            rateMatchCounter = 0
            # Merge result according to charge code to the input charges.
            for charge in inputData.get('charges'):
                charge['tariffValue'] = finalValue.get(charge.get('chargeCode'))
                if finalValue.get(charge.get('chargeCode')) and charge.get('userValue'):
                    charge['status'] = 'unmatched'
                if charge.get('userValue') == finalValue.get(charge.get('chargeCode')) \
                    and charge.get('userValue') is not None:
                    charge['status'] = 'matched'
                    rateMatchCounter += 1
            inputData['status'] = 'Rated' if rateMatchCounter == len(inputData.get('charges')) else 'Rate Mismatch'
            return self.response(inputData)
        except NotFoundError, e:
            logging.error(e)
            return self.response(e.message, 404)
        except ValidationError, e:
            logging.error(e)
            return self.response(e.message, 406)
        except Exception, e:
            logging.error(e)
            return self.response(e.message, 402)