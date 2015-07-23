from os import listdir
import os
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

def main():
	
	#Reindexed the collected data by continued natural number
	#Because manually deleting irrelevant files leaves gaps in index
	ctr=1

	paths = ['other/tree%20street%20city/', 'other/raingarden/', 'other/bioswale/']
	for path in paths:
		file_list = listdir(path)

		#Sort the given list in the way that humans expect.
		file_list.sort(key=alphanum_key)

		print(path)



		for item in file_list:
			if item.endswith('.jpg'):
				base = os.path.splitext(item)[0]
				#print(base)
				os.rename(path+item, path+str(ctr)+'.jpg')
				os.rename(path+base+'.json', path+str(ctr)+'.json')
				os.rename(path+base+'_comment.txt', path+str(ctr)+'_comment.txt')
				os.rename(path+base+'_stat.txt', path+str(ctr)+'_stat.txt')
				ctr += 1
				print(ctr)

	print('Done! '+str(ctr)+' files reindexeded')


if __name__ == '__main__':
    main()
	#Then it gives me one more last 3 but it works for a small number??
