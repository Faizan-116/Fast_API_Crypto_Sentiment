# main.py
from fastapi import FastAPI,status
from pydantic import BaseModel


import pandas as pd
from datetime import date
import datetime
# import nltk
# from nltk.tokenize import word_tokenize 
# from nltk.corpus import stopwords
# stop = stopwords.words('english')
import re #[\s!-@^#$]
from requests import get
from bs4 import BeautifulSoup
import praw
import datetime as dt


import snscrape.modules.twitter as sntwitter









app = FastAPI()

@app.get("/")
def hello():
    return {"message":"Hello TutLinks.com"}


class findhas(BaseModel):
    InputText: str
    
#function to extract hastags
def sentiment_scores(Curency):
    url = 'https://finance.yahoo.com/topic/crypto?guccounter=1'
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    web = html_soup.find_all('li', class_ = 'js-stream-content Pos(r)')
    
    text = []
# Extract data from individual movie container
    for container in web:

        tex = container.find('p')
        if(tex) is not None:
            text.append(tex.text)
# The year
        tex = container.a.text
        text.append(tex)

    url = 'https://www.coindesk.com/'
    response = get(url)

    html_soup = BeautifulSoup(response.text, 'html.parser')
    web = html_soup.find_all('div', class_ = 'article-cardstyles__StyledWrapper-q1x8lc-0 fWyZg article-card default')


    
    # Extract data from individual movie container
    for container in web:
# If the movie has Metascore, then extract:
   
# The name
  # if(container.p.text) is not None:
        tex = container.find('a', class_ = 'card-title')
        if(tex) is not None:
            text.append(tex.text)
# The year
        tex = container.find('span', class_ = 'content-text')
        if(tex) is not None:
            text.append(tex.text)


    
    
    url = 'https://www.investopedia.com/cryptocurrency-news-5114163'
    response = get(url)
    
    html_soup = BeautifulSoup(response.text, 'html.parser')
    web = html_soup.find_all('a', class_ = 'comp mntl-card-list-items mntl-document-card mntl-card card card--no-image')

    
# Extract data from individual movie container
    for container in web:
    # If the movie has Metascore, then extract:
    
    # The name
    # if(container.p.text) is not None:
        tex = container.find('span', class_ = 'card__title-text')
        if(tex) is not None:
            text.append(tex.text)
    
    sec_df = pd.DataFrame({'text': text})
    return sec_df
    Previous_Date = datetime.datetime.today() - datetime.timedelta(days=7)
    from_date = Previous_Date.strftime ('%Y-%m-%d') # format the date to ddmmyyyy
    today = date.today()
    end_date = today


    
        # Creating list to append tweet data to
    tweets_list1 = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:elonmusk').get_items()):
        if i>200:
            break
        tweets_list1.append([tweet.content])
    df_elon = pd.DataFrame(tweets_list1, columns=[ 'text'])


    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:CoinMarketCap').get_items()):
        if i>200:
            break
        tweets_list1.append([tweet.content])
    df_Coin = pd.DataFrame(tweets_list1, columns=[ 'text'])

    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:spectatorindex').get_items()):
        if i>200:
            break
        tweets_list1.append([tweet.content])
    df_spect = pd.DataFrame(tweets_list1, columns=[ 'text'])




    
    # user_name = "elonmusk"
    # user_tweets = "snscrape --format '{content!r}'"+ f" --since {from_date} twitter-user '{user_name}  until:{end_date}' > user-tweets.value"
    # os.system(user_tweets)
    
    # df_elon = pd.read_csv('user-tweets.value', names=['text'])


    # user_name = "CoinMarketCap"
    # user_tweets = "snscrape --format '{content!r}'"+ f"  --since {from_date}  twitter-user '{user_name}  until:{end_date}' > user-tweets.txt"
    # os.system(user_tweets)
    
    # df_Coin = pd.read_csv('user-tweets.txt', names=['text'])
    # return df_Coin


    # user_name = "spectatorindex"
    # user_tweets = "snscrape --format '{content!r}'"+ f"  --since {from_date}  twitter-user '{user_name}  until:{end_date}' > user-tweets.txt"
    # os.system(user_tweets)
    # if os.stat("user-tweets.txt").st_size == 0:
    #     print('No Tweets found')
    # else:
    #     df_spect = pd.read_csv('user-tweets.txt', names=['text'])
    
    reddit = praw.Reddit(client_id='1JgmmDr2XlraFbpe0nJjjQ', \
                     client_secret='oeHeDMRu9A9GsLCzIGQeywj6RaqNtw', \
                     user_agent='Crypto', \
                     username='FaizanSaab ', \
                     password='Keyewa1122.')


    subreddit = reddit.subreddit('CryptoNews')

    top_subreddit = subreddit.top(time_filter="week")
    df_rCrypto = { "text":[], 
                
                    }
    for submission in top_subreddit:
        df_rCrypto["text"].append(submission.title)
    df_rCrypto = pd.DataFrame(df_rCrypto)
    subreddit = reddit.subreddit('cryptosignals')

    top_subreddit = subreddit.top(time_filter="week")
    df_signal = { "text":[], 
                
                }
    for submission in top_subreddit:
        df_signal["text"].append(submission.title)
   #
    df_signal = pd.DataFrame(df_signal)
    frames = [sec_df,df_elon,df_Coin,df_spect,df_rCrypto,df_signal ]
    
    df1 = pd.concat(frames)
    
    df = df1.dropna()

    df["text"]  = df["text"].apply(lambda x : ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",x).split()))
    df["text"]  = df["text"].apply(lambda x : ''.join([i for i in x if not i.isdigit()]))
    df["text"]  = df["text"].apply(lambda x : x.lower())

  
    val = Curency

    df2 = df[df['text'].str.contains(val)]
    data=df2[['text']]
    dataa=data.to_dict()
    return dataa


# If the movie has Metascore, then extract:
   

  # if(container.p.text) is not None:
   



#api for find sentiment in the text
@app.post("/findsentiment", status_code=status.HTTP_201_CREATED)
def sentiment(User: findhas):
    return sentiment_scores(User.InputText)