import praw
import pandas as pd
import datetime as dt
import time
import html
import twint
import re
from tkinter import *
from tkinter import ttk
from tkcalendar import *
from pmaw import PushshiftAPI
from twint.run import Search


flag = True
url = "https://www.reddit.com"

def get_date(created):
    return dt.datetime.fromtimestamp(created).date()

def return_utc(tkinterdate):
    date = str(tkinterdate)
    date = dt.datetime.strptime(date,"%Y-%m-%d").timetuple()
    date = int(time.mktime(date))
    return date

def popoutimg(): #Success message popout function when scraping is completed
    popup = Tk()
    popup.geometry('250x150')
    popup.wm_title("!")
    label = ttk.Label(popup, text="Congrats its done!")
    label.pack(side="top",fill="x",pady=30)


def reddit_scraper(topic, subreddit, limit, after, before, csvredditfilename, custom):
    api = PushshiftAPI()
    comments = api.search_comments(q=topic,subreddit=subreddit,limit= limit, after=after, before=before)
    print(f"Retrieved")
    comments_df= pd.DataFrame(comments)
    comments_df.drop(comments_df.columns.difference(custom),1,inplace=True)
    
    _timestamp = comments_df["created_utc"].apply(get_date)
    comments_df = comments_df.assign(created_utc = _timestamp)
    comments_df = comments_df.assign(permalink= url + comments_df["permalink"]) 

    comments_df.body = comments_df.body.apply(html.unescape)
    comments_df.body = comments_df.body.apply(lambda x: re.split('https:\/\/.*', str(x))[0])

    nan_value = float("NaN")
    comments_df.replace("",nan_value, inplace=True)
    comments_df.dropna(subset=["body"],inplace=True)

    final_df = comments_df.sort_values('created_utc', ignore_index= True) #Sort the entire sheet by datetime and then index accordingly
    final_df.to_csv(csvredditfilename)
    popoutimg()
    

def twint_scraper(topic, links ,since, until, limit, custom, output):
    c = twint.Config()
    c.Search = topic
    c.Since = since
    c.Until = until
    c.Store_csv = True
    c.Lang = "en"
    c.Limit = limit
    c.Filter_retweets = True
    c.Links = links
    c.Custom["tweet"] = custom
    c.Output = output
    twint.run.Search(c)
    popoutimg()

def twitterpage():
    def twitterclick():
        twitter_topic = twitterentry.get()
        if variablelink.get() == "Yes":
            links = "exclude"
        else:
            links = "include"
        limit = limits.get()
        custom = []
        columnname = optionList.curselection()
        for i in columnname:
            custom.append(optionList.get(i))
        
        afterdate = str(calafter.get_date())
        beforedate = str(calbefore.get_date())
        filename = csvname.get()
        twint_scraper(twitter_topic, links, afterdate, beforedate,limit, custom,filename) 
    
    
    for labels in list(window.children.values()):
        label = str(labels)
        if label != '.!menu' and label != '.!label':
            labels.destroy()

    Label(window, text="Enter your twitter topic").grid(row=1,column=0,sticky=W)
    Label(window, text="Do you want to exclude links contained in tweets?").grid(row=3,column=0,sticky=W)
    Label(window, text="Enter the limit of your tweets(numbers)").grid(row=5,column=0,sticky=W)
    Label(window, text="Choose all columns you want to be included:").grid(row=7,column=0,sticky=W)
    Label(window, text="From which date?" ).grid(row=9,column=0,sticky=W)
    Label(window,text="To which date?").grid(row=11,column=0,sticky=W)
    Label(window,text="Enter your CSV filename").grid(row=13,column=0,sticky=W)

    twitterentry = Entry(window,width=20,bg="white")
    twitterentry.grid(row=2,column=0,sticky=W)
    variablelink = StringVar(window, "Yes")
    links = OptionMenu(window, variablelink, "Yes","No")
    links.grid(row=4,column=0,sticky=W)
    limits = Entry(window, width=20,bg="white") 
    limits.grid(row=6, column=0, sticky=W)

    choices = ["id","username","date","time","tweet","link","likes_count","replies_count","retweets_count"]
    optionList = Listbox(window, selectmode="multiple")
    optionList.grid(row=8,column=0, sticky=W)
    for column in range(len(choices)):
        optionList.insert(END,choices[column])
        optionList.itemconfig(column,bg="red")
    
    calafter= DateEntry(window,width=20, selectmode="day")
    calafter.grid(row=10,column=0,sticky=W)
    calbefore = DateEntry(window, width=20, selectmode="day")
    calbefore.grid(row=12,column=0,sticky=W)
    csvname = Entry(window, width=20, bg="white")
    csvname.grid(row=14,column=0, sticky=W)
    
    button = Button(window, text="SUBMIT",width=6, command=twitterclick).grid(row=15,column=0,sticky=W)
    Button(window, text="Refresh", width=6, command=twitterpage).grid(row=15,column=1, sticky=E)

def redditpage():
    def redditclick():
        reddit_topic = textentry.get()
        subreddit = subredditentry.get()
        limit = int(commentlimit.get())
        afterdate = return_utc(str(calafter.get_date()))
        beforedate = return_utc(str(calbefore.get_date()))
        filename = csvname.get()
        custom = []
        columnname = optionList.curselection()
        for i in columnname:
            custom.append(optionList.get(i))       

        reddit_scraper(reddit_topic,subreddit,limit,afterdate,beforedate,filename,custom)
    
    
    for labels in list(window.children.values()):
        label = str(labels)
        if label != '.!menu' and label != '.!label':
            labels.destroy()

    #Create label
    Label (window, text="Enter your reddit topic:").grid(row=1, column=0,sticky=W)
    Label (window, text="Enter the subreddit you want to search(Optional):").grid(row=3, column=0,sticky=W)
    Label (window, text="Enter the limit of your comments(Needed):").grid(row=5, column=0,sticky=W)
    Label(window, text="Choose all columns you want to be included:").grid(row=7,column=0,sticky=W)
    Label (window, text="From which date?").grid(row=9,column=0,sticky=W)
    Label (window, text="To which date?" ).grid(row=11,column=0,sticky=W)
    Label (window, text="Enter your CSV filename").grid(row=13,column=0,sticky=W)
    
    #create a text entry box()
    textentry = Entry(window, width=20, bg = "white")
    textentry.grid(row=2,column=0, sticky=W)
    subredditentry = Entry(window, width=20, bg= "white")
    subredditentry.grid(row=4, column=0, sticky=W)
    commentlimit = Entry(window,width=20, bg= "white" )
    commentlimit.grid(row=6,column=0,sticky=W)
    choices = ["id","author","all_awardings","body","created_utc","permalink","score","subreddit"]
    optionList = Listbox(window, selectmode="multiple")
    optionList.grid(row=8,column=0, sticky=W)
    for column in range(len(choices)):
        optionList.insert(END,choices[column])
        optionList.itemconfig(column,bg="red")
    calafter = DateEntry(window, width =20, selectmode="day")
    calafter.grid(row=10,column=0,sticky=W)
    calbefore = DateEntry(window, width=20, selectmode="day")
    calbefore.grid(row=12,column=0,sticky=W)
    csvname = Entry(window, width=40, bg="white")
    csvname.grid(row=14, column=0 , sticky=W)
    #adding a submit and refresh button
    button = Button(window, text="SUBMIT",width=6, command=redditclick).grid(row=15,column=0,sticky=W)
    Button(window, text="Refresh", width=6, command=redditpage).grid(row=15,column=1, sticky=E)



#Main GUI 
window = Tk()
window.title("Reddit and Twitter data scraper")

menubar = Menu(window)
window.config(menu=menubar)

#tearoff 0 to stop random lines from appearing
filemenu = Menu(menubar,tearoff=0) 
menubar.add_cascade(label="Type of Scraper",menu=filemenu)
filemenu.add_command(label="Reddit Scraper",command=redditpage)
filemenu.add_command(label="Twitter Scraper",command=twitterpage)


# #My photo
photo1 = PhotoImage(file="Screenshot_3.png")
Label (window, image= photo1, bg="white").grid(row=0, columnspan=2,sticky=E)

#Create label
frame = Frame(window)

redditpage()
#Main loop
window.mainloop()