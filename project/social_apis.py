import pyrebase, json, requests
import json
from random import choice
from flask_oauthlib.client import OAuth
import requests as rq
from bs4 import BeautifulSoup

# Firebase Connection
def firebaseConnect():
	# Configuring connection to database
	config = {
	    'apiKey': "AIzaSyB-zW5qNKkTlfLzhbigIZkMWypJ4XMAAvY",
	    'authDomain': "cpanel-8d88a.firebaseapp.com",
	    'databaseURL': "https://cpanel-8d88a.firebaseio.com",
	    'projectId': "cpanel-8d88a",
	    'storageBucket': "cpanel-8d88a.appspot.com",
	    'messagingSenderId': "955905061850"
	  }

	returnData = dict()

	# Defining variable equal to database connection
	firebase = pyrebase.initialize_app(config)

	# Test Variables
	database = firebase.database()

	returnData['database'] = database

	# Defing users with
	authe = firebase.auth()

	returnData['authe'] = authe


	return returnData

# Twitter Connect
def twitterConnect():
	oauth = OAuth()
	twitter = oauth.remote_app(
		'twitter',
		consumer_key='QAlCACLnh0Zac3NgdgvXai4mo',
		consumer_secret='xU1L8fYe71matyfq2TNa6CpwVKbXTTS7Y60Sg1VJOmj4WBnjpY',
		base_url='https://api.twitter.com/1.1/',
		request_token_url='https://api.twitter.com/oauth/request_token',
		access_token_url='https://api.twitter.com/oauth/access_token',
		authorize_url='https://api.twitter.com/oauth/authorize'
		
	)
	return twitter

# Twitter webscrapping
def getTwitterData(username):
	r = rq.get('https://twitter.com/' + str(username))
	# print(r.text)
	soup = BeautifulSoup(r.text, 'html.parser')
	numberTags = soup.find('ul',{'class': 'ProfileNav-list'} )
	children = numberTags.findChildren("span" , recursive=True)
	# numberTagChildren
	# print(numberTags.prettify())
	info = {}
	counter = 0
	for child in children:
		# print(child.text)
		try:
			number = int(child.text)
			if counter == 0:
				info['tweets'] = number
			if counter == 1:
				info['following'] = number
			if counter == 2:
				info['followers'] = number
			if counter == 3:
				info['likes'] = number
			counter += 1
		except Exception as e:
			print('das tuff')
	# print(info)

	tweets = soup.find('div', {'class': 'stream'})
	# print(tweets.prettify())
	streamChildren = tweets.findChildren("p" , recursive=True)
	streamChildrenTime = tweets.findChildren("small" , recursive=True)
	tweets = []
	tweetTimes = []
	finalTweetData = []
	for child in streamChildren:
		wrongPTag = "@" + str(username) + " hasn't Tweeted yet."
		if wrongPTag in child.text:
			continue
		elif "Twitter may be over capacity or experiencing a momentary hiccup. Try again or visit Twitter Status for more information." in child.text:
			continue
		elif child.text == "Back to top ↑":
			continue

			tweets.append(child.text)
	for child in streamChildrenTime:
		# print(child.text)
		tweetTimes.append(child.text[1:-1])

	counterTimeIteration = 0
	for tweet in tweets:
		tweetDict = {}
		tweetDict['tweet'] = tweet
		for time in tweetTimes:
			# print(tweetTimes[counterTimeIteration])
			tweetDict['time'] = tweetTimes[counterTimeIteration]
			counterTimeIteration += 1
			break
		finalTweetData.append(tweetDict)	

	returnedData = [finalTweetData, info]
	return returnedData

# Website Scrapping
def websiteScrapping(website):
	print('aaalll')
	# Making Request
	r = rq.get(str(website))
	print('aaaaa\n\n\n\n')
	print(website)

	# Defining variable soup
	soup = BeautifulSoup(r.text, 'html.parser')

	# Getting header tags
	headerTags = soup.find('title').text

	# Define return list
	returnList = []
	linkList = []
	# Getting hrefs

	hrefs = soup.find_all('a')
	for href in hrefs:
		link = href['href']	
		if link == '/':
			continue
		if '/' in link:
			fullUrl = str(website) + str(link)
			linkList.append(fullUrl)


	returnList.append(headerTags)
	returnList.append(linkList)

	return returnList

# Google Search
def googleSearch(niche, location, start):
	title_list = []
	link_list = []

	# Getting user data to search
	url = "https://www.googleapis.com/customsearch/v1"
	userInput = str(niche) + " company in " + str(location)

	# Connect google
	parameters = {
		"q": userInput,
		"cx": '001120039411021127475:a4iq_yrptao',
		"key": 'AIzaSyCoVGR41c_O-q7Xz21FduFHtmm37azYTjQ',
		"start": start,
		# "siteSearch": "https://instagram.com"
	}
	page = requests.request("GET", url, params=parameters)
	results = json.loads(page.text)
	
	# Getting title and link through for loop
	for item in results['items']:
		link_list.append(item['link'])
		title_list.append(item['title'])

	returnedData = [title_list, link_list]
	return returnedData


# Instagram Scrapping
_user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
]
 
class InstagramScraper:
 
    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.proxy = proxy
 
    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)
 
    def __request_url(self, url):
        try:
            response = requests.get(url, headers={'User-Agent': self.__random_agent()}, proxies={'http': self.proxy,
                                                                                                 'https': self.proxy})
            response.raise_for_status()
        except requests.HTTPError:
            raise requests.HTTPError('Received non 200 status code from Instagram')
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response.text
 
    @staticmethod
    def extract_json_data(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)
 
    def profile_page_metrics(self, profile_url):
        results = {}
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        except Exception as e:
            raise e
        else:
            for key, value in metrics.items():
                if key != 'edge_owner_to_timeline_media':
                    if value and isinstance(value, dict):
                        value = value['count']
                        results[key] = value
                    elif value:
                        results[key] = value
        return results
 
    def profile_page_recent_posts(self, profile_url):
        results = []
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']["edges"]
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node)
        return results



