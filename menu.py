#!/usr/bin/env python
# -*- coding: ascii -*-
import csv
import sys


INF = float('inf')

# For using set operations.
keys = set(sys.argv[2:])

# Get filename from command line.
with open(sys.argv[1]) as f:
    reader = csv.reader(f, delimiter=',', skipinitialspace=True)
    data = {}

    for row in reader:
        hotel_id = row[0]
        price = row[1]
        items = row[2:]
        price = float(price)
        if all(k in items for k in keys):
            # If all keys are found in this row, then the data will be saved in the 'combo' key of this hotel_id
            # i.e. a single item or a combo contains requested items.
            d = data.setdefault(hotel_id, {})
            d['combo'] = min(price, d.get('combo', INF))

        else:
            # otherwise just loop through the intersecting key and save their values in their respective hotel_ids
            flag = 0
            for item in keys.intersection(items):
                d = data.setdefault(hotel_id, {})
                # If more than one items requested are found in a combo, price counted only once.
                if not flag:
                    d[item] = min(price, d.get(item, INF))
                    flag = 1
                # and price taken as 0 for rest of the items.
                else:
                    d[item] = min(0, d.get(item, INF))

    winner = {'id': None, 'price': INF}

    for hotel_id, d in data.items():
        if all(k in d for k in keys):
            # If all items were found in current Hotel then find
            # their sum, compare it with 'combo' or inf and then
            # finally the minimum of them is compared with winner['price']
            min_ = min(sum(d[k] for k in keys), d.get('combo', INF))
            if min_ < winner['price']:
                winner['id'] = hotel_id
                winner['price'] = min_
        elif 'combo' in d:
            # If not all keys were present but 'combo' was there then
            # compare its value with winner['price'] and modify
            # winner appropriately.
            if d['combo'] < winner['price']:
                winner['id'] = hotel_id
                winner['price'] = d['combo']

    if winner['id'] is not None:
        print winner.get('id'), winner.get('price')



