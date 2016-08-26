'''
Each page contains only 20 posts, but they are real posts containing everything
Use next page to fetch the next 20 posts

url = [pagination][next_url]
for post in [data]:
	#test if there are any comment
	if(post[comments][count]):
		#get the comments
		for comment in post[comments][data]:
			cmt_text = comment[text]
			cmt_time = comment[created_time]

	#number of like
	like = post[likes][count]

	#image, and also [width] and [height]
	imgurl = post[images][standard_resolution][url]

	#caption, or title
	caption = post[caption][text]

	#post time, need conversion
	post_time = post[caption][created_time]

	#geo info
	region = post[location][name]
	geo = (post[location][latitude], post[location][longtitude])
'''

import urllib
import urllib2
import requests
import json
import pandas as pd
import datetime
import time
import schedule


class flicker_data(object):
	"""docstring for ClassName"""
	def __init__(self, term):
		# term is the name of GI term we search for / we care
		self.term = term

		# statistics  of a certain photo
		# all params are lists of integers
		self.photo_stat = {'photo_id' = [], 'number_like' = [], 'number_comment' = []}

		# geo info of a certain photo
		self.geo_info = {'photo_id' = [], 'geo' = [], 'region' = [], 'photo_url' = [], 'date_upload' = []}
		
		# poster info of a certain photo
		self.poster_info = {'photo_id' = [], 'poster' = [], 'count' = []}

		# self.geo_heatmap = {'region' = [], 'count' = []}
		

	def get_comments(self, post):
		output = open(self.term+'/comments/'+post['id']+'.txt', 'w')

		for comment in post['comments']['data']:
			#Take each comments out and remove noun charecters (like Emoji)
			line = comment['text'].encode('ascii', 'ignore')
			#Some comments have new lines with it. Better to get rid of them
			line = line.replace('\n',' ')
			output.write(line+'\n')
		
		output.close()


	def get_photo_stat(self, post):
		self.photo_stat['photo_id'].append(post['id'])
		self.photo_stat['number_like'].append(post['likes']['count'])
		self.photo_stat['number_comment'].append(post['comments']['count'])


	def get_image(self, post):
		imgurl = post['images']['standard_resolution']['url']
		urllib.urlretrieve(imgurl, self.term+'/images/'+post['id']+'.jpg')
		#standard solution is 640*640


	def count_geo(self, post):
		#print post['location']
		if post['location'].get('latitude') and post['location'].get('longitude'):
			if post['location'].get('name'):
				self.geo_info['region'].append(post['location']['name'])
			else:
				self.geo_info['region'].append('NA')
			self.geo_info['geo'].append(str(post['location']['latitude']) + ',' + str(post['location']['longitude']))
			self.geo_info['photo_id'].append(post['id'])
			self.geo_info['photo_url'].append(post['images']['standard_resolution']['url'])

			created_time = datetime.datetime.fromtimestamp(
				int(post['created_time'])
			).strftime('%Y-%m-%d %H:%M:%S')
			created_time = created_time[0:7]
			self.geo_info['date_upload'].append(created_time)


	def count_poster(self, post):
		photo_id = post['id']
		poster_id = post['user']['id']
		if(poster_id in self.poster_info['poster']):
			idx = self.poster_info['poster'].index(poster_id)
			self.poster_info['count'][idx] += 1
			self.poster_info['photo_id'][idx].append(photo_id)
		else:
			self.poster_info['poster'].append(poster_id)
			self.poster_info['count'].append(1)
			self.poster_info['photo_id'].append([photo_id])


	def storejson():	
		with open(self.term + '/geo.json', "w") as outfile2:
			json.dump(self.geo_info, outfile2)		

		'''
		with open(self.term + '_heatmap'+".json", "w") as outfile3:
			json.dump(geo_heatmap, outfile3)
		'''

		with open(self.term + '/poster.json', "w") as outfile5:
			json.dump(self.poster_info, outfile5)

		with open(self.term + '/stat.json', "w") as outfile6:
			json.dump(self.photo_stat, outfile6)


	def dispose():
		with open(self.term + '/geo.json') as infile2:
			data = json.load(infile2)
			df = pd.DataFrame.from_dict(data)
			df.to_csv(self.term + '/geo/geo.csv',  index = False, encoding = 'utf-8')

			'''
			writer = pd.ExcelWriter(self.term+'geo/geo_by_state.xlsx')
			for region in df['region'].unique():
				cur = df.loc[df['region'] == region]
				cur = cur[['date_upload', 'geo', 'photo_id', 'photo_url']].reset_index(drop=True)
				cur.to_excel(writer, region, index=False, encoding = 'utf-8')
			writer.save()
			#penpyxl.shared.exc.SheetTitleException: Maximum 31 characters allowed in sheet title
			'''

		'''
		with open(self.term+'_heatmap'+".json") as infile3:
			data = json.load(infile3)
			df = pd.DataFrame.from_dict(data)
			df.to_csv('geo/'+self.term+'_heatmap.csv',  index = False, encoding = 'utf-8')
		'''
		
		with open(self.term+'/poster.json') as infile5:
			data = json.load(infile5)
			df = pd.DataFrame.from_dict(data)
			df.to_csv(self.term+'/stat/poster.csv', index = False, encoding = 'utf-8')


		with open(self.term+'/stat.json') as infile6:
			data = json.load(infile6)
			df = pd.DataFrame.from_dict(data)
			df.to_csv(self.term+'/stat/stat.csv', index = False, encoding = 'utf-8')


def query():
	GI = ['raingarden','bioswale', 'streettree']

	for term in GI:
		print('Now crawling '+ term)
		data = flicker_data(term)
		apiurl = 'https://api.instagram.com/v1/tags/'+term+'/media/recent?access_token=1659794646.1fb234f.97f9c97043b14e8484e343ca31620931'
		pagenumber = 1
		ctr = 0

		while(1):
			print('  Page ' + str(pagenumber) + ' ...')
			time.sleep(1)
			req = urllib2.Request(apiurl)
			f = urllib2.urlopen(req)
			response = json.loads(f.read())	


			for post in response['data']:
				#print post
				if(post['comments']['count'] != 0):
					data.get_comments(post)

				data.get_stat(post)

				data.get_image(post)

				if(post['location'] != 'null' and post['location'] is not None):
					data.count_geo(post)

				data.count_poster(post)

				ctr += 1 
			pagenumber += 1

			if(response['pagination'].get('next_url') is not None):
				apiurl = response['pagination']['next_url']
				if(pagenumber%15 == 0):
					data.storejson()
			else:
				print(term+' has been crawled!')
				data.storejson()
				break

		print('Now disposing '+ term)
		data.dispose()


def main(): 
	# GI terms we care / search queries
	scheudle.every().day.at('04:00').do(query)
	while(1):
		scheudle.run_pending()
		time.sleep(60)


if __name__ == '__main__':
    main()
