import urllib
import json
import os
import sys
from os import listdir
import re
from reindex import tryint, alphanum_key


def getctr(newpath):

	file_list = listdir(newpath)
	file_list.sort(key=alphanum_key)

	if(file_list[-1] == '.DS_Store'):
		return int(re.sub("[^A-Z\d]", "", re.search("^[^_]*", file_list[-2]).group(0).upper())) + 1
	else:
		return int(re.sub("[^A-Z\d]", "", re.search("^[^_]*", file_list[-1]).group(0).upper())) + 1


def get_comments(photo_id):
	#The api for flickr.photos.comments.getList
	apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.comments.getList&api_key=25541b9c40a64b6fac3cc21145bc7400&photo_id='+photo_id+'&format=json&nojsoncallback=1'
	urllib.urlretrieve(apiurl, newpath+'/'+str(ctr)+'.json')
	with open(newpath+'/'+str(ctr)+'.json') as data_file:
		data = json.load(data_file)

	output = open(newpath+'/'+str(ctr)+'_comment.txt', 'w')
	#parse json file to get the 'content' part

	if data['comments'].get('comment'):						#Test if the comment is null
		for content in data['comments']['comment']:
			#Take each comments out and remove noun charecters (like Emoji)
			line = content['_content'].encode('ascii', 'ignore')
			#Some comments have new lines with it. Better to get rid of them
			line = line.replace('\n',' ')
			output.write(line+'\n')

	output.close()


def get_fav(photo_id, output):
	#favs
	#The api for flickr.favorites.getList
	apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.getFavorites&api_key=25541b9c40a64b6fac3cc21145bc7400&photo_id='+photo_id+'&format=json&nojsoncallback=1'
	urllib.urlretrieve(apiurl, newpath+'/'+str(ctr)+'.json')
	with open(newpath+'/'+str(ctr)+'.json') as data_file:
		data = json.load(data_file)

	#parse json file to get the 'total' part
	output.write(data['photo']['total']+'\n')


def done():
	sys.exit()


def main():
	
	#Types of GI
	#1 means searching by text, 2 means searching by tag
	#Sometimes you need both for relatively broad search; how?
	#GI = [('raingarden',1), ('bioswale',2)]#
	GI = [('tree%20street%20city', 1)]	
	global ctr 
	global newpath

	for term in GI:
		newpath = term[0]
		if not os.path.exists(newpath): 
			os.makedirs(newpath)
			ctr = 1
		else: #There should be no empty hanging haunt ghost folder
			ctr = getctr(newpath)
		print('Now crawling '+newpath)

		pagenumber = 1
		#Get the ctr to continue crawling from last time

		while(1):
			print('  Page '+str(pagenumber)+' ...')
			if(term[1] == 1):#&min_taken_date=1433221200 #-flower%2C-people
				apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=25541b9c40a64b6fac3cc21145bc7400&tags=tree%2Ctrees&tag_mode=or&text='+term[0]+'&sort=relevance&privacy_filter=1&extras=date_taken%2Cviews&per_page=500&&page='+str(pagenumber)+'&format=json&nojsoncallback=1'
			if(term[1] == 2):
				apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=25541b9c40a64b6fac3cc21145bc7400&tags='+term[0]+'-people&tag_mode=all&min_taken_date=1433221200&sort=relevance&privacy_filter=1&extras=date_taken%2Cviews&per_page=500&&page='+str(pagenumber)+'&format=json&nojsoncallback=1'
			urllib.urlretrieve(apiurl, term[0]+str(pagenumber)+'.json')

			with open(term[0]+str(pagenumber)+'.json') as data_file:
				data = json.load(data_file)			

			for photo in data['photos']['photo']:

				#The api for flickr.photos.getInfo
				apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key=25541b9c40a64b6fac3cc21145bc7400&photo_id='+photo['id']+'&format=json&nojsoncallback=1'
				urllib.urlretrieve(apiurl, newpath+'/'+str(ctr)+'.json')
				with open(newpath+'/'+str(ctr)+'.json') as data_file:
					cmtdata = json.load(data_file)

				#get comment number 'cn' by parsing json file to get the 'total' part
				cn = int(cmtdata['photo']['comments']['_content'])

				if(cn>0):
					#First retrive the image and store it
					keys = [photo['farm'],photo['server'],photo['id'],photo['secret']]

					#see how to map photo to url: https://www.flickr.com/services/api/misc.urls.html
					imgurl = 'https://farm'+str(keys[0])+'.staticflickr.com/'+str(keys[1])+'/'+str(keys[2])+'_'+keys[3]+'_z.jpg'
					urllib.urlretrieve(imgurl, newpath+'/'+str(ctr)+'.jpg')

					#Then retrive its corrresponding comments 
					get_comments(photo['id'])

					#Then retrive its corrresponding stats: # view, favs and comments
					output = open(newpath+'/'+str(ctr)+'_stat.txt', 'wb')

					#view
					output.write(photo['views']+'\n')
					#fav
					get_fav(photo['id'], output)
					#cmt
					output.write(str(cn)+'\n')

					output.close()

					'''
					#Do this until we get 350 data
					if(ctr == 350): done()
					'''
					ctr += 1
					
			    		
			if(pagenumber == data['photos']['pages']) or (pagenumber>5): 
				print(term[0]+' has been crawled!')
				break
			pagenumber += 1 

		



if __name__ == '__main__':
    main()

'''
Difficult to retrive: photo with people in it, which conveys the idea of green economy / green community

https://www.flickr.com/search/?text=%22street%20tree%22%20%22green%20infrastructure%22
https://www.flickr.com/search/?text=%22green%20wall%22%20living%20%20architecture
https://www.flickr.com/search/?text=%22urban%20landscape%22%20park
'''