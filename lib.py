#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import json
import urllib.parse
import pathlib
import requests
import logging
from bs4 import BeautifulSoup, UnicodeDammit
import random

def get_json(fname, k = None):
    with open(fname) as f :
        d = json.load(f)
    if k == None :
        return d
    else :
        return d[k]

config = get_json('config.json')

def strip_html(html):
    soup = BeautifulSoup(html, "lxml")
    return soup.getText()

def is_url(u):
    return u[0:4] == 'http'

