'''for any queries contact - rai5@illinois.edu'''
__author__ = 'ankit'
import json
import os.path
import nltk
from nltk.tag import pos_tag
import pprint
import pandas as pd
import time
from nltk.corpus import stopwords

def tweettotable(input_tweets,input_table): #program does nothing as written
    tweets=[]
    with open(input_tweets) as f1:
        for line in f1:
            tweets.append(json.loads(line))
    if not os.path.isfile(input_table):
        f2 = open(input_table, 'w')
        for t in range(len(tweets)):
            if not ('retweeted_status' in tweets[t].keys()):
                ascii_text= ''.join([i if ord(i) < 128 else ' ' for i in tweets[t]['text']])
                f2.write('\t'.join([tweets[t]['created_at'], 
                                ascii_text.replace('\n','').replace('\r','').encode('ascii'),'\n']))    
    else:
        print 'the table file ',input_table,' already exists'
# first unzip the large json file in data folder
# this takes a few minutes
tweettotable('data/tweets_large.json','data/input_table.csv')

# create dataframe 
input_table='data/input_table.csv'
df=pd.read_csv(input_table,sep='\t',encoding='latin-1',header=None, names=['time','text','non'])
df.drop('non',axis=1,inplace=True)
df['one']=1
df['datetime']=df.time.apply(lambda x: time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(x,'%a %b %d %H:%M:%S +0000 %Y')))

# remove rubbish words
rubbish = ['http','RT','@','#','!',':','.','-',',','//t','/but','one','via','\'s','(',')','?',';','&','"','n\'t','\'m']
for item in rubbish:
    df.text = df.text.str.replace(item,'')
df['text'] = df.text.str.lower()    
all_text = ' '.join(df.text.tolist())

# tokenize 
token_text= nltk.word_tokenize(all_text)

# remove stop words
stop=stopwords.words('english')
text_nonstop=[]
for word in token_text: # iterate over word_list
    if not (word in stop): 
        text_nonstop.append(word)    

fdist=nltk.FreqDist(text_nonstop)
top=sorted(fdist,key=fdist.get,reverse=True)[:7]

for key in top:    
    df[key]= df.text.apply(lambda x: key in x)

df[top].resample('H',sum).plot(figsize=(15,10), title='Top Keywords')
