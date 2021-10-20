import pandas as pd
import ftfy
import datetime as dt

#Concatenation of both files (with same column names and file names provided)
df = pd.concat(
    map(pd.read_csv,['OfficialReddit1.csv','covidsgtweets4.csv']))
df['date']=pd.to_datetime(df.date)
redditandtwitter = df.sort_values(by=['date'], ascending= False, ignore_index=True)
redditandtwitter.to_csv('redditandtweets2')


#Reading each tweet/comment and fixing unicode errors FTFY
comments_df = pd.read_csv("redditandtweets2.csv")
#Loops every element in body and replacing it with the fixed version
for x in comments_df["body"]: 
    comments_df["body"]= comments_df["body"].replace(x, ftfy.fix_text(x))

comments_df.to_csv("redditandtweetsv2")
