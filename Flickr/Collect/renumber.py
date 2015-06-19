from os import listdir
import os

path = 'bioswale_clean/' 
file_list = listdir(path)

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

    """ Sort the given list in the way that humans expect.
    """
file_list.sort(key=alphanum_key)

#print(file_list)

ctr=0

for item in file_list:
	if item.endswith('.jpg'):
		os.rename(path+item, path+str(ctr/4)+'.jpg')
	elif item.endswith('.json'):
		os.rename(path+item, path+str(ctr/4)+'.json')
	elif item.endswith('_comment.txt'):
		os.rename(path+item, path+str(ctr/4)+'_comment.txt')
	elif item.endswith('_stat.txt'):
		os.rename(path+item, path+str(ctr/4)+'_stat.txt')

	ctr += 1

#Then it gives me one more last 3 but it works for a small number??
