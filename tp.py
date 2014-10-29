# import os
# import sys
#
# r, w = os.pipe()
# processid = os.fork()
# if processid:
# # Close write fd because parent not going to write
#     print "parent started"
#     os.close(w)
#     r = os.fdopen(r)
#     #Read from pipe
#     str = r.read()
#     print "text =", str
#     print "parent ended"
#     sys.exit(0)
# else:
#     # This is the child process
#     # Close read end cause child not going to read from pipe
#     print "Child started"
#     os.close(r)
#     w = os.fdopen(w, "w")
#     #Write to pipe
#     w.write("Text written by child...")
#     w.close()
#     print "Child ended"
#     sys.exit(0)


# def chargeMatch(pair, matchParameters):
#     """
#         This method matches charges according to weight breakages.
#
#     """
#     shipmentCharge = pair[0]
#     tariffCharge = pair[1]
#     if shipmentCharge.get("chargeCode") != tariffCharge.get("chargeName"):
#         return 0
#     for param, value in matchParameters.iteritems():
#         if tariffCharge.get(param):
#             if not tariffCharge.get(param)["to"]:
#                 tariffCharge.get(param)["to"] = float("inf")
#             if int(tariffCharge.get(param)["to"]) < value or value < int(tariffCharge.get(param)["from"]):
#                 return 0
#     return 1
#
#
# print 'Success' if chargeMatch(({"chargeCodeStatus": "Enable", "chargeCodeDescription": "HANDLING & PROCESSING",
#                                  "value": "1516", "currency": "CAD", "chargeCategory": "Documentation",
#                                  "ChargeCodeCategory": "Bill to Payer", "chargeType": "FREIGHT", "country": "CA",
#                                  "chargeCode": "123", "chargeCodeCategory": "Expense", "chargeCodeType": "HANR"},
#                                 {"calculationOnCharge": None, "zipCodes": {"to": 111, "from": 0,
#                                                                            "method": {"c": "", "g": "",
#                                                                                       "id": "538572997fa64270984d6123",
#                                                                                       "v": "538572997fa64270984d6123",
#                                                                                       "n": "A4", "tc": None}},
#                                 "weight": {"to": "23", "from": 0, "method": ""}, "min": 150, "max": None, "value": 0.5,
#                                 "fieldKey": "123_Weight_0_23_ZIPCode_0-111", "currency": "CAD", "chargeName": "123",
#                                 "operand": None}),
#                                {"zipCodes": 31.465, "weight": 4.465}) else 'Failure'


# def multiply(a, b):
#     """
#     >>> multiply(4, 3)
#     64
#     >>> multiply("a", 3)
#     "aaa"
#     """
#     if type(a) == int and type(b) == int:
#         return a**b
#     else:
#         return a * b


# digit_map = {'3': 'def', '2': 'abc', '5': 'jkl', '4': 'ghi', '7': 'pqrs', '6': 'mno', '9': 'wxyz', '8': 'tuv'}
#
#
# def word_numbers(inp):
#     inp = str(inp)
#     ret = ['']
#     for char in inp:
#         letters = digit_map.get(char, '')
#         ret = [prefix + letter for prefix in ret for letter in letters]
#     return ret
#
# print word_numbers(7252)
#
# import bisect
# a = [1, 21, 34, 34, 43, 65]
# print bisect.bisect_left(a, 43)
#
#
# def binary_search(a, x, lo=0, hi=None):
#     hi = hi if hi is not None else len(a)
#     pos = bisect.bisect_left(a, x, lo, hi)
#     return pos if pos != hi and a[pos] == x else -1
#
# print binary_search(a, 43)
#
#
# import bintrees
# tree = bintrees.BinaryTree()
# tree.insert('a', 'stolen')
# print tree._root()
#
#
# from blist import blist
# import datetime
# x = blist([0])
# t = datetime.datetime.now()
# x *= 2**9
# x[34] = 5
# print x
# print datetime.datetime.now() - t
# x.append(5)
# print x
# y = x[4:-234]
# print x
# del x[3:102]
# print x
#
# q = [0]
# t = datetime.datetime.now()
# q *= 2**9
# print q
# q[34] = 5
# print q
# print datetime.datetime.now() - t


from abc import ABCMeta, abstractmethod
class Vehicle(object):
    """A vehicle for sale by Jeffco Car Dealership.


    Attributes:
        wheels: An integer representing the number of wheels the vehicle has.
        miles: The integral number of miles driven on the vehicle.
        make: The make of the vehicle as a string.
        model: The model of the vehicle as a string.
        year: The integral year the vehicle was built.
        sold_on: The date the vehicle was sold.
    """

    __metaclass__ = ABCMeta

    base_sale_price = 0

    def sale_price(self):
        """Return the sale price for this vehicle as a float amount."""
        if self.sold_on is not None:
            return 0.0  # Already sold
        return 5000.0 * self.wheels

    def purchase_price(self):
        """Return the price for which we would pay to purchase the vehicle."""
        if self.sold_on is None:
            return 0.0  # Not yet sold
        return self.base_sale_price - (.10 * self.miles)

    @abstractmethod
    def vehicle_type(self):
        """"Return a string representing the type of vehicle this is."""
        pass

#========================================================================================

class Foo(object):
    pass

Foo = type('Foo', (), {})

def always_false(self):
    return False
Foo.always_false = always_false

Foo = type('Foo', (), {'always_false': always_false})

FooBar = type('FooBar', (Foo,), {})


#====================================================================================================

from functools import wraps

def currency(f):
    @wraps(f)  # to avoid changing .__name__ and .__doc__ of the function to be decorated
                                                                            # to this function's .__name__ and .__doc__
    def wrapper(*args, **kwargs):
        return '$' + str(f(*args, **kwargs))

    return wrapper

#=================================================================================

def get_primes(number):
    while True:
        print number
        if number:
            number = yield number  # Save parameter passed to generator as number.
        number += 1


def print_successive_primes(iterations, base=10):
    prime_generator = get_primes(base)
    prime_generator.send(None)  # Pass None first time (coz you have to)
    for power in range(iterations):
        print(prime_generator.send(base ** power), base ** power)  # Pass parameter to generator.

print_successive_primes(5)

#=================================================================================================

class Foo():
    def __init__(self):
            self.value = 0
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self.value)

f = Foo()
foo_tuple = (f, f)
print(foo_tuple)
#(0, 0)
f.value = 999
print(foo_tuple)
#(999, 999)

#=================================================================================================

root = {}
value_string = 'abc'
for character in value_string:
        root = root.setdefault(character, {})
print root

