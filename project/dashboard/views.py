# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, Blueprint, request, jsonify, g, url_for, make_response

# Importing twitter api
from project.social_apis import twitterConnect, firebaseConnect, websiteScrapping, getTwitterData, InstagramScraper
InstagramScraper

# Importing Login Required
from project.decorators import login_required

# Importing formating function
from project.users.views import creationFormating

# Importing tips function
from project.api.views import tips, history, followerData, websites

# Importing counter tool
import itertools

# Importing time to 
from datetime import datetime

# Creating blueprint for app
dashboard = Blueprint('dashboard', __name__, static_folder='static' , template_folder='templates', static_url_path='/static/dashboard')

# FIREBASE AUTHENTICATION
databaseConnect = firebaseConnect()

database = databaseConnect['database']

authe = databaseConnect['authe']

# TWITTER OAUTH
twitter = twitterConnect()

@dashboard.route("/dashboard", methods=['GET', 'POST'])
@login_required
def home():
	# Checking if twitter oauth is in session
	if session.get('twitter_oauth') is not None:
		# Running twitter request function if session exist
		twitterRequest = requestTwitter()
	instagramRequest = requestInstagram()
	return render_template('dashboard/home.html')

# Setup and Website Update
@dashboard.route('/setup-update', methods=['GET', 'POST'])
def updateSetupAndWebsite():
	try:
		print('aaff\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		# Getting session data
		twitter_exist = session['userTwitterData']
		
		# Attemptingto sign in to backend
		user = session['user']

		# Assigning uid as a variable which will be used to go through branched in for loop
		uid = user['localId']
		setup_completed = { "setup_complete": True }

		# Adding Setup Complete to Database
		database.child("users").child(uid).child("account").update({ "setup_complete": True })

		session['setup_complete'] = True
		print('aaff\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		value = "success"

		websiteData = dict(database.child("users").child(uid).child("website").get().val())

		session['websiteData'] = websiteData
	except Exception as e:
		print("twiiter not connected")
		value = "Twitter not connected"
		return value

	# Trying to get and save required data
	try:
		# Getting database value
		databaseData = dict(database.child("users").child(uid).get().val())

		formatData = creationFormating(databaseData)

		returnedTips = tips(databaseData)
		session['tips'] = returnedTips

		websites = websites(databaseData)

		value = "success"
	except Exception as e:
		print("Session couldn't save")
		print(e)


	return redirect(url_for('dashboard.home'))

@twitter.tokengetter
def get_twitter_token():
	if 'twitter_oauth' in session:
		resp = session['twitter_oauth']
		return resp['oauth_token'], resp['oauth_token_secret']


@dashboard.before_request
def before_request():
	g.user = None
	if 'twitter_oauth' in session:
		g.user = session['twitter_oauth']


@dashboard.route('/twitter-getdata')
def index():
	tweets = None
	if g.user is not None:
		resp = twitter.request('statuses/home_timeline.json')
	if resp.status == 200:
		tweets = resp.data
		print(tweets)
	else:
		print('Unable to load tweets from Twitter.')
	return jsonify(tweets)

# Twitter Sign In function
@dashboard.route('/sign-in-twitter')
def twitterLogin():
	callback_url = url_for('dashboard.twitterOauthorized', next=request.args.get('next'))

	# callback_url = "http://localhost:5000/"
	return twitter.authorize(callback=callback_url)

# Getting multiple pages of followers using this function
def nextCursorFollowers(screen_name, followers, next_cursor):
	prev_cursor = followers['previous_cursor']
	# Creating List to hold list
	followersScreenNameList = []
	followersNameList = []

	nextCursor = twitter.request('followers/list.json?screen_name=' + screen_name + '&cursor=' + str(next_cursor))
	nextCursor = nextCursor.data
	
	# Creating For Loop to get all user screen names
	for cursorItem in nextCursor['users']:
		followersItemScreenName = cursorItem['screen_name']
		followersItemName = cursorItem['name']
		followersScreenNameList.append(followersItemScreenName)
		followersNameList.append(followersItemName)
	returnedCursor = nextCursor['next_cursor']
	returnedArray = [returnedCursor, followersScreenNameList, followersNameList]

	# print(followingScreenNameList)
	return returnedArray


@dashboard.route('/twitter-oauthorized')
def twitterOauthorized():
	print('dfdff')
	resp = twitter.authorized_response()
	print(resp)
	print('lll')
	if resp is None:
		print('You denied the request to sign in.')
	else:
		# Putting response in session
		session['twitter_oauth'] = resp

		# Running twitter request function
		twitterRequest = requestTwitter()
	return redirect(url_for('dashboard.home'))

@dashboard.route('/twitter-session-exist')
def sessionExist():
	print('session exist')
	try:

		# Running twitter request function
		twitterRequest = requestTwitter()
	except Exception as e:
		print(e)
		value = 'failed'
		flash(f'Twitter Refresh Failed')
		return redirect(url_for('dashboard.home'))
	return redirect(url_for('dashboard.home'))
# Requesting twitter function
def requestTwitter():
	try:
		# Creating List to hold data
		NumberOfTweets = []
		tweetText = []
		favoritesNumber = []
		retweets = []
		comments = []

		followersNameList = []
		followersScreenNameList = []


		followingNameList = []
		followingScreenNameList = []

		resp = session['twitter_oauth']
		screen_name = resp['screen_name']
		print(screen_name)

		# Getting User Time Line
		# timeline = twitter.request('statuses/home_timeline.json?count=200')
		# tweets = timeline.data
		# print('printing timeline\n\n\n\n\n\n\n\n')
		# print(tweets)

		# Getting User Followers
		getFollowers = twitter.request('followers/list.json?count=200')
		followers = getFollowers.data
		print('printing followers\n\n\n\n\n\n\n\n')
		print(followers)
		firstFollowersCursor = followers['next_cursor']
		firstFollowersPrevCursor = followers['previous_cursor']

		followersCursorList = [firstFollowersCursor]

		for followerItem in followers['users']:
			followerItemScreenName = followerItem['screen_name']
			followerItemName = followerItem['name']
			followersScreenNameList.append(followerItemScreenName)
			followersNameList.append(followerItemName)

		for i in itertools.count():
			print(followersCursorList[i])
			returnedList = nextCursorFollowers(screen_name, followers, followersCursorList[i])
			cursor = returnedList[0]
			if cursor == 0:	
				print("done")
				break
			else:
				userScreenNames = returnedList[1]
				userNames = returnedList[2]
				followersScreenNameList.append(userScreenNames)
				followersNameList.append(userNames)
				followersCursorList.append(cursor)
		print('printing followers\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		print(followersScreenNameList)
		print(followersNameList)
		print(len(followersScreenNameList))

		userData = twitter.request('users/show.json?screen_name=' + screen_name)
		userData = userData.data

		# Updating twitter data in firebase
		
		# Defining user info
		userLikes = {"user_likes" : userData['statuses_count']}
		userFollowers = {"followers_count" : userData['followers_count']}
		userFollowing = {"following_count" : userData['friends_count']}
		userScreenName = {"screen_name" : userData['screen_name']}
		userName = {"name" : userData['name']}
		bio = {"bio" : userData['description']}

		try:
			# Attemptingto sign in to backend
			print('aaa')
			print('session')
			print(session['user'])
			print('aaa')

			# Getting user from session

			user = session['user']
			
			print('second print section')
			# Assigning uid as a variable which will be used to go through branched in for loop
			uid = user['localId']
			print('third print section')

			# Getting current time 
			now = datetime.now()

			date_time = now.strftime("%m-%d-%Y")
			date_time_api = now.strftime("%m_%d_%Y")


			try:
				# Getting follower history
				historyData = dict(database.child("users").child(uid).child("twitter").child("history").get().val())

				# Counter variable
				print('aaakdmofbwfkgbnwrthirgnbiwsga\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

				counterFollowers = 0
				todayAlreadyIn = False
				followersDateList = []
				followersCountList = []
				print(historyData)

				# Checking if user is new if so updating data
				try:
					if historyData['followers'][0] == 'null':
						database.child("users").child(uid).child("twitter").child("history").child("followers").child(0).set({'followers_count': userData['followers_count'], 'date': date_time_api })
					if historyData['following'][0] == 'null':
						database.child("users").child(uid).child("twitter").child("history").child("following").child(0).set({'following_count': userData['following_count'], 'date': date_time_api })
				except Exception as e:
					print('not a new account')

				todayAlreadyIn = False
				for followerItem in historyData['followers']:
					if str(date_time_api) == followerItem['date']:
						todayAlreadyIn = True
						break
					else:
						counterFollowers += 1
				if todayAlreadyIn == False:
					database.child("users").child(uid).child("twitter").child("history").child("followers").child(counterFollowers).set({'followers_count': userData['followers_count'], 'date': date_time_api })

				print(historyData['followers'])

				counterFollowing = 0
				followingDateList = []
				followingCountList = []
				print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

				print(historyData)
				# Getting following
				for followingItem in historyData['following']:
					# Getting data
					date = followerItem['date']
					followingCount = followingItem['following_count']

					print(counter)
					print(date)
					print(followingCount)

					# Appending to list
					followingDateList.append(date)
					followingCountList.append(followingCount)
					counterFollowing += 1
					if date_time_api != followingDateList[-1]:
						database.child("users").child(uid).child("twitter").child("history").child("following").child(counterFollowing).update({'followers_count': userData['followers_count'], 'date': date_time_api })
						break
					else:
						continue
			except Exception as e:
				print('Exception for loop')
				print(e)
			
			# Saving Data as history

			# Unrequired data for setup
			try:
				# Getting website data
				websiteData = dict(database.child("users").child(uid).child("website").get().val())
				session['websiteData'] = websiteData
			except Exception as e:
				print('website not connected')
				print(e)

			print('aaaa')
		except Exception as e:
			value = 'failed'
			print(e)
			print('Twitter Login Failed1111')
			return redirect(url_for('dashboard.home'))

		# Trying to define username 
		try:
			print("screen name")
			username = userData['screen_name']
		except Exception as e:
			print("Error Defining username as screen name")
			username = database.child("users").child(uid).child("twitter").child("userData").child("screen_name").get().val()
			print(e)
		print("lllll\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

		# WEBSCRAPPING

		# Trying to run webscrapping function
		try:
			print('webscrapping')
			twitterScrapped = getTwitterData(username)
			tweets = twitterScrapped[0]
			twitterStats = twitterScrapped[1]
			database.child("users").child(uid).child("twitter").child("tweets").set(tweets)
		except Exception as e:
			print(e)


		# Saving data to firebase

		# Saving Userdata
		database.child("users").child(uid).child("twitter").child("userData").set(userData)
		print('aaad')
		# Updating followers info
		database.child("users").child(uid).child("twitter").child("followers").set(followers)
		print('aaad')

		databaseData = dict(database.child("users").child(uid).get().val())

		# Getting Tips
		returnedTips = tips(databaseData)
		session['tips'] = returnedTips
		print('aaaalllllaa')

		# Updating tips in firebase
		database.child("users").child(uid).child("tips").set(returnedTips)

		# Getting followers' data
		followersData = followerData(databaseData)
		session['followersData'] = followersData
		print('aaall')
		value = 'success'
		print(value)

		# Saving formated follower data
		database.child("users").child(uid).child("twitter").child("followersFormated").set(followersData)

		print('aaaa\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		# Formating Twitter Data
		formatData = creationFormating(databaseData)
		print('aaaa')


		# Getting history
		historyData = history(databaseData)
		print('a')
		session['history'] = historyData
		print('aaaa')

		print(databaseData)

		return value
	except Exception as e:
		 print(e)
		 print('Twitter Login Failed')
		 return redirect(url_for('dashboard.home'))
	# Twitter Search Function Terms

# Instagram 
def requestInstagram():
	
	try:
		print("Request Instagram\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
		# Getting user from session
		user = session['user']
		print(user)
		# Assigning uid as a variable which will be used to go through branched in for loop
		uid = user['localId']
		print('aaa')

		# Checking if instagram is connected
		try:
			instagramData = dict(database.child("users").child(uid).child("instagram").get().val())
			session['userInstagramData'] = instagramData
		except Exception as e:
			print('instagram not connected')

		# Getting Data
		try:
			print('aaa')

			username = database.child("users").child(uid).child("instagram").child("username").get().val()
			instagramConnection = InstagramScraper()
			results = instagramConnection.profile_page_metrics('https://www.instagram.com/' + username + '/')
			print('asddaa')
			print(results)
			numberOfFollowers = results['edge_followed_by']
			numberOfFollowing = results['edge_follow']
			print('aa')
		except Exception as e:
			print("Instagram not connected")
			print(e)
			return redirect(url_for('dashboard.home'))

		# Getting current time 
		now = datetime.now()

		date_time = now.strftime("%m-%d-%Y")
		date_time_api = now.strftime("%m_%d_%Y")
		print(numberOfFollowers)
		print(numberOfFollowing)
		# Instagram History
		historyData = dict(database.child("users").child(uid).child("instagram").child("history").get().val())

		counterFollowers = 0
		todayAlreadyInFollowers = False
		followersDateList = []
		followersCountList = []
		
		# Checking if user is new if so updating data
		try:
			if historyData['followers'][0] == 'null':
				database.child("users").child(uid).child("instagram").child("history").child("followers").child(0).set({'followers_count': numberOfFollowers, 'date': date_time_api })
			if historyData['following'][0] == 'null':
				database.child("users").child(uid).child("instagram").child("history").child("following").child(0).set({'following_count': numberOfFollowing, 'date': date_time_api })
		except Exception as e:
			print('not a new account')

		for followerItem in historyData['followers']:
			if str(date_time_api) == followerItem['date']:
				todayAlreadyInFollowers = True
				break
			else:
				counterFollowers += 1
		if todayAlreadyInFollowers == False:
			database.child("users").child(uid).child("instagram").child("history").child("followers").child(counterFollowers).set({'followers_count': numberOfFollowers, 'date': date_time_api })

		# Adding following history
		counterFollowing = 0
		todayAlreadyInFollowing = False
		followingDateList = []
		followingCountList = []

		for followingItem in historyData['following']:
			if str(date_time_api) == followingItem['date']:
				todayAlreadyInFollowing = True
				break
			else:
				counterFollowing += 1
		if todayAlreadyInFollowing == False:
			database.child("users").child(uid).child("instagram").child("history").child("following").child(counterFollowing).set({'following_count': numberOfFollowing, 'date': date_time_api })

	except Exception as e:
		print(e)
		print('Instagram Get Data failed')
		return redirect(url_for('dashboard.home'))

