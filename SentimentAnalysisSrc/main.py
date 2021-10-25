"""
This module does sentimental analysis utilising the VADER sentiment analysis library.
It supports csv files that must include 3 default column field names in any order.

They are:

    1. "body" (this refers to the text column that contains rows of text to be analysed)
    2. "date" (this refers to the date of the social media post)
    3. "link" (this refers to the link to the social media post)

It evaluates the text row by row, giving them a compound score that represents the sentiment.
Score ranges from -1 (very negative) to +1 (very positive).
Once the script finishes execution, it generates 3 output csv files with the text and their sentiment scores.
"""

# Done by: Pang Ka Ho and Wang Qi Xian

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import os.path
import pandas as pd
import sys
import re
import time
import decimal


# Algorithm provided by: Kamil Slowikowski (2018) remove-emoji.py version 1 [source code]
# https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
def removeEmoji(text: str) -> str:
    """
    Removes all emojis in a string. Returns the string without emojis.
    :param text: A string containing emojis.
    :type text: str
    :return: A string without the emojis.
    :rtype: str
    """

    emojiPattern = re.compile("["
                              u"\U0001F600-\U0001F64F"  # emoticons
                              u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                              u"\U0001F680-\U0001F6FF"  # transport & map symbols
                              u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                              u"\U00002500-\U00002BEF"  # chinese char
                              u"\U00002702-\U000027B0"
                              u"\U00002702-\U000027B0"
                              u"\U000024C2-\U0001F251"
                              u"\U0001f926-\U0001f937"
                              u"\U00010000-\U0010ffff"
                              u"\u2640-\u2642"
                              u"\u2600-\u2B55"
                              u"\u200d"
                              u"\u23cf"
                              u"\u23e9"
                              u"\u231a"
                              u"\ufe0f"  # dingbats
                              u"\u3030"
                              "]+", flags=re.UNICODE)
    return emojiPattern.sub(r'', text)


def loadData(filePath: str) -> pd.DataFrame:
    """
    Loads file using pandas CSV read function. Returns a pandas DataFrame object.
    :param filePath: A string containing the file path to the data file.
    :type filePath: str
    :return: A panda data frame containing the file data.
    :rtype: pd.DataFrame
    """

    try:
        df = pd.read_csv(filePath, encoding="utf-8")
    except FileNotFoundError:
        print("File not found, please check file name input.")
        sys.exit(1)

    if df is None:
        print("Something went wrong.")
        sys.exit(1)

    return df


def appendDataToBuffer(data: dict, buffer: dict) -> None:
    """
    Helper function to append values of data dict to values of buffer dict. Modifies in place. Returns none.
    :param data: A dictionary containing the relevant data.
    :type data: dict
    :param buffer: A dictionary to contain the data.
    :type buffer: dict
    :return: None.
    :rtype: NoneType
    """

    buffer["text"].append(removeEmoji(data["text"]))
    buffer["score"].append(data["score"])
    buffer["date"].append(data["date"])
    buffer["link"].append(data["link"])


def createDataFrame(buffer: dict) -> pd.DataFrame:
    """
    Helper function to create a pandas DataFrame Object from buffer dict. Returns a pandas DataFrame Object.
    :param buffer: A dictionary that contains the data.
    :type buffer: dict
    :return: A dataframe with the data stored in buffer.
    :rtype: pd.DataFrame
    """

    df = pd.DataFrame({
        "rowNo": list(range(buffer["rowNo"])),
        "text": buffer["text"],
        "score": buffer["score"],
        "date": buffer["date"],
        "link": buffer["link"]
    })

    return df


def createDataBuffer() -> dict:
    """
    Helper function that creates a data buffer with the relevant key value pairs. Returns a dictionary.
    :return: A dictionary
    :rtype: dict
    """

    dataBuffer = {
        "text": [],
        "score": [],
        "date": [],
        "link": []
    }
    return dataBuffer


def analyseData(df: pd.DataFrame) -> tuple:
    """
    Analyses the DataFrame input and returns 3 DataFrame objects in a tuple.
    :param df: A pandas DataFrame object containing the sanitized data.
    :type df: pd.DataFrame
    :return: A tuple containing 3 DataFrame objects with their respective sentiments (posDF, negDF, neuDF).
    :rtype: tuple
    """

    posDataBuffer = createDataBuffer()
    negDataBuffer = createDataBuffer()
    neuDataBuffer = createDataBuffer()

    threshold = 0.05

    positiveCount = 0
    negativeCount = 0
    neutralCount = 0

    charLimit = 280

    analyzer = SentimentIntensityAnalyzer()

    for row in range(len(df.index)):

        try:
            originalSentence = df.iloc[row]["body"]
            date = df.iloc[row]["date"]
            link = df.iloc[row]["link"]
        except (IndexError, KeyError) as e:
            continue

        score = 0

        # If the social media posts exceeds the character limit that we set
        if len(originalSentence) > charLimit:

            # Break in up to sentences
            listOfSentences = TextBlob(originalSentence).sentences

            # Aggregate sentiment score at the sentence level
            for sentence in listOfSentences:
                score += analyzer.polarity_scores(sentence)["compound"]
                
            # Get the average score for the tallied sentiment score
            score = decimal.Decimal(score) / decimal.Decimal(len(listOfSentences))

        else:

            score = analyzer.polarity_scores(originalSentence)["compound"]

        data = {
            "text": removeEmoji(originalSentence),
            "score": score,
            "date": date,
            "link": link
        }

        if score >= threshold:
            positiveCount += 1
            appendDataToBuffer(data, posDataBuffer)

        elif score <= -threshold:
            negativeCount += 1
            appendDataToBuffer(data, negDataBuffer)

        else:
            neutralCount += 1
            appendDataToBuffer(data, neuDataBuffer)

    posDataBuffer["rowNo"] = positiveCount
    negDataBuffer["rowNo"] = negativeCount
    neuDataBuffer["rowNo"] = neutralCount

    posDF = createDataFrame(posDataBuffer)
    negDF = createDataFrame(negDataBuffer)
    neuDF = createDataFrame(neuDataBuffer)

    return posDF, negDF, neuDF


def createOutputCSVFile(df: pd.DataFrame, fileName: str, index: int = 1) -> None:
    """
    Creates an output CSV file based on the DataFrame input using the pandas to_csv function.
    If there is an existing file that has the same name, it creates another file with a modified name instead.
    Returns None.
    :param df: A pandas DataFrame object containing the analysed data.
    :type df: pd.DataFrame
    :param fileName: A string containing the name of the new file to be created.
    :type fileName: str
    :param index: An integer specifying the version of the file. Default argument provided is 1.
    :type index: int
    :return: None.
    :rtype: NoneType
    """

    if index == 1:

        # If file does not exist in project folder
        if not os.path.isfile(f"{fileName}.csv"):

            # Attempt to create a new file
            df.to_csv(f"{fileName}.csv", index=False)

        # Else file exist with the same name, attempt to create another file instead
        else:

            index += 1
            createOutputCSVFile(df, f"{fileName}", index)

    else:

        newFileName = f"{fileName} ({index})"

        if not os.path.isfile(f"{newFileName}.csv"):

            # Attempt to create a new file
            df.to_csv(f"{newFileName}.csv", index=False)

        else:

            index += 1
            createOutputCSVFile(df, f"{fileName}", index)


def main():
    """
    Loads data, analyses data, and generates 3 csv files for positive, negative and neutral sentiment in folder.
    """
    
    # Set decimal precision
    decimal.getcontext().prec = 4

    startTime = time.perf_counter()

    # Sample hardcoded test data
    # filePath = "redditandtweetsv3.csv"
    
    # Validate user argument length
    if len(sys.argv) != 2:
        print("Usage: py main.py dataFile.csv")
        sys.exit(1)

    filePath = sys.argv[1]
    df = loadData(filePath)

    posDF, negDF, neuDF = analyseData(df)

    createOutputCSVFile(posDF, "positive")
    createOutputCSVFile(negDF, "negative")
    createOutputCSVFile(neuDF, "neutral")

    stopTime = time.perf_counter()

    print(f"\nTime taken: {stopTime - startTime:.02f} seconds")

    sys.exit(0)


if __name__ == "__main__":
    main()
