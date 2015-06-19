import urllib
import json
from pprint import pprint
import os
import sys

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

def get_stat(photo_id, output):
	#favs
	#The api for flickr.favorites.getList
	apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.getFavorites&api_key=25541b9c40a64b6fac3cc21145bc7400&photo_id='+photo_id+'&format=json&nojsoncallback=1'
	urllib.urlretrieve(apiurl, newpath+'/'+str(ctr)+'.json')
	with open(newpath+'/'+str(ctr)+'.json') as data_file:
		data = json.load(data_file)

	#parse json file to get the 'total' part
	output.write(data['photo']['total']+'\n')

	#comments
	#The api for flickr.photos.getInfo
	apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key=25541b9c40a64b6fac3cc21145bc7400&photo_id='+photo_id+'&format=json&nojsoncallback=1'
	urllib.urlretrieve(apiurl, newpath+'/'+str(ctr)+'.json')
	with open(newpath+'/'+str(ctr)+'.json') as data_file:
		data = json.load(data_file)

	#parse json file to get the 'total' part
	output.write(data['photo']['comments']['_content']+'\n')

	output.close()

def done():
	sys.exit()

def main():
	'''
	Trys for different searching key words goes in here
	'''
	#text = ['green+roof','%22raingarden%22','permeable+pavement','bioswale','green+corridor']
	#text = ['permeable+court', '%22green%20wall%22%20living%20%20architecture', '%22street+tree%22+%22green+infrastructure%22', 'rainwater+storage', '%22urban%20landscape%22%20park']
	text = ['rain+garden'] 
	stopword = '-droplet%2C-drop%2C-leaves'  #Get rid of the tags better not appear
	#not work: tags = ['rain+garden%2Cgreen+infrastructure']
	#tags = ['bioswale%2C-text']

	
	global ctr 
	ctr = 1	

	pagenumber = 1
	while(1):
		for term in text:
			#apiurl_withtag = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=25541b9c40a64b6fac3cc21145bc7400&tags='+term+'&text='+term+'&sort=relevance&privacy_filter=1&content_type=1&extras=views&per_page=500&format=json&nojsoncallback=1'
			apiurl = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=25541b9c40a64b6fac3cc21145bc7400&text='+term+'&tags='+stopword+'&tag_mode=all&sort=relevance&privacy_filter=1&extras=views&per_page=500&&page='+str(pagenumber)+'&format=json&nojsoncallback=1'
			urllib.urlretrieve(apiurl, term+str(pagenumber)+'.json')

			with open(term+str(pagenumber)+'.json') as data_file:
				data = json.load(data_file)

			global newpath 
			newpath = term#+'_clean' 
			if not os.path.exists(newpath): os.makedirs(newpath)

			for photo in data['photos']['photo']:
				if(int(photo['views'])>250):
					#First retrive the image and store it
					keys = [photo['farm'],photo['server'],photo['id'],photo['secret']]

					#see how to map photo to url: https://www.flickr.com/services/api/misc.urls.html
					imgurl = 'https://farm'+str(keys[0])+'.staticflickr.com/'+str(keys[1])+'/'+str(keys[2])+'_'+keys[3]+'_z.jpg'
					urllib.urlretrieve(imgurl, newpath+'/'+str(ctr)+'.jpg')

					#Then retrive its corrresponding comments 
					get_comments(photo['id'],)

					#Then retrive its corrresponding stats: # view, favs and comments
					output = open(newpath+'/'+str(ctr)+'_stat.txt', 'wb')

					#view
					output.write(photo['views']+'\n')
					get_stat(photo['id'], output)

					#Do this until we get 350 data
					if(ctr == 350): done()
					ctr += 1
			    		

			pagenumber += 1 



if __name__ == '__main__':
    main()

'''
Difficult to retrive: photo with people in it, which conveys the idea of green economy / green community

https://www.flickr.com/search/?text=%22street%20tree%22%20%22green%20infrastructure%22
https://www.flickr.com/search/?text=%22green%20wall%22%20living%20%20architecture
https://www.flickr.com/search/?text=%22urban%20landscape%22%20park
'''