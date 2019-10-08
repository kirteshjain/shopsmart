#!/usr/bin/env python

from pymongo import MongoClient
from engine import getStoreOffersFromCD
import os
import time
import datetime
from stores import ts
from sys import argv
 
#mongoserver = MongoClient('mongodb://ubuntu@ec2-54-251-184-168.ap-southeast-1.compute.amazonaws.com:27017/test')
mongoserver = MongoClient('mongodb://appuser:appuser@ds061701.mongolab.com:61701/shopsmart')
#mongoserver = MongoClient('mongodb://localhost/ShopSmart')
db = mongoserver['shopsmart']
BOT_LOC = 'D:/ShopSmart'

def main(args):
	if len(args) > 0:
		processStore(args[0])
	else:
		for x in ts:
			q = x['id']
			processStore(q)
		

def processStore(q):
	o = {}
	try:
		logMessage('Fetching: ' + q)
		o = getStoreOffersFromCD(q)
	except Exception as e:
		logMessage(e)
	else:
		logMessage('Inserting: ' + q)
		insertOffers(q, o)
	finally:
		logMessage('Done: ' + q)
		pass

def insertOffers(q, o):
	try:
		collectionName = 'store_offers'
		if not db[collectionName].find_one({'store':q}):			
			db[collectionName].insert({'store':q, 'offers':[]})
		db[collectionName].update({'store':q},{'$addToSet':{'offers':{'$each':o}}})
	except Exception as e:
		logMessage(e)		
			
def logMessage(e):
	try:
		with open('D:/ShopSmart/' + 'log_' + datetime.date.today().isoformat() + '.txt', 'a') as f:
			f.write(time.strftime('%c') + ' : ' + e + '\n')
	except Exception as e_i:
		pass


if __name__ == '__main__':
	main(argv[1:])
