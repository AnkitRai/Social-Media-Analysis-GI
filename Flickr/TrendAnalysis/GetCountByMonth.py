import urllib
import urllib2
import json
import pandas as pd
import datetime

def count_post(dateupload, datetaken):
	if(dateupload in time_distribution['date_upload']):
		idx = time_distribution['date_upload'].index(dateupload)
		time_distribution['post'][idx] += 1

	else:
		time_distribution['date_upload'].append(dateupload)
		time_distribution['date_taken'].append(datetaken)
		time_distribution['post'].append(1)
		time_distribution['fav'].append(0)
		time_distribution['cmt'].append(0)


def count_fav(photo_id):
	#Use flickr.photos.getFavorites to get date of favs

	apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.getFavorites&api_key=25541b9c40a64b6fac3cc21145bc7400&photo_id='+photo_id+'&format=json&nojsoncallback=1'
	urllib.urlretrieve(apiurl, 'fav.json')
	with open('fav.json') as data_file:
		fav = json.load(data_file)

	for term in fav['photo']['person']:
		if term.get('favedate'):
			fav_date = term['favedate']
			fav_date = datetime.datetime.fromtimestamp(
				int(fav_date)
			).strftime('%Y-%m-%d %H:%M:%S')
			fav_date = fav_date[0:7]

			if(fav_date in time_distribution['date_upload']):
				idx = time_distribution['date_upload'].index(fav_date)
				time_distribution['fav'][idx] += 1

			else:
				time_distribution['date_upload'].append(fav_date)
				time_distribution['date_taken'].append('')
				time_distribution['fav'].append(1)
				time_distribution['post'].append(0)
				time_distribution['cmt'].append(0)



def count_cmt(photo_id):
	#Use flickr.comments.getList to get date of favs

	apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.comments.getList&api_key=25541b9c40a64b6fac3cc21145bc7400&photo_id='+photo_id+'&format=json&nojsoncallback=1'
	urllib.urlretrieve(apiurl, 'cmt.json')
	with open('cmt.json') as data_file:
		cmt = json.load(data_file)

	if cmt['comments'].get('comment'):
		for term in cmt['comments']['comment']:
			cmt_date = term['datecreate']
			cmt_date = datetime.datetime.fromtimestamp(
				int(cmt_date)
			).strftime('%Y-%m-%d %H:%M:%S')
			cmt_date = cmt_date[0:7]

			if(cmt_date in time_distribution['date_upload']):
				idx = time_distribution['date_upload'].index(cmt_date)
				time_distribution['cmt'][idx] += 1

			else:
				time_distribution['date_upload'].append(cmt_date)
				time_distribution['date_taken'].append('')
				time_distribution['cmt'].append(1)
				time_distribution['fav'].append(0)
				time_distribution['post'].append(0)


'''
def count_geo(photo_id):
	apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key=25541b9c40a64b6fac3cc21145bc7400&photo_id='+photo_id+'&format=json&nojsoncallback=1'
	req = urllib2.Request(apiurl)
	f = urllib2.urlopen(req)
	post = json.loads(f.read())
	place = post['photo']['owner']['location']
	if(place.endswith('U.S.A.')):
		if(place in city_distribution['city']):
				idx = city_distribution['city'].index(place)
				city_distribution['count'][idx] += 1

		else:
			city_distribution['city'].append(place)
			city_distribution['count'].append(1)
'''

def count_geo(photo_id, dateupload, datetaken):
	'''
	{ "stat": "fail", "code": 2, "message": "Photo has no location information." }
	{ "photo": { "id": "16612022625", 
    "location": { "latitude": -12.551882, "longitude": -41.288681, "accuracy": 10, "context": 0, 
      "county": { "_content": "Lencois", "place_id": "DegViWBQUL9FPvBk5g", "woeid": "12578461" }, 
      "region": { "_content": "Bahia", "place_id": "HTlt5udTUb7fwhxO", "woeid": "2344848" }, 
      "country": { "_content": "Brazil", "place_id": "xQfoS31TUb6eduaTWQ", "woeid": "23424768" }, "place_id": "DegViWBQUL9FPvBk5g", "woeid": "12578461" } }, "stat": "ok" }
    '''
      
	apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.geo.getLocation&api_key=25541b9c40a64b6fac3cc21145bc7400&photo_id='+photo_id+'&format=json&nojsoncallback=1'
	req = urllib2.Request(apiurl)
	f = urllib2.urlopen(req)
	post = json.loads(f.read())
	#print post
	if post.get('photo'):
		if post['photo']['location'].get('country'):
			country = post['photo']['location']['country']['_content']
			if(country == "United States"):
				#But the accuracy for the geo info is different 
				geo = (post['photo']['location']['latitude'], post['photo']['location']['longitude']) 	#I mean to wrap geo as a tuple, but become list instead
				if post['photo']['location'].get('region'):
					region = post['photo']['location']['region']['_content']
				else:
					region = ''

				if(geo in geo_distribution['geo']):
					idx = geo_distribution['geo'].index(geo)
					geo_distribution['count'][idx] += 1

				else:
					geo_distribution['geo'].append(geo)
					geo_distribution['count'].append(1)
					geo_distribution['region'].append(region)

				#Same geo info ganrantees same region, but not vice versa

				if(region in geo_heatmap['region']):
					idx = geo_heatmap['region'].index(region)
					geo_heatmap['count'][idx] += 1

				else:
					geo_heatmap['region'].append(region)
					geo_heatmap['count'].append(1)

				geo_timestamp['geo'].append(geo)
				geo_timestamp['region'].append(region)
				geo_timestamp['photo_id'].append(photo_id)
				geo_timestamp['date_upload'].append(dateupload)
				geo_timestamp['date_taken'].append(datetaken)
					


def main():
	# GI = [(text, tag, tagmode)]
	#GI = [('raingarden', '-people', 'all') , ('bioswale', '-people', 'all'), ('tree%20street%20city', 'tree%2Ctrees', 'or')]
	#GI = [('wetland', '+landscape%2C+wetland', 'all'), ('stormwater','stormwater%2C+-fire%2C+-light', 'all'), ('flooding+street','flood', 'all'), ('retention', '+basin%2C+pond', 'or')]
	#GI = [('stormwater','stormwater%2C+-fire%2C+-light', 'all'), ('flooding+street','flood', 'all'), ('retention', '+basin%2C+pond', 'or'), ('%22green+infrastructure%22', '', '')]
	GI = [('tree%20street%20city', '+tree%2C+trees', 'or')]
	#For now wetland has some problems

	for term in GI:
		
		print('Now crawling '+ term[0])
		
		global time_distribution
		time_distribution = {}
		time_distribution['date_upload'] = []
		time_distribution['date_taken'] = []
		time_distribution['post'] = []
		time_distribution['fav'] = []
		time_distribution['cmt'] = []
		#time_distribution['total'] = []


		global geo_distribution
		geo_distribution = {}
		geo_distribution['geo'] = []
		geo_distribution['region'] = []
		geo_distribution['count'] = []

		global geo_heatmap
		geo_heatmap = {}
		geo_heatmap['region'] = []
		geo_heatmap['count'] = []

		global geo_timestamp
		geo_timestamp = {}
		geo_timestamp['geo'] = []
		geo_timestamp['region'] = []
		geo_timestamp['photo_id'] = []
		geo_timestamp['date_upload'] = []
		geo_timestamp['date_taken'] = []

		pagenumber = 1
		ctr = 0

		while(1):
			print('  Page '+str(pagenumber)+' ...')

			#has_geo=1 for geo info 
			if term[0] == '':
				apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=25541b9c40a64b6fac3cc21145bc7400&tags='+term[1]+'&tag_mode='+term[2]+'&sort=relevance&privacy_filter=1&extras=date_taken%2Cdate_upload&per_page=500&&page='+str(pagenumber)+'&format=json&nojsoncallback=1'
			elif term[1] == '':
				apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=25541b9c40a64b6fac3cc21145bc7400&text='+term[0]+'&sort=relevance&privacy_filter=1&extras=date_taken%2Cdate_upload&per_page=500&&page='+str(pagenumber)+'&format=json&nojsoncallback=1'
			else:
				apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=25541b9c40a64b6fac3cc21145bc7400&tags='+term[1]+'&tag_mode='+term[2]+'&text='+term[0]+'&sort=relevance&privacy_filter=1&extras=date_taken%2Cdate_upload&per_page=500&&page='+str(pagenumber)+'&format=json&nojsoncallback=1'	

			req = urllib2.Request(apiurl)
			f = urllib2.urlopen(req)
			data = json.loads(f.read())		
			
			for photo in data['photos']['photo']:
				global photo_id
				photo_id = photo['id']
				dateupload = datetime.datetime.fromtimestamp(int(photo['dateupload'])).strftime('%Y-%m-%d %H:%M:%S')
				dateupload = dateupload[0:7]
				datetaken = photo['datetaken'][0:7]

				count_post(dateupload, datetaken)
				count_fav(photo_id)
				count_cmt(photo_id)				

				count_geo(photo_id, dateupload, datetaken)

				ctr += 1
				if(ctr%200 == 0): print(ctr)
				#if(ctr == 50): break

			#print(time_distribution)			


			if(pagenumber == data['photos']['pages']): 
				print(term[0]+' has been crawled!')
				with open(term[0]+'_time'+".json", "w") as outfile1:
					json.dump(time_distribution, outfile1)
				with open(term[0]+'_geo'+".json", "w") as outfile2:
					json.dump(geo_distribution, outfile2)				
				with open(term[0]+'_heatmap'+".json", "w") as outfile3:
					json.dump(geo_heatmap, outfile3)				
				with open(term[0]+'_timestamp'+".json", "w") as outfile4:
					json.dump(geo_timestamp, outfile4)
				break

			'''
			#dump for every page crawled to avoid network error
			with open('geo_'+term[0]+".json", "w") as outfile:
				json.dump(geo_distribution, outfile)
			with open('time_'+term[0]+'.json', 'w') as outfile:
				json.dump(time_distribution, outfile)
			'''
			pagenumber += 1 
		

		
		print('Now disposing '+ term[0])
		with open(term[0]+'_time'+".json") as infile1:
			data = json.load(infile1)
			df = pd.DataFrame.from_dict(data)
			df.to_csv('Flickr_time/'+term[0]+'_time.csv')

		with open(term[0]+'_geo'+".json") as infile2:
			data = json.load(infile2)
			df = pd.DataFrame.from_dict(data)
			df.to_csv('Flickr_geo/'+term[0]+'_geo.csv')

		with open(term[0]+'_heatmap'+".json") as infile3:
			data = json.load(infile3)
			df = pd.DataFrame.from_dict(data)
			df.to_csv('Flickr_geo/'+term[0]+'_heatmap.csv')

		with open(term[0]+'_timestamp'+".json") as infile4:
			data = json.load(infile4)
			df = pd.DataFrame.from_dict(data)
			df.to_csv('Flickr_geo/'+term[0]+'_timestamp.csv')

		
		

if __name__ == '__main__':
    main()
			