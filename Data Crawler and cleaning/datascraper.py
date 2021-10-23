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


url = "https://www.reddit.com"

#Function to return UTC number to readable Date format
def getDate(created):
    """Takes in a UTC number and returns a readable Date format"""
    return dt.datetime.fromtimestamp(created).date()

#Function to format date selected to proper date format
def returnUtc(tkinterdate):
    date = str(tkinterdate)
    date = dt.datetime.strptime(date,"%Y-%m-%d").timetuple()
    date = int(time.mktime(date))
    return date

#Success message popout function when scraping is completed
def popoutImg(): 
    popup = Tk()
    popup.geometry('250x150')
    popup.wm_title("!")
    label = ttk.Label(popup, text="Congrats its done!")
    label.pack(side="top",fill="x",pady=30)

def popoutError():
    popup = Tk()
    popup.geometry('250x150')
    popup.wm_title("!")
    label = ttk.Label(popup, text="Please fill in properly!")
    label.pack(side="top",fill="x",pady=30)

#Reddit function to scrape data using PMAW libraries
#https://github.com/mattpodolak/pmaw 
def redditScraper(topic, subreddit, limit, after, before, csvredditfilename, custom):
    """This function takes in parameters and
    uses PushshiftAPI to scrape through Reddit according
    to the given parameters and limitations"""
    limit = int(limit)
    api = PushshiftAPI()
    
    defaultValues = "body","created_utc","permalink"
    custom.extend(["body","created_utc","permalink"])
    print(custom)
    comments = api.search_comments(q=topic,subreddit=subreddit,limit= limit, after=after, before=before)
    commentsDf= pd.DataFrame(comments)
    commentsDf.drop(commentsDf.columns.difference(custom),1,inplace=True)
    
    if "created_utc" in commentsDf.columns: #Checking whether this is created
        timeStamp = commentsDf["created_utc"].apply(getDate)
        commentsDf = commentsDf.assign(created_utc = timeStamp)
    if "permalink" in commentsDf.columns:
        commentsDf = commentsDf.assign(permalink= url + commentsDf["permalink"]) 
        commentsDf = commentsDf.sort_values('created_utc', ignore_index= True) #Sort the entire sheet by datetime and then index accordingly

    if "body" in commentsDf.columns:
        commentsDf.body = commentsDf.body.apply(html.unescape) #Removing HTML encoding such as &gt &amp
        commentsDf.body = commentsDf.body.apply(lambda x: re.split('https:\/\/.*', str(x))[0]) #Remove Links
        nanValue = float("NaN")
        commentsDf.replace("",nanValue, inplace=True)
        commentsDf.dropna(subset=["body"],inplace=True) #Dropping NaN value for those links found
    
    commentsDf.rename(columns={"created_utc":"date","permalink":"link"},inplace=True)
    
    commentsDf.to_csv(csvredditfilename)
    popoutImg()
    
#Twitter scraping function 
#https://github.com/twintproject/twint 
def twintScraper(topic, links ,since, until, limit, custom, output):
    """Takes in parameters and then set accordingly 
    to the twint configurations and run it"""
    custom.extend(["date","tweet","link"])
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
    popoutImg()

#Tkinter GUI page for twitter menu
def twitterPage(): 
    def twitterClick():
        twitterTopic = twitterEntry.get()
        if variableLink.get() == "Yes":
            links = "exclude"
        else:
            links = "include"
        limit = limits.get()
        custom = []
        columnName = optionList.curselection()
        for i in columnName:
            custom.append(optionList.get(i))
        
        afterDate = str(calAfter.get_date())
        beforeDate = str(calBefore.get_date())
        fileName = csvName.get()
        if twitterTopic and limit and fileName:
            twintScraper(twitterTopic, links, afterDate, beforeDate,limit, custom,fileName) 
        else:
            popoutError()
    
    
    for labels in list(window.children.values()): #This ensures no other menus are overlapping current one
        label = str(labels)
        if label != '.!menu' and label != '.!label':
            labels.destroy()

    digitvalidation = window.register(only_number)

    Label(window, text="Enter your twitter search keyword").grid(row=1,column=0,sticky=W)
    Label(window, text="Do you want to exclude links contained in tweets?").grid(row=3,column=0,sticky=W)
    Label(window, text="Enter the limit of your tweets(numbers)").grid(row=5,column=0,sticky=W)
    Label(window, text="Choose all columns you want to be included: (Default= Date,Tweet, Link").grid(row=7,column=0,sticky=W)
    Label(window, text="From which date?" ).grid(row=9,column=0,sticky=W)
    Label(window,text="To which date?").grid(row=11,column=0,sticky=W)
    Label(window,text="Enter your CSV filename").grid(row=13,column=0,sticky=W)

    twitterEntry = Entry(window,width=20,bg="white")
    twitterEntry.grid(row=2,column=0,sticky=W)
    variableLink = StringVar(window, "Yes")
    links = OptionMenu(window, variableLink, "Yes","No")
    links.grid(row=4,column=0,sticky=W)
    limits = Entry(window, width=20,bg="white") 
    limits.grid(row=6, column=0, sticky=W)
    limits.config(validate="key", validatecommand=(digitvalidation,'%S'))
    choices = ["id","username","time","likes_count","replies_count","retweets_count"]
    optionList = Listbox(window, selectmode="multiple")
    optionList.grid(row=8,column=0, sticky=W)
    for column in range(len(choices)):
        optionList.insert(END,choices[column])
        optionList.itemconfig(column,bg="red")
    
    calAfter= DateEntry(window,width=20, selectmode="day")
    calAfter.grid(row=10,column=0,sticky=W)
    calBefore = DateEntry(window, width=20, selectmode="day")
    calBefore.grid(row=12,column=0,sticky=W)
    csvName = Entry(window, width=20, bg="white")
    csvName.grid(row=14,column=0, sticky=W)
    
    button = Button(window, text="SUBMIT",width=6, command=twitterClick).grid(row=15,column=0,sticky=W)
    Button(window, text="Refresh", width=6, command=twitterPage).grid(row=15,column=1, sticky=W)

def only_number(digit):
    return digit.isdigit()


#Tkinter GUI page for Reddit menu
def redditPage():
    """
    Contains two functions
    redditPage() = GUI menu page for reddit parameters. 
    redditClick() = Onsubmit, wrap parameters and inserts/send the value to redditScraper"""

    def redditClick():

        redditTopic = textEntry.get()
        subreddit = subredditEntry.get()
        limit = commentLimit.get()
        afterDate = returnUtc(str(calAfter.get_date()))
        beforeDate = returnUtc(str(calBefore.get_date()))
        fileName = csvName.get()
        custom = []
        columnName = optionList.curselection() #Gets all of the list selection in Tkinter
        for i in columnName:
            custom.append(optionList.get(i))
            
        if redditTopic and limit and fileName:           
            redditScraper(redditTopic,subreddit,limit,afterDate,beforeDate,fileName,custom)
        else:
            popoutError()
    
    
    for labels in list(window.children.values()):
        label = str(labels)
        if label != '.!menu' and label != '.!label':
            labels.destroy()

    digitvalidation = window.register(only_number)
    #Create label (Text)
    Label (window, text="Enter your reddit topic:").grid(row=1, column=0,sticky=W)
    Label (window, text="Enter the subreddit you want to search(Optional):").grid(row=3, column=0,sticky=W)
    Label (window, text="Enter the limit of your comments(Needed):").grid(row=5, column=0,sticky=W)
    Label(window, text="Choose all columns you want to be included: (Default: body, date, link)").grid(row=7,column=0,sticky=W)
    Label (window, text="From which date?").grid(row=9,column=0,sticky=W)
    Label (window, text="To which date?" ).grid(row=11,column=0,sticky=W)
    Label (window, text="Enter your CSV filename").grid(row=13,column=0,sticky=W)
    
    #create a entry boxes()
    textEntry = Entry(window, width=20, bg = "white")
    textEntry.grid(row=2,column=0, sticky=W)
    subredditEntry = Entry(window, width=20, bg= "white")
    subredditEntry.grid(row=4, column=0, sticky=W)
    commentLimit = Entry(window,width=20, bg= "white" )
    commentLimit.grid(row=6,column=0,sticky=W)
    commentLimit.config(validate="key", validatecommand=(digitvalidation,'%S'))
    choices = ["id","author","all_awardings","is_submitter","author_premium","score","subreddit","subreddit_id"]
    optionList = Listbox(window, selectmode="multiple")
    optionList.grid(row=8,column=0, sticky=W)
    for column in range(len(choices)):
        optionList.insert(END,choices[column])
        optionList.itemconfig(column,bg="red")
    calAfter = DateEntry(window, width =20, selectmode="day")
    calAfter.grid(row=10,column=0,sticky=W)
    calBefore = DateEntry(window, width=20, selectmode="day")
    calBefore.grid(row=12,column=0,sticky=W)
    csvName = Entry(window, width=40, bg="white")
    csvName.grid(row=14, column=0 , sticky=W)
    #adding a submit and refresh button
    button = Button(window, text="SUBMIT",width=6, command=redditClick).grid(row=15,column=0,sticky=W)
    Button(window, text="Refresh", width=6, command=redditPage).grid(row=15,column=1, sticky=E)

#Main GUI layout
window = Tk()
window.title("Reddit and Twitter data scraper")
menuBar = Menu(window)
window.config(menu=menuBar)
fileMenu = Menu(menuBar,tearoff=0) #tearoff 0 to stop random lines from appearing in the menu button
menuBar.add_cascade(label="Type of Scraper",menu=fileMenu)
fileMenu.add_command(label="Reddit Scraper",command=redditPage)
fileMenu.add_command(label="Twitter Scraper",command=twitterPage)
photo1 = PhotoImage(file="Screenshot_3.png")# #My photo
Label (window, image= photo1, bg="white").grid(row=0, columnspan=2,sticky=E)

if __name__ == "__main__":
 #GUI main page   
    #Tkinter GUI to open
    redditPage()
    window.mainloop()