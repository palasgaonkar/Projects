#!/usr/bin/env python
# -*- coding: ascii -*-

import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(msecs)-3d::%(filename)s::%(message)s',
                    datefmt='%Y%m%d %H%M%S',
                    filename='invoize.log',
                    filemode='a')