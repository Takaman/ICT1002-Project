import pandas as pd
import ftfy
import datetime as dt
import re
from langdetect import detect

#Concatenation of both reddit and twitter files(with same column names and file names provided in CSV)
df = pd.concat(
    map(pd.read_csv,['Redditdata.csv','covidsgtweets4.csv']))
df['date']=pd.to_datetime(df.date)
redditandtwitter = df.sort_values(by=['date'], ascending= False, ignore_index=True)
redditandtwitter.to_csv('redditandtweets2.csv')


#Reading each tweet/comment and fixing unicode errors FTFY and Detect
commentsDf = pd.read_csv("redditandtweetsv2.csv")
#Loops every element in body and replacing it with the fixed version
for x in commentsDf["body"]: 
    commentsDf["body"]= commentsDf["body"].replace(x, ftfy.fix_text(x))
    try:
        if detect(x) != 'en':
            commentsDf["body"] = commentsDf["body"].replace(x,"")
    except: #Catches the error in case that it cannot detect a suitable language
        commentsDf["body"] = commentsDf["body"].replace(x,"")
        commentsDf["body"].replace("\\b[0-9]+\\b","")
        
nanValue = float("NaN")
commentsDf.replace("",nanValue, inplace=True)
commentsDf.dropna(subset=["body"],inplace=True)
commentsDf.to_csv("redditandtweetsv3")
