# -*- coding: utf-8 -*-
'''
Created on Sep 6, 2017

@author: Promod George
'''

import logging

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    #handler = logging.StreamHandler()
    handler = logging.FileHandler(name+'.log', encoding="utf-8",mode='a', delay=False)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger