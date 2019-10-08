from flask import Flask, request
from flask.ext.restful import Resource, Api
from engine import *
from pymongo import MongoClient


#mongoserver = MongoClient('mongodb://ubuntu@ec2-54-251-184-168.ap-southeast-1.compute.amazonaws.com:27017/test')
mongoserver = MongoClient('mongodb://appuser:appuser@ds061701.mongolab.com:61701/shopsmart')
#mongoserver = MongoClient('mongodb://localhost/ShopSmart')
db = mongoserver['shopsmart']

app2 = Flask(__name__)
api = Api(app2)

todos = {}

class ProductOffers(Resource):
    def get(self, q):
		collectionName = 'store_offers'
		if db[collectionName].find_one({'store':q}):
			a_items = []
			x = db[collectionName].find_one({'store':q})
			print x
			for item in x['offers']:
				a_items.append({'title': item['title'], 'stripped': item['stripped'], 'type': item['type'], 'coupon':item['coupon'], 'version':2})
		return a_items
		
class StoreOffers(Resource):
    def get(self, q):
		collectionName = 'store_offers'
		if db[collectionName].find_one({'store':q}):
			a_items = []
			x = db[collectionName].find_one({'store':q})
			print x
			for item in x['offers']:
				a_items.append({'title': item['title'], 'stripped': item['stripped'], 'type': item['type'], 'coupon':item['coupon'], 'version':2})
			return a_items
		else:
			return getStoreOffersFromCD(extractSearchTerm(q))
			
@app2.route('/test')
def test():
	return '<a href="whatsapp://send?text=Hello%2C%20World!">Send</a>'


api.add_resource(ProductOffers, '/product/<string:q>')
api.add_resource(StoreOffers, '/store/<string:q>')

if __name__ == '__main__':
    app2.run(debug=True)