import requests
from bs4 import BeautifulSoup
import cgi
import urlparse
import urllib
import re
from operator import itemgetter
#Add proxies if required (normally we have to if we are at workplace ;))
'''
PROXIES = {
  'http': 'http://rchoubey:Sherlock%4013@20.198.58.158:6588',
  'https': 'http://rchoubey:Sherlock%4013@20.198.64.13:6588',
}
'''
PROXIES = {}

SEARCH_URL = 'http://www.coupondunia.in/search/?q=%s'
STORE_URL = 'http://www.coupondunia.in/%s'

# STORE_AFF = [
# { 'id':'trendin', 'aff':['utm_source', 'utm_medium', 'utm_campaign']},
# { 'id':'lenscart', 'aff':['utm_source']},
# { 'id':'homeshop18', 'aff':['utm_source', 'utm_medium', 'utm_campaign']},
# { 'id':'indiatimeshoping', 'aff':['utm_source', 'utm_medium']},
# { 'id':'healthkart', 'aff':['utm_source', 'utm_medium', 'utm_campaign']},
# { 'id':'foodpanda', 'aff':['utm_source', 'utm_medium', 'utm_campaign']},
# { 'id':'goibibo', 'aff':['utm_source', 'utm_medium', 'utm_campaign', 'utm_content']},
# { 'id':'snapdeal', 'aff':['utm_source', 'utm_campaign']},
# { 'id':'amazon', 'aff':['tag']},
# { 'id':'flipkart', 'aff':['affid', 'AffExtParam1']},
# { 'id':'ebay', 'aff':['aff_source']},
# { 'id':'fabfurnish', 'aff':['utm_source', 'utm_medium', 'utm_term', 'utm_content', 'utm_campaign']},
# { 'id':'pepperfry', 'aff':['utm_source', 'utm_medium', 'utm_campaign']},
# { 'id':'dominos', 'aff':['src']},
# { 'id':'jabong', 'aff':['subid']},
# { 'id':'shopclues', 'aff':['utm_source']},
# { 'id':'zovi', 'aff':['ccode', 'utm_source', 'utm_medium', 'utm_content', 'utm_campaign']},
# { 'id':'zivame', 'aff':['utm_source']},
# { 'id':'vistaprint', 'aff':['GP', 'GPS', 'GNF']},
# { 'id':'myntra', 'aff':['utm_source', 'utm_medium']}]

STORE_AFF = [
{ 'id':'babyoye', 'aff':'aff_id'},
{ 'id':'expedia', 'aff':'affcid'},
{ 'id':'fabfurnish', 'aff':'wt_af'},
{ 'id':'greendust', 'aff':'src'},
{ 'id':'naaptol', 'aff':'ntpromoid'},
{ 'id':'rediffshopping', 'aff':'sc_cid'},
{ 'id':'vistaprint', 'aff':'GP'},
{ 'id':'yatra', 'aff':'ci'},
{ 'id':'zovi', 'aff':'ccode'},
{ 'id':'bookadda', 'aff':'affiliateID'},
{ 'id':'saholic', 'aff':'afid'},
{ 'id':'flipkart', 'aff':'affid'},
{ 'id':'infibeam', 'aff':'trackId'},
{ 'id':'fetise', 'aff':'ref'},
{ 'id':'firstcry', 'aff':'ref'},
{ 'id':'hotels', 'aff':'rffrid'},
{ 'id':'dominos', 'aff':'src'},
{ 'id':'yepme', 'aff':'PromoSiteID'},
{ 'id':'groupon', 'aff':'CID'},
{ 'id':'makemytrip', 'aff':'cmp'},
{ 'id':'chumbak', 'aff':'utm_campaign'},
{ 'id':'booking.com', 'aff':'aid'},
{ 'id':'ebay', 'aff':'aff_source'},
{ 'id':'amazon', 'aff':'tag'},
{ 'id':'miraistore', 'aff':'msref'},
{ 'id':'floristsinindia', 'aff':'tracking'},
{ 'id':'gobol', 'aff':'acc'},
{ 'id':'qatar', 'aff':'CID'},
{ 'id':'goibibo', 'aff':'aff'}
]


RESULT_COUNT = 10

def extractSearchTerm(input):
	unwanted = ['OF', 'FOR', 'IS', 'WAS', 'RS', '$', 'AND', '&']
	a_input = input.upper().split(' ')
	a_output = [];
	for i in a_input:
		if i in unwanted:
			continue
		else:
			a_output.append(i)
	return ' '.join(a_output)
	
def getProductOffersFromCD(q):
	rs = requests.get(SEARCH_URL % q, proxies=PROXIES)
	soup = BeautifulSoup(rs.text)
	#with open('response.txt', 'a') as f:
	#	f.write(rs.text.encode('utf-8'))
	a_items = []
	i = 0
	for item in soup.select('div.offer-big'):
		i = i + 1
		if i > RESULT_COUNT:
			break
		item_lnk = item.find('div',{'class': 'btn btn-cd btn-deal coupon-click'})
		item_title = item_lnk.get_text().strip()
		item_href = requests.get(item_lnk['data-url'], allow_redirects=False).headers['location']		
		a_items.append({'title': item_title, 'href': item_href})
			#id = item.find('div',{'class':'coupon altCoupon'})['id']
	
	return a_items
	
def getStoreOffersFromCD(q):
	rs = requests.get(STORE_URL % q, proxies=PROXIES)
	soup = BeautifulSoup(rs.text, 'html.parser')
	#with open('response.txt', 'a') as f:
	#	f.write(rs.text.encode('utf-8'))
	item_selector = 'div.coupon-big'
	deal_coupon_lnk_class = re.compile('get-code')
	title_class = re.compile('dummy-anchor')
	coupon_class = 'div.coupon-code_new'
	a_items = []
	i = 0
	for item in soup.select(item_selector):
		i = i + 1
		if i > RESULT_COUNT:
			break
				
		item_type = ''
		coupon_code	= ''
		if item.find('div',{'class': deal_coupon_lnk_class}):
			item_lnk = item.find_all('div',{'class': deal_coupon_lnk_class})[1]
			if 'Activate Deal' in item_lnk.get_text().strip():
				item_type = 'D'
			else:
				item_type = 'C'
				print item_lnk['data-coupon-url']
				rsc = requests.get(item_lnk['data-coupon-url'])
				#with open('response2.txt', 'a') as f:
				#	f.write(rsc.text.encode('utf-8'))
				soupc = BeautifulSoup(rsc.text, 'html.parser')
				coupon_code = soupc.select(coupon_class)[0].get_text().strip()
				#print coupon_code
			#print item_type
		else:
			continue
			
		item_href = checkMetaRedirect(requests.get(item_lnk['data-coupon-url'], allow_redirects=True).url)
		item_title = item.find('a',{'class': title_class}).get_text().strip()
		
		stripped_href = stripURL(item_href, q)
		
		if len(stripped_href) > 0:
			a_items.append({'title': item_title, 'stripped': stripped_href, 'type': item_type, 'coupon':coupon_code})
		else:
			continue
			#id = item.find('div',{'class':'coupon altCoupon'})['id']
	
	return sorted(a_items, key=itemgetter('type'))
	

def checkMetaRedirect(url):
	soup  = BeautifulSoup(requests.get(url).text, 'html.parser')
	result=soup.find("meta",attrs={"http-equiv":"Refresh"})
	if result:
		wait,text=result["content"].split(";")
		if text.encode('utf-8').strip().lower().startswith("url="):
			url=text[5:]
			return url
	return url
	
def stripURL(item_href, q):
	#special case for ibibo
	if 'ibibo'.upper() in q.upper():
		return 'http://www.goibibo.com/'		
		
	# if 'coupondunia' in item_href:
		# if 'url' in item_href_qs.keys():
			# item_href = item_href_qs['url'][0]
			# redo = True
		# else:
			# return ''
	
	# if 'jasper' in item_href:
		# if 'url' in item_href_qs.keys():
			# item_href = item_href_qs['url'][0]
			# redo = True
		# else:
			# return ''
	#Commented old logic of selective filtering of query string	
	# if redo:
		# item_href_url = urlparse.urlparse(item_href)
		# item_href_qs = cgi.parse_qs(item_href_url[4])
	
	
	# curr_aff = {}		
	# for x in STORE_AFF:
		# if x['id'].upper() == q.upper():
			# curr_aff = x
			# break
	
	# if 'aff' in curr_aff.keys():
		# for y in curr_aff['aff']:
			# if y in item_href_qs.keys():
				# del(item_href_qs[y])
	
	# return urlparse.urlunparse((item_href_url[0],item_href_url[1],item_href_url[2],item_href_url[3],urllib.urlencode(item_href_qs),item_href_url[5]))
	
	#Added new logic of stripping everything after certain querystring
	curr_aff = {}		
	for x in STORE_AFF:
		if x['id'].upper() == q.upper():
			curr_aff = x
			break
	
	
	stripped_href = item_href
	if 'aff' in curr_aff.keys():
		if (curr_aff['aff'] + '=') in item_href:
			stripped_href = item_href[:item_href.index(curr_aff['aff'] + '=')]
			
	if 'utm_' in stripped_href:
		stripped_href = stripped_href[:stripped_href.index('utm_')]
		
	if stripped_href[len(stripped_href)-1:] == '?' or stripped_href[len(stripped_href)-1:] == '&':
		stripped_href = stripped_href[:len(stripped_href)-1]
	
	
	return stripped_href
	
def main():
	q = 'dominos'
	print getStoreOffersFromCD(q)
	
	
if __name__ == '__main__':
	main()
