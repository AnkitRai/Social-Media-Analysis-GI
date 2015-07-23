'''
The data is expected to be stored in a 2D data structure, where 
the first index is over features and the second is over samples.

data = {'img': ['1.jpg', '2.jpg', '3.jpg'],
		'comment': (['Great!', 'Nice shot', 'Awsome'],['ah, good']),
		'view': [301, 222, 256],
		'fav': [2, 3, 4],
		'cmt': [11, 15, 16]
}

'''

import os
from os import listdir
import sys 
import json

#Append comment list from *_comment.txt
def append_comment(base):
	comment_list = []	
	with open(path+'/'+base+'_comment.txt', 'r') as input:
		for line in input:
			comment_list.append(line)
	data['comment'].append(comment_list)

#Append view, fav, and cmt list following the order from *_stat.txt 
def append_stat(base):
	with open(path+'/'+base+'_stat.txt', 'r') as input:
		data['view'].append(input.readline().rstrip('\n'))
		data['fav'].append(input.readline().rstrip('\n'))
		data['cmt'].append(input.readline().rstrip('\n'))

import re

def tryint(s):
    try:
        return int(s)
    except:
        return s
     
def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]


def main(paths):

	#paths = ['rain+garden_clean', 'bioswale_clean']

	#Initialize data structure by the format defined at the top
	global data
	data = {}
	data['img'] = []
	data['comment'] = []
	data['view'] = []
	data['fav'] = []
	data['cmt'] = []
	data['label'] = []

	label = 1 
	
	for item in paths:
		global path
		path = item
		
		file_list = listdir(path)
		#Sort the given list in the way that humans expect.
		file_list.sort(key=alphanum_key)
		#print(file_list)

		#Build the dict from each file
		
		for item in file_list:
			if item.endswith('.jpg'):
				data['img'].append(item)
				#Get rid of the extension to better refer to for other type of files
				#i.e. 1.jpg -> 1
				base = os.path.splitext(item)[0]

				append_comment(base)
				
				append_stat(base)

				data['label'].append(str(label))

		label += 1

	#convert list to tuple
	#data['comment'] = tuple(data['comment'])
	#print(data)

	#convert to json for visualization 
	with open("Data.json", "w") as outfile:
		json.dump(data, outfile)

	return data

if __name__ == '__main__':
	main()
