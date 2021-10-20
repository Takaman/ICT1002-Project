from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import pandas as pd
import sys
import re


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


def main():
    """
    Loads data, analyses data, and generates 3 csv files for positive, negative and neutral sentiment in folder.
    """

    # filePath = sys.argv[1]
    filePath = "redditandtweetsv2.csv"
    df = loadData(filePath)

    posDF, negDF, neuDF = analyseData(df)

    posDF.to_csv("positive.csv", index=False)
    negDF.to_csv("negative.csv", index=False)
    neuDF.to_csv("neutral.csv", index=False)

    sys.exit(0)


if __name__ == "__main__":
    main()
