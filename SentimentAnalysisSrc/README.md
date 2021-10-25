# Sentiment Analysis

## Description of Sentiment Analysis

This scripts takes in sanitized data as a csv file and analyses every row's text column using the VADER sentiment analysis library.
A score is generated for the text to determine the sentiment. At the sentence level, this is between -1
to +1, -1 being very negative and +1 being very positive.

The threshold set are as follows:

Positive sentiment	: compound score >= 0.05 

Negative sentiment	: compound score <= -0.05

Neutral sentiment	: compound score > -0.05 and compound score < 0.05 


After the data is analyzed, 3 output files are generated that contains their respective sentiments.

They are positive.csv, negative.csv and neutral.csv.

### Neccessary library installations 

1) Run command line terminal and change directory to where your SentimentAnalysisSrc folder is.
2) Type in the following code in your terminal to install the libraries: 

	``pip -m install -r requirements.txt``

3) Download the NLTK data. We recommend these 2 ways of installing the NLTK data.

	- Command Line installation
		- Run cmd and type into it the following: python -m nltk.downloader all

	- Interactive installer
		- Run Python interpreter and the following code:
		- This is to check NLTK has been installated successfully:
			
			``> import nltk``
			
			``> nltk.download()``
	
		- (Extracted from nltk.org) A new window should open, showing the NLTK Downloader. 
		Click on the File menu and select Change Download Directory. 
		For central installation, set this to C:\nltk_data (Windows), 
		/usr/local/share/nltk_data (Mac), or /usr/share/nltk_data (Unix). 
		Next, select the packages or collections you want to download.

		We recommend downloading all of the collections.

		- (Extracted from nltk.org) Test that the data has been installed as follows. 
		(This assumes you downloaded the Brown Corpus): 
			
			``> from nltk.corpus import brown``
			
			``> brown.words()``

			output: ['The', 'Fulton', 'County', 'Grand', 'Jury', 'said', ...]

	- For further information, please check https://www.nltk.org/data.html 

### Steps neccessary to run code

1) Run command line terminal and change directory to where your SentimentAnalysisSrc folder is.
2) Type in the following code in your terminal to run the script:

``py main.py dataFile.csv``


3) Give the script time to run. It takes an average of 60 - 70 seconds for a sameple data of 70K rows.
4) 3 newly generated CSV outfile files will appear in the same project folder.
5) If you run the code with an existing output file in the same project folder, a new outfile file with
a modified name with be generated instead. Your existing output file will not be overwritten.

#### Description of each file:

- main.py

	- This is the main script for the sentiment analysis.
	- It takes in a sanitized data csv file and outputs 3 csv files for their respective sentiments.

- redditandtweetsv3

	- Sample sanitized input data.

- positive.csv

	- Sample output data.

- negative.csv

	- Sample output data.

- neutral.csv

	- Sample output data.

- requirements.txt

	- It specifies the dependencies and their versions that the script depends on.
