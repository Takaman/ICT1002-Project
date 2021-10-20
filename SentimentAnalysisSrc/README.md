# Sentiment Analysis

## Description of Sentiment Analysis

This scripts takes in sanitized data as a csv file and analyses every row's text column.
A score is generated for the text to determine the sentiment. At the sentence level, this is between -1
to +1, -1 being very negative and +1 being very positive.

The threshold set are as follows:

Positive sentiment	: compound score >= 0.05 
Negative sentiment	: compound score <= -0.05
Neutral sentiment	: compound score > -0.05 and compound score < 0.05 

However, if a sentence exceeds a certain character limit (280), it is then broken up into sentences, and scores
are aggregated at the sentence level for the whole post. This is to allow for better accuracy of evaluating
the sentiment as the sentiment analysis performs better in shorter texts. But because the score is aggregated,
the maximum and minimum scores will differ from the max and min score of +1 and -1 respectively.

After data is analyzed, 3 output files are generated that contains their respective sentiments.

They are positive.csv, negative.csv and neutral.csv.

### Steps neccessary to run code

1) Open CMD and run ``> pip install requirements.txt``
2) Download the NLTK data. We recommend these 2 ways of installing the NLTK data.
	- Interactive installer
		- Run Python interpreter and the following code:
		- This is to check NLTK has been installated successfully:
			
			``> import nltk``
			
			``> ntlk.download()``
	
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

	- Command Line installation
		- Run cmd and type into it the following: python -m nltk.downloader all

	- For further information, please check https://www.nltk.org/data.html 

#### Description of each file:

- main.py

	- This is the main script for the sentiment analysis.
	- It takes in a sanitized data csv file and outputs 3 csv files for their respective sentiments.

- redditandtweetsv2

	- Sample sanitized input data.

- positive.csv

	- Sample output data.

- negative.csv

	- Sample output data.

- neutral.csv

	- Sample output data.

- requirements.txt

	- It specifies the dependencies and their versions that the script depends on.
