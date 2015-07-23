import urllib
import urllib2
import json
import pandas as pd
import datetime

def count_post(photo_id):
	#Use flickr.photos.getInfo to get date of posts

	apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key=25541b9c40a64b6fac3cc21145bc7400&photo_id='+photo_id+'&format=json&nojsoncallback=1'
	urllib.urlretrieve(apiurl, 'post.json')
	with open('post.json') as data_file:
		post = json.load(data_file)

	post_date = post['photo']['dates']['posted']
	post_date = datetime.datetime.fromtimestamp(int(post_date)).strftime('%Y-%m-%d %H:%M:%S')
	post_date = post_date[0:7]

	if(post_date in time_distribution['date']):
		idx = time_distribution['date'].index(post_date)
		time_distribution['post'][idx] += 1

	else:
		time_distribution['date'].append(post_date)
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

			if(fav_date in time_distribution['date']):
				idx = time_distribution['date'].index(fav_date)
				time_distribution['fav'][idx] += 1

			else:
				time_distribution['date'].append(fav_date)
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

			if(cmt_date in time_distribution['date']):
				idx = time_distribution['date'].index(cmt_date)
				time_distribution['cmt'][idx] += 1

			else:
				time_distribution['date'].append(cmt_date)
				time_distribution['cmt'].append(1)
				time_distribution['fav'].append(0)
				time_distribution['post'].append(0)


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


def main():
	# GI = [(text, tag, tagmode)]
	#GI = [('raingarden', '-people', 'all') , ('bioswale', '-people', 'all'), ('tree%20street%20city', 'tree%2Ctrees', 'or')]
	GI = [('tree%20street%20city', 'tree%2Ctrees', 'or')]

	for term in GI:
		'''
		print('Now crawling '+ term[0])
		
		global time_distribution
		time_distribution = {}
		time_distribution['date'] = []
		time_distribution['post'] = []
		time_distribution['fav'] = []
		time_distribution['cmt'] = []
		#time_distribution['total'] = []


		global city_distribution
		city_distribution = {}
		city_distribution['city'] = []
		city_distribution['count'] = []

		pagenumber = 1
		ctr = 0

		while(1):
			print('  Page '+str(pagenumber)+' ...')

			apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=25541b9c40a64b6fac3cc21145bc7400&tags='+term[1]+'&tag_mode='+term[2]+'&text='+term[0]+'&sort=relevance&privacy_filter=1&extras=date_taken%2Cviews&per_page=500&&page='+str(pagenumber)+'&format=json&nojsoncallback=1'

			urllib.urlretrieve(apiurl, term[0]+str(pagenumber)+'_city.json')

			with open(term[0]+str(pagenumber)+'.json') as data_file:
				data = json.load(data_file)			
			
			for photo in data['photos']['photo']:
				global photo_id
				photo_id = photo['id']

				
				count_post(photo_id)
				count_fav(photo_id)
				count_cmt(photo_id)
				

				count_geo(photo_id)

				ctr += 1
				if(ctr%200 == 0): print(ctr)
				#if(ctr == 50): break

			#print(time_distribution)

			with open('city_'+term[0]+".json", "w") as outfile:
				json.dump(city_distribution, outfile)

			with open('data_'+term[0]+'.json', 'w') as outfile:
													json.dump(time_distribution, outfile)


			if(pagenumber == data['photos']['pages']): 
				print(term[0]+' has been crawled!')
				with open('city_'+term[0]+".json", "w") as outfile:
					json.dump(city_distribution, outfile)
				break

			pagenumber += 1 
		

		'''
		print('Now disposing '+ term[0])
		with open('city_'+term[0]+".json") as infile:
			data = json.load(infile)


		df = pd.DataFrame.from_dict(data)
		#df = df.sort(['date'])
		df = df.groupby(["city"]).sum()
		#df['total'] = df.sum(axis=1)
		#print(pd)
		df.to_csv(term[0]+'_region_count.csv')
		
		

if __name__ == '__main__':
    main()
			