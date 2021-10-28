import pandas as pd
import ftfy
import datetime as dt
import re
import sys
from langdetect import detect

if __name__ == "__main__":
    stringinput1 = str(sys.argv[1])
    stringinput2 = str(sys.argv[2])

#Concatenation of both reddit and twitter files(with same column names and file names provided in CSV)
twitterCsv = pd.read_csv(stringinput1)
twitterCsv.rename(columns={"tweet":"body","username":"author"},inplace=True)
redditCsv = pd.read_csv(stringinput2)
df = pd.concat([redditCsv,twitterCsv])

# df = pd.concat(
#     map(pd.read_csv,['testreddit.csv',twitter_csv]))
df['date']=pd.to_datetime(df.date)
redditandtwitter = df.sort_values(by=['date'], ascending= False, ignore_index=False)
redditandtwitter.to_csv('redditandtweets.csv')


#Reading each tweet/comment and fixing unicode errors FTFY and Detect
commentsDf = pd.read_csv("redditandtweets.csv")
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
commentsDf.reset_index(drop=True, inplace=True)
commentsDf.drop(commentsDf.columns[[0,1]],axis=1, inplace=True)
commentsDf.to_csv("redditandtweets.csv")

print("Done, output stored in redditandtweets.csv")
