#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#mines
import lib

#built out
import logging
logging.basicConfig(level=logging.DEBUG)
from bs4 import BeautifulSoup
import requests
import requests_cache
#monkey patching... FIXME use CacheControl
requests_cache.install_cache('tmp/cache', backend='sqlite', expire_after=12*3600)
#import datetime

#get config
config = lib.config

def get_films(url):
    logging.debug("Get Films from %s", url)
    r = requests.get(url)
    t = r.text
    soup = BeautifulSoup(t, 'html.parser')
    links = soup.find_all('a')
    films = {}
    for l in links :
        u = l.get('href')
        u = u.split('#')[0]
        if "/film" in u :
            films[u] = {"url" :u }
    return(films)

def get_film(url):
    film = {"url" : url, "cines" : []}
    logging.debug("Parse film datas from %s", url)
    r = requests.get(url)
    t = r.text
    soup = BeautifulSoup(t, 'html.parser')
    cines = soup.find_all('div', class_="cinema-result")
    for c in cines :
        cine = {"seances" : []}
        cine['cinename'] = c.find(class_='cinemaTitle').find("h3").text
        cine['url'] = c.find(class_='cinemaTitle').find("a").get('href')
        seances = c.find_all(class_="session-date")
        for s in seances :
            ladate = s.find(class_="sessionDate").text
            lheure = s.find(class_="time").text
            cine['seances'].append({"date" : ladate, "heure": lheure})
        film["cines"].append(cine)

    return(film)

if __name__ == "__main__":
    #print(config)
    url = config['cip']['url']
    prefix = config['cip']['prefix']
    films = get_films(url)
    for f in films :
        films[f] = get_film(prefix+f)
    print(films)
