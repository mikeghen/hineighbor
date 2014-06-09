from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from instagram.client import InstagramAPI
import tweepy
import json
import requests
import urllib
# Create your views here.

# set_twitter - Autheticate with twitter using tweepy
# FCTVAL == api, an instance of tweepy api
def setup_twitter():
    # Authenticate with Twitter
    auth = tweepy.OAuthHandler('')
    auth.set_access_token('', '')
    api = tweepy.API(auth)
    sapi = tweepy.streaming.Stream(auth, 1)
    return api, sapi

# setup_instagram - Authenticate with instagram 
# FCTVAL == api, an instance of the Instagram API that has been authenticated
def setup_instagram():
    access_token = ''
    api = InstagramAPI(access_token=access_token)
    return api 

def index(request):
    ## Twitter
    api, sapi = setup_twitter()
    #Query for Harvard Tweets
    harvard_data = api.search(q="Harvard Square", rpp=10, show_user=True)
    harvard_tweets = []   
    for tweet in harvard_data:
        harvard_tweets.append(tweet.text)
    #Query for Porter Tweets
    porter_data = api.search(q="Porter Square", rpp=10, show_user=True)
    porter_tweets = []
    for tweet in porter_data:
        porter_tweets.append(tweet.text)
    #Query for Kendall Tweets
    kendall_data = api.search(q="Kendall Square", rpp=10, show_user=True)
    kendall_tweets = []
    for tweet in kendall_data:
        kendall_tweets.append(tweet.text)
    ## Instagram
    api = setup_instagram()
    # Harvard
    harvard_data = api.media_search(count='20', lat=42.373524, lng=-71.118628, distance=2000)
    harvard_grams_data = []
    i = 0
    for media in harvard_data:
        try:
            harvard_grams_data.append({'number':i, 'link': media.link, 'caption': str(media.caption).encode('utf-8').replace('\n', ' ').replace('\r', ''), 'lat':str(media.location.point.latitude),'lng':str(media.location.point.longitude), 'url':str(media.images['standard_resolution'].url)})
        except UnicodeDecodeError:
            harvard_grams_data.append({'number':i, 'link': media.link, 'caption': '', 'lat':str(media.location.point.latitude),'lng':str(media.location.point.longitude), 'url':str(media.images['standard_resolution'].url)})
        i = 1 + i
    # Porter
    porter_data = api.media_search(count='20', lat=42.388651, lng=-71.119775)
    porter_grams_data = []
    i = 0
    for media in porter_data:
        try:
            porter_grams_data.append({'number':i, 'link': media.link, 'caption': str(media.caption).encode('utf-8').replace('\n', ' ').replace('\r', ''), 'lat':str(media.location.point.latitude),'lng':str(media.location.point.longitude), 'url':str(media.images['standard_resolution'].url)})
        except UnicodeDecodeError:
            porter_grams_data.append({'number':i, 'link': media.link, 'caption': '', 'lat':str(media.location.point.latitude),'lng':str(media.location.point.longitude), 'url':str(media.images['standard_resolution'].url)})
        i = 1 + i
    # Kendall
    kendall_data = api.media_search(count='20', lat=42.362558, lng=-71.086386, distance=2000)
    kendall_grams_data = []
    i = 0
    for media in kendall_data:
        try:
            kendall_grams_data.append({'number':i, 'link': media.link, 'caption': str(media.caption).encode('utf-8').replace('\n', ' ').replace('\r', ''), 'lat':str(media.location.point.latitude),'lng':str(media.location.point.longitude), 'url':str(media.images['standard_resolution'].url)})
        except UnicodeDecodeError:
            kendall_grams_data.append({'number':i, 'link': media.link, 'caption': '', 'lat':str(media.location.point.latitude),'lng':str(media.location.point.longitude), 'url':str(media.images['standard_resolution'].url)})
        i = 1 + i 
    template = loader.get_template('index.html')
    ## Globe
    # Harvard Square
    r = requests.get('http://54.237.114.25/s?key=chris&start=0&size=5&return-fields=headline,summary,printpublicationdate,canonicalurl,latitude_1k,longitude_1k,latitude,longitude,&bq=(and%20content:%27harvard%20square%27)&rank=-printpublicationdate')

    harvard_raw_globe = json.loads(r.text)
    harvard_globe_urls = []
    harvard_globe_lats = []
    harvard_globe_lngs = []
    for i in range(0,5):
        harvard_globe_urls.append(harvard_raw_globe['hits']['hit'][i]['data']['canonicalurl'])
        harvard_globe_lats.append(harvard_raw_globe['hits']['hit'][i]['data']['latitude'])
        harvard_globe_lngs.append(harvard_raw_globe['hits']['hit'][i]['data']['longitude'])
    # Porter Square
    r = requests.get('http://54.237.114.25/s?key=chris&start=0&size=5&return-fields=headline,summary,printpublicationdate,canonicalurl,latitude_1k,longitude_1k,latitude,longitude,&bq=(and%20content:%27porter%20square%27)&rank=-printpublicationdate')

    porter_raw_globe = json.loads(r.text)
    porter_globe_urls = []
    porter_globe_lats = []
    porter_globe_lngs = []
    for i in range(0,5):
        porter_globe_urls.append(porter_raw_globe['hits']['hit'][i]['data']['canonicalurl'])
        porter_globe_lats.append(porter_raw_globe['hits']['hit'][i]['data']['latitude'])
        porter_globe_lngs.append(porter_raw_globe['hits']['hit'][i]['data']['longitude'])
    # Porter Square
    r = requests.get('http://54.237.114.25/s?key=chris&start=0&size=5&return-fields=headline,summary,printpublicationdate,canonicalurl,latitude_1k,longitude_1k,latitude,longitude,&bq=(and%20content:%27kendall%20square%27)&rank=-printpublicationdate')

    kendall_raw_globe = json.loads(r.text)
    kendall_globe_urls = []
    kendall_globe_lats = []
    kendall_globe_lngs = []
    for i in range(0,5):
        kendall_globe_urls.append(kendall_raw_globe['hits']['hit'][i]['data']['canonicalurl'])
        kendall_globe_lats.append(kendall_raw_globe['hits']['hit'][i]['data']['latitude'])
        kendall_globe_lngs.append(kendall_raw_globe['hits']['hit'][i]['data']['longitude'])
    
    context = RequestContext(request, {
        'harvard_tweets': harvard_tweets,
        'harvard_glode_urls': harvard_globe_urls,
        'harvard_globe_lats':harvard_globe_lats,
        'harvard_globe_lngs':harvard_globe_lngs,
        'harvard_grams_data': harvard_grams_data,
        'porter_tweets': porter_tweets,
        'porter_glode_urls':porter_globe_urls,
        'porter_globe_lats':porter_globe_lats,
        'porter_globe_lngs':porter_globe_lngs,
        'porter_grams_data': porter_grams_data,
        'kendall_tweets': kendall_tweets,
        'kendall_glode_urls':kendall_globe_urls,
        'kendall_globe_lats':kendall_globe_lats,
        'kendall_globe_lngs':kendall_globe_lngs,
        'kendall_grams_data': kendall_grams_data,

    })
    return HttpResponse(template.render(context))

