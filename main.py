from flask import Flask, render_template, request
import flask
import json
from urllib import request, parse
from textblob import TextBlob
import re
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

app = Flask(__name__)
try:
	key = json.loads('./util/Secret.json')
except:
	print('Save the secret key in Secret.json')
app.config['SECRET_KEY'] = key['SECRET']

def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(tweet)).split())


def get_tweet_sentiment(tweet):
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def getLang(tweets):
    ces = 0
    cen = 0
    cth = 0
    chi = 0
    cfr = 0
    for tweet in tweets:
        if (str(tweet['lang']).__contains__('es')):
            ces = ces + 1
        elif (str(tweet['lang']).__contains__('en')):
            cen = cen + 1
        elif (str(tweet['lang']).__contains__('th')):
            cth = cth + 1
        elif (str(tweet['lang']).__contains__('hi')):
            chi = chi + 1
        elif(str(tweet['lang']).__contains__('fr')):
            cfr = cfr + 1
    print("Number of tweets by language:")
    print("Number of English Tweets=")
    print(cen)
    print("Number of Spanish Tweets=")
    print(ces)
    print("Number of Thai Tweets=")
    print(cth)
    print("Number of Hindi Tweets=")
    print(chi)
    print("Number of French Tweets=")
    print(cfr)
    tweetCount=list()
    tweetCount.append(cen)
    tweetCount.append(ces)
    tweetCount.append(cth)
    tweetCount.append(chi)
    tweetCount.append(cfr)
    print(tweetCount)
def getCity(tweets):
    ces = 0
    cen = 0
    cth = 0
    chi = 0
    cfr = 0
    for tweet in tweets:
        if (str(tweet['city']).__contains__('New York City')):
            ces = ces + 1
        elif (str(tweet['city']).__contains__('Mexico City')):
            cen = cen + 1
        elif (str(tweet['city']).__contains__('Paris')):
            cth = cth + 1
        elif (str(tweet['city']).__contains__('Bangkok')):
            chi = chi + 1
        elif(str(tweet['city']).__contains__('New Delhi')):
            cfr = cfr + 1
    print("Number of tweets by language:")
    print("Number of English Tweets=")
    print(cen)
    print("Number of Spanish Tweets=")
    print(ces)
    print("Number of Thai Tweets=")
    print(cth)
    print("Number of Hindi Tweets=")
    print(chi)
    print("Number of French Tweets=")
    print(cfr)
    tweetCount=list()
    tweetCount.append(cen)
    tweetCount.append(ces)
    tweetCount.append(cth)
    tweetCount.append(chi)
    tweetCount.append(cfr)
    print(tweetCount)
def getTweets(query,city,topic):
    finalQuery= 'city:"'+city+'" AND topic:"'+topic+'" AND '+query
    filterQuery = parse.quote_plus(finalQuery)
    query = parse.quote_plus(query)
    in_url = 'http://127.0.0.1:8983/solr/Project4/select?facet.field=extended_tweet.entities.hashtags.text&facet=on&q=' + filterQuery + '&fl=text,extended_tweet.entities.hashtags.text&rows=20&wt=json'
    print(in_url)
    trend_in_url = 'http://127.0.0.1:8983/solr/Project4/select?facet.field=extended_tweet.entities.hashtags.text&facet.field=lang&facet.field=city&facet.field=topic&facet=on&q=' + query + '&fl=text&rows=1000&wt=json'
    data = request.urlopen(in_url)
    data_analysis=request.urlopen(trend_in_url)
    docs = json.load(data)
    docs_analysis=json.load(data_analysis)
    response=docs['response']['docs']
    hashtags=docs_analysis['facet_counts']['facet_fields']['extended_tweet.entities.hashtags.text']
    cities = docs_analysis['facet_counts']['facet_fields']['city']
    topics = docs_analysis['facet_counts']['facet_fields']['topic']
    languages = docs_analysis['facet_counts']['facet_fields']['lang']
    print(cities)
    print(topics)
    print(languages)
    fetched_data = docs_analysis['response']['docs']
    tweets = list()
    analysis=list()
    trending_hashtags = list()
    city_analysis = list()
    lang_analysis = list()
    topic_analysis = list()
    for doc in response:
        tweet=str(doc['text'])
        tweets.append(tweet[2:tweet.__len__()-2])
    #getLang(fetched_data)
    #getCity(fetched_data)
    for tweet in fetched_data:
        parsed_tweet = dict()
        currTweet = tweet['text']
        # saving text of tweet
        # print(currTweet)
        parsed_tweet['text'] = currTweet
        # print(currTweet)
        currTweetTxt=str(currTweet)
        currTweetTxt=currTweetTxt[2:currTweetTxt.__len__()-2]
        currTweetTxt=re.sub(r'(@[A-Za-z0-9]+)|(^https?:\/\/.*[\r\n]*)', ' ',currTweetTxt)
        # print(currTweetTxt)
        # try:
        #     translator = Translator()
        #     en=translator.translate(currTweetTxt,dest='en')
        #     for enTweet in en:
        #         currTweet=enTweet.text
        # except Exception as ex:
        #     print(ex)
        #     pass
        parsed_tweet['sentiment'] = get_tweet_sentiment(currTweet)
        analysis.append(parsed_tweet)
    index=0
    city_analysis=['','','','','']
    topic_analysis=['','','','','']
    for city in cities:
        print(city)
        if (index == len(cities) - 1):
            break
        if (str(city).__contains__('New York City')):
            city_analysis[0]=cities[index+1]
        elif (str(city).__contains__('Mexico City') or str(city).__contains__('Mexico')):
            city_analysis[1] = cities[index + 1]
        elif (str(city).__contains__('Paris')):
            city_analysis[2] = cities[index + 1]
        elif (str(city).__contains__('Bangkok')):
            city_analysis[3] = cities[index + 1]
        elif(str(city).__contains__('New Delhi')):
            city_analysis[4] = cities[index + 1]
        index=index+1
    index = 0
    for lang in languages:
        if index <= len(languages) - 1:
            if (int(languages[index + 1]) >= 1):
                lang_analysis.append(str(languages[index]))
            index += 2
        else:
            break
    index = 0
    for topic in topics:
        if(index==len(topics)-1):
            break
        if (str(topic).__contains__('Social Unrest') or str(topic).__contains__('Social Unrest')):
            topic_analysis[0]=topics[index+1]
        elif (str(topic).__contains__('infra') or str(topic).__contains__('Infra') or str(topic).__contains__('Infrastructure')):
            topic_analysis[1] = topics[index + 1]
        elif (str(topic).__contains__('environment') or str(topic).__contains__('Environment')):
            topic_analysis[2] = topics[index + 1]
        elif (str(topic).__contains__('crime') or str(topic).__contains__('Crime')):
            topic_analysis[3] = topics[index + 1]
        elif(str(topic).__contains__('politics') or str(topic).__contains__('Politics')):
            topic_analysis[4] = topics[index + 1]
        index = index + 1
    index=0
    for hashtag in hashtags:
        if index <= len(hashtags) - 1:
            if (int(hashtags[index + 1]) >= 1):
                trending_hashtags.append('#' + str(hashtags[index]))
            index += 2
        else:
            break
    data_set = pd.DataFrame(trending_hashtags, columns=["Hashtag"])
    index=0
    for topic in topic_analysis:
        if topic=='':
            topic_analysis[index]=0
        index=index+1
    index=0
    for city in city_analysis:
        if city=='':
            city_analysis[index]=0
        index=index+1
    print(topic_analysis)
    print(city_analysis)
    return trending_hashtags,tweets,analysis,data_set,city_analysis,lang_analysis,topic_analysis


def GetAnalysisResult(tweets):
    # picking positive tweets from tweets
    try:
        positivetweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        # percentage of positive tweets
        positivePer=100 * len(positivetweets)/ len(tweets)
        print(positivePer)
        # picking negative tweets from tweets
        negTweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        # percentage of negative tweets
        negativePer = 100 * len(negTweets) / len(tweets)
        print(negativePer)
        # percentage of neutral tweets
        neutralTweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
        neutralPer = 100 * len(neutralTweets) / len(tweets)
        print(neutralPer)
    except:
        return 0,0,0
    return positivePer,negativePer,neutralPer


def genWordcloud(data_set):
    data_set_wordcloud = data_set.groupby('Hashtag').size()
    data_set_wordcloud.to_csv("hashtags_wordcloud.csv")
    Hashtag_Combined = " ".join(data_set['Hashtag'].values.astype(str))
    wc = WordCloud(background_color="white", stopwords=STOPWORDS)
    wc.generate(Hashtag_Combined)
    plt.figure(figsize=(20,10), facecolor='k')
    plt.imshow(wc)
    plt.axis("off")
    plt.tight_layout(pad=1)
    plt.savefig('static/img/Hashtag.png', dpi=800)


# Basic flask call to start web app
@app.route("/",methods = ['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        topic = flask.request.form.get('topic')
        # print(topic)
        city = flask.request.form.get('city')
        # print(city)
        query = flask.request.form.get('query')
        # print(query)
        trending_hashtags, tweets,analysis,data_set,city_analysis,lang_analysis,topic_analysis = getTweets(query,city,topic)
        genWordcloud(data_set)
        positivePer,negativePer,neutralPer=GetAnalysisResult(analysis)
        # for tweet in tweets:
        #     print(str(tweet) + ":" + str(tweets[tweet]))
        # print(trending_hashtags)
        return render_template("home/dashboard.html",trending_hashtags=trending_hashtags,tweets=tweets,positivePer=positivePer,negativePer=negativePer,neutralPer=neutralPer,city=city,topic=topic,query=query,city_analysis=city_analysis,lang_analysis=lang_analysis,topic_analysis=topic_analysis)
    else:
        return render_template("home/index.html")


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
