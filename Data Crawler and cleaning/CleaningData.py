import pandas as pd
import ftfy
import datetime as dt

df = pd.concat(
    map(pd.read_csv,['OfficialReddit1.csv','covidsgtweets4.csv']))

df['date']=pd.to_datetime(df.date)

redditandtwitter = df.sort_values(by=['date'], ascending= False, ignore_index=True)
redditandtwitter.to_csv('redditandtweets2')


comments_df = pd.read_csv("redditandtweets2.csv")

for x in comments_df["body"]:
    comments_df["body"]= comments_df["body"].replace(x, ftfy.fix_text(x))

comments_df.to_csv("redditandtweetsv2")
