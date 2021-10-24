# GUI Data scraper for reddit and twitter

## What does it do?

The Datascraper.exe file opens up a GUI utilising Tkinter's library for users to enter search parameters for Reddit and Twitter.

Tools used:
1) Twint      https://github.com/twintproject/twint
2) Pmaw       https://github.com/mattpodolak/pmaw
3) langdetect https://github.com/Mimino666/langdetect
4) FTFY       https://github.com/rspeer/python-ftfy

## Features
1) User friendly
2) Loosely coupled from other modules, can be used independently.
3) Filters to choose exactly which columns you need
4) Exported into a CSV file with clickable links


## Step by step process on using it

1) Download the entire folder "Data Crawler and cleaning"
2) Navigate to the folder in terminal and type `pip3 install -r requirements.txt` to install the prerequisites libraries
3) Open up Datascraper.exe and enter the parameters needed
<img src="https://user-images.githubusercontent.com/91510432/138582781-52ececba-274b-4ebc-a45f-37a2c0fc9a37.png" width="250" height="400">

4) If there are missing or error fields, a popup will appear to indicate that it has issues.
5) After clicking on the submit button, the screen will be unresponsive for a while and the submit button will remain pressed. When scraping of data is successful, there will be a popup message.
<img src= "https://user-images.githubusercontent.com/91510432/138583295-57029e12-5226-417a-9098-091162adfe36.png" width="200" height="150">
6) A CSV file named by you will then appear in the same folder. 


