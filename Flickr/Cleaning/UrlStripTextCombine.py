from os import listdir
import os
import sys
from HTMLParser import HTMLParser
import re
import shutil


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

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
    GI = ['tree%20street%20city']#['raingarden', 'bioswale']#, 
    for item in GI:
        global path
        path = item+'/'
        global newpath
        newpath = item+'complete/'
        file_list = listdir(path)
        #Sort the given list in the way that humans expect.
        file_list.sort(key=alphanum_key)
        final_file = open(item+'Comment.csv', 'w')
        #csv header
        final_file.write('Comment,Image No.\n')

        irrelevent = ['seen', 'award', 'admin', 'thank you']

        ctr = 0    
        for filename in file_list:
            if(filename.endswith('_comment.txt')):
                ctr += 1
                with open(path+filename, 'r') as input:
                    output = open(newpath+filename, 'w')
                    for line in input:
                        if not any(ir in line.lower() for ir in irrelevent):
                            line = strip_tags(line)
                            line = re.sub(r'.(www|https?).*', '', line)
                            #print(str(ctr)+','+line)
                            output.write(line)
                    
                    output.close()

                #Now output has been striped jibrish 
                output = open(newpath+filename, 'r')
                line_array = output.read().splitlines()
                #Quote each line, and add corresponding image number
                #if(line_array != []):
                for idx in range(0,len(line_array)):
                    final_file.write('\"'+line_array[idx]+'\",\"'+str(ctr)+'\"\n')
                    #final_file.write('\"'+line_array[-1]+'\",\"'+str(ctr)+'\"')

            else:
                shutil.copyfile(path+filename, newpath+filename)
                #ctr += 1
            
            #if(ctr):
                #break

        final_file.close()
        print(ctr+' comments have been collected tide and clean for ' + item + ' !!')

if __name__ == '__main__':
    main()

    '''
    So beautiful!  I am enjoying this whole series of photos.
    Thank you!
    This is beautiful!  You've done a lovely job with your garden.
    I saw your beautiful work in: Ho ammirato questo tuo lavoro in: <img src="https://farm9.staticflickr.com/8185/8127089334_24c1222144_o.jpg" width="235" height="157" alt="icogarden/" /> <a href="https://www.flickr.com/groups/privategarden_">www.flickr.com/groups/privategarden_</a> group 
    '''
