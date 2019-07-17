# Importing all needed Flask classes
from flask import Flask, session, redirect, Blueprint, request, jsonify, g, url_for, make_response, Response, flash

# Firebase connection
from project.social_apis import firebaseConnect, websiteScrapping, googleSearch, getTwitterData, InstagramScraper

# Tools for for loops
import itertools

# Importing random
import random

# Importing time 
from datetime import datetime

api = Blueprint('api', __name__)

# FIREBASE AUTHENTICATION
databaseConnect = firebaseConnect()

database = databaseConnect['database']

authe = databaseConnect['authe']

# Website
def websites(userReturn):
	websiteData = dict()
	try:
		# Saving required variables
		websiteName = userReturn['website']['website_name']
		websiteUrl = userReturn['website']['website_url']

		websiteData['website_name'] = websiteName
		websiteData['website_url'] = websiteUrl
		
		# Trying other variables
		try:
			headerText = userReturn['website']['header_text']
			links = userReturn['website']['links']
			websiteData['header_text'] = headerText
			websiteData['links'] = links
		except Exception as e:
			print(e)
		print('\n\n\n\n\n\n\n\n\n\n\n\n')
		print(websiteData)
		return websiteData
	except Exception as e:
		 print('Getting Website failed')
		 print(e)

# Tips
def tips(userReturn):
	tips = []
	print('aaaa')
	try:
		# Defining variables

		print(userReturn)
		historyData = history(userReturn)
		# twitter tips
		try:
			print('twiterrerTips\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
			twitterConnected = True

			# Twitter variables
			twitterDescription = userReturn['twitter']['description']
			twitterName = userReturn['twitter']['name']
			twitterLocation = userReturn['twitter']['location']
			twitterFollowing = userReturn['twitter']['following']
			twitterFollowers = userReturn['twitter']['followers']

			twitterDescriptionLen = len(twitterDescription)

			print('\n\n\n\n\n\n\n\n\n\n\n')
			print(twitterFollowers)
			twitterFollowerNumberList = historyData['twitter'][1]
			print(twitterFollowerNumberList)

			# Finding out static trend with for loop
			twitterFollowersDaysStatic = 0
			for i in itertools.count():
				if i == 0:
					i += 1
				print('aaaaaaa')
				print(twitterFollowerNumberList[-i])
				print(twitterFollowerNumberList[-i + 1])
				print(i)
				print(twitterFollowerNumberList)
				if i == len(twitterFollowerNumberList):
					break
				if twitterFollowerNumberList[-i] == twitterFollowerNumberList[-i - 1]:
					twitterFollowersDaysStatic += 1
					print(twitterFollowersDaysStatic)
				else:
					break
			print('\n\n\n\n\n\n\n\n\n\n\n\n\ndaysStatic')
			print(twitterFollowersDaysStatic)

			# Twitter tips
			if twitterDescriptionLen < 128:
				twitterDescriptionLenMessage = "Only " + str(twitterDescriptionLen) + "/160 of your characters have been used for your twitter description. Explain who you are!"
				tips.append(twitterDescriptionLenMessage)
			if "#" not in twitterDescription:
				twitterDescriptionNoHashtagsMessage = "No Hashtags Found. Try adding hashtags to your twitter description!"
				tips.append(twitterDescriptionNoHashtagsMessage)
			if twitterLocation == "":
				twitterLocationIsNoneMessage = "No location found! Add your location on twitter so your followers know if your close or not!"
				tips.append(twitterLocationIsNoneMessage)
			if twitterFollowersDaysStatic >= 3:
				twitterFollowersDaysStaticMessage = "Followers on twitter haven't changed in the last " + str(twitterFollowersDaysStatic) + " days. Try posting more and engaging with people."
				tips.append(twitterFollowersDaysStaticMessage)
			if twitterFollowing < 100:
				twitterFollowingTips = "You are only following " + str(twitterFollowing) + " people on twitter. Try following more people in your niche."
				tips.append(twitterFollowingTips)
		except Exception as e:
			twitterConnected = False
			print(e)
			print('no twitter')
		try:
			instagramConnected = True

			# Defining instagram data
			instagramBio = userReturn['instagram']['biography']
			instagramName = userReturn['instagram']['username']
			instagramFollowing = userReturn['instagram']['edge_follow']
			instagramBioLen = len(instagramBio)
			instagramFollowerNumberList = historyData['instagram'][1]

			# Finding instagram data trends
			instagramFollowersDaysStatic = 0
			for i in itertools.count():
				if i == 0:
					i += 1
				print('aaaaaaa')
				print(instagramFollowerNumberList[-i])
				print(instagramFollowerNumberList[-i + 1])
				print(i)
				print(instagramFollowerNumberList)
				if i == len(instagramFollowerNumberList):
					break
				if instagramFollowerNumberList[-i] == instagramFollowerNumberList[-i - 1]:
					instagramFollowersDaysStatic += 1
					print(instagramFollowersDaysStatic)
				else:
					break

			# Instagram tips
			if instagramBioLen < 120:
				instagramBioLenMessage = "Only " + str(instagramBioLen) + "/150 of your characters have been used for your instagram bio. Explain who you are!"
				tips.append(instagramBioLenMessage)
			if "#" not in instagramBio:
				instagramBioNoHashtagsMessage = "No Hashtags Found. Try adding hashtags to your instagram bio!"
				tips.append(instagramBioNoHashtagsMessage)
			if instagramFollowersDaysStatic >= 3:
				instagramFollowersDaysStaticMessage = "Followers on twitter haven't changed in the last " + str(instagramFollowersDaysStatic) + " days. Try posting more and engaging with people."
				tips.append(instagramFollowersDaysStaticMessage)
			if instagramFollowing < 100:
				instagramFollowingTips = "You are only following " + str(instagramFollowing) + " people on instagram. Try following more people in your niche."
				tips.append(instagramFollowingTips)

		except Exception as e:
			instagramConnected = False
			print(e)
			print('no instagram')
		# Trying to give other tips
		try:
			websiteConnected = True
			# Getting website title text
			websiteHeader = userReturn['website']['header_text']

			# Making both strings uppercase to identify same letters
			websiteHeader = websiteHeader.upper()
			websiteName = websiteName.upper()
			if websiteName not in websiteHeader:
				websiteInTitleMessage = "Your website/business name is not in your url. Try finding a domain that fits"
				tips.append(websiteInTitleMessage)

			if websiteName in twitterName or twitterName in websiteName:
				pass
			else:
				websiteNameMessage = "Website name and twitter name are not simular. Try to make it simular!"			
			x = 0
			for link in websiteLinks:
				if 'about' in link:
					x += 1
			if x == len(websiteLinks):
				websiteLinkTips = "Doesn't seem linke you have an about link on your homepage. Tell people who you are!"
				tips.append(websiteLinkTips)
		except Exception as e:
			websiteConnected = False
			print('no unrequired tips')
			print(e)

		# Competition
		competition = userReturn['competition']

		if competition['title'][0] == 'null':
			competitionNoneTip = "Find your competition as soon as possible"
			tips.append(competitionNoneTip)


		# If conditions are true tips will be given to user
		
		# Instagram tips
		try:
			print('instagram')

		except Exception as e:
			raise e

		# Website tips
		
		# Trying to get website variables
		try:
			websiteName = userReturn['website']['website_name']
			websiteUrl = userReturn['website']['website_url']
			websiteLinks = userReturn['website']['links']
			
		except Exception as e:
			print('Website tips not working/setup')
			print(e)

		if 'websiteName' in locals() and 'websiteUrl' in locals():
			if websiteName == '' and websiteUrl == '':
				websiteNotExist = "Website not connected we recommend you connect it as soon as possible."
				tips.append(websiteNotExist)
		else:
			websiteNotExist = "Website not connected we recommend you connect it as soon as possible."
			tips.append(websiteNotExist)

		print('tips')
		print(tips)
		return tips

	except Exception as e:
		print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\ntips error')
		print(e)

# Getting statistics
def statistics(userReturn, uid):
	try:
		print('statsasfswef\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		returnedData = {}
		historyData = history(userReturn)

		# Checking if twitter is connected
		try:
			twitterFollowerNumberList = historyData['twitter'][1]
			twitterConnected = True
		except Exception as e:
			print(e)
			print('twitter not connected stats')
			twitterConnected = False

		# Checking if instagram is connected
		try:
			instagramFollowerNumberList = historyData['instagram'][1]	
			instagramConnected = True
		except Exception as e:
			print(e)
			print('instagram not connected stats')
			instagramConnected = False
		
		# Followers min, max, and average
		totalFollowersList = []
		if twitterConnected == True:
			for number in twitterFollowerNumberList:
				print(number)
				totalFollowersList.append(number)
		if instagramConnected == True:
			for number in instagramFollowerNumberList:
				print(number)
				totalFollowersList.append(number)
		print(len(totalFollowersList))
		# if len(totalFollowersList) > 1:
		# 	totalFollowersList = [sum(x) for x in zip(*totalFollowersList)]
		

		print("totalFollowersList")
		print(totalFollowersList)
		# Doing math
		lowestAmountOfFollowers = min(totalFollowersList)
		highestAmountOfFollowers = max(totalFollowersList)

		# Getting sum of list
		sumOfFollowersList = 0
		print("totalFollowersList")
		for number in totalFollowersList:
			print(number)
			sumOfFollowersList+=number
		averageAmountOfFollowers = sumOfFollowersList / len(totalFollowersList)
		print("totalFollowersList")

		# Saving data to dict
		returnedData['minFollowers'] = lowestAmountOfFollowers
		returnedData['maxFollowers'] = highestAmountOfFollowers
		returnedData['avgFollowers'] = round(averageAmountOfFollowers, 2)	
		print("totalFollowersList")
		print(returnedData)
		try:
			numberOfLikesList = []
			numberOfCommentsList = []
			lenOfDescriptionList = []
			instagramPosts = userReturn['instagram']['instagramPosts']
			
			# Running for loop to get data
			for post in instagramPosts:
				numberOfLikes = post['number_of_likes']
				numberOfLikesList.append(numberOfLikes)

				numberOfComments = post['number_of_comments']
				numberOfCommentsList.append(numberOfComments)

				lenOfDescription = post['caption']
				lenOfDescriptionList.append(len(lenOfDescription))

			totalNumberOfLikes = sum(numberOfLikesList) 
			totalNumberOfComments = sum(numberOfCommentsList) 
			totalLenOfDescription = sum(lenOfDescriptionList)

			# Saving data in variable
			instagramRecentAvgLikes = round(totalNumberOfLikes / len(instagramPosts), 1)
			instagramRecentAvgComments = round(totalNumberOfComments / len(instagramPosts), 1)
			instagramRecentAvgDescriptionLen = round(totalLenOfDescription / len(instagramPosts), 1)
			print(returnedData)
			instagramStats = { "instagramRecentAvgLikes" : instagramRecentAvgLikes, "instagramRecentAvgComments" : instagramRecentAvgComments, "instagramRecentAvgDescriptionLen" : instagramRecentAvgDescriptionLen }
			returnedData['instagramStats'] = instagramStats


		except Exception as e:
			print(e)
			print('failed to get instagram statistics')
		return returnedData
	except Exception as e:
		print(e)
		print('statistics failed')
		return 'failed'

# Get History
def history(userReturn):
	print('historyaaaa')
	print(userReturn)

	try:
		returnedData = dict()
		try:
			historyInstagram = userReturn['instagram']['history']
			instagramDateList = []
			instagramFollowerList = []
			for followerItem in historyInstagram['followers']:
				print(followerItem)
				date = followerItem['date']
				followersCount = followerItem['followers_count']
				instagramDateList.append(date)
				instagramFollowerList.append(followersCount)
			instagramData = []
			instagramData.append(instagramDateList)
			instagramData.append(instagramFollowerList)
			returnedData['instagram'] = instagramData
		except Exception as e:
			print(e)
			print("instagram no history")

		try:
			print(userReturn['twitter']['history'])
			# print("userReturn['twitter']['history']")
			historyTwitter = userReturn['twitter']['history']
			print('aaaa')
			twitterDateList = []
			twitterFollowerList = []
			print('aggg')
			for followerItem in historyTwitter['followers']:
				print(followerItem)
				date = followerItem['date']
				followersCount = followerItem['followers_count']

				# Appending to list
				twitterDateList.append(date)
				twitterFollowerList.append(followersCount)
			twitterData = []
			twitterData.append(twitterDateList)
			twitterData.append(twitterFollowerList)
			returnedData['twitter'] = twitterData
		except Exception as e:
			print(e)
			print("twitter no history")
		return returnedData
	except Exception as e:
		print('Trouble getting history')
		print(e)

# Getting followers' data
def followerData(userReturn):
	try:
		print('followw\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		followersLocatonList = []
		followersNameList = []
		print(userReturn)
		# Getting followers info from database
		followers = userReturn['twitter']['followers']['users']

		# counter
		x = 0

		# For loop getting location and name
		for follow in followers:
			x += 1
			followerLocation = follow['location']
			print(followerLocation)
			followersLocatonList.append(followerLocation)

			followerName = follow['name']
			print(followerName)

			followersNameList.append(followerName)

			if x > 9:
				break
		print(followersLocatonList)
		print(followersNameList)
		data = {}
		data['name'] = followersNameList
		data['location'] = followersLocatonList
		print('\n\n\n\n\n\n\n\n\n\n\n\n')
		return data
	except Exception as e:
		print('Trouble getting follower data returned')
		print(e)

def instagramPostsFormat(instagramPosts):
	print(instagramPosts)
	formattedDictionary = []
	for post in instagramPosts:
		postDict = {}
		picUrl = post['display_url']
		numberOfLikes = post['edge_liked_by']['count']
		numberOfComments = post['edge_media_to_comment']['count']
		pictureText = post['accessibility_caption']
		caption = post['edge_media_to_caption']['edges'][0]['node']['text']

		postDict['pic_url'] = picUrl
		postDict['number_of_likes'] = numberOfLikes
		postDict['number_of_comments'] = numberOfComments
		postDict['picture_text'] = pictureText
		postDict['caption'] = caption
		formattedDictionary.append(postDict)
	return formattedDictionary

def itemStats(userReturn, uid):
	print("userRgqergqergwrtgwrtgeturn\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
	try:
		instagramPosts = userReturn['instagram']['instagramPosts']
		instagramStats = userReturn['statistics']
		for post in instagramPosts:
			success = 0
			tips = []
			if post['number_of_comments'] > instagramStats['instagramRecentAvgComments']:
				success += 1
			if post['number_of_likes'] > instagramStats['instagramRecentAvgLikes']:
				success += 1
			if len(post['caption']) > instagramStats['instagramRecentAvgDescriptionLen']:
				success += 1

			if len(post['caption']) < 20:
				tip = "This caption is definately too short. In the future go into more detail"
				tips.append(tip)
			# database.child("users").child(uid).child("")
	except Exception as e:
		print("Instagram not connected item stats")

# Sign Up Function
@api.route("/create-user", methods=['GET', 'POST'])
def signUp():
	
	# Getting posted data and putting it in a dictionary
	print(request.get_json)
	print(request.json)
	# Assigning variables to sign in to database
	firstname = request.json['firstname']
	lastname = request.json['lastname']
	email = request.json['email']
	password = request.json['password']
	software = request.json['software']


	createdUser = createUserFunc(email, password, firstname, lastname, software)
	return jsonify(createdUser)

# Signin function
def createUserFunc(email, password, firstname, lastname, software):
	try:
		userReturn = []
		userData = dict()
		userData['firstname'] = firstname
		userData['lastname'] = lastname
		userData['password'] = password
		userData['email'] = email

		# Attemptingto sign in to backend
		user = authe.create_user_with_email_and_password(email,password)

		# Assigning json data to variable to return to database
		userAccount = {"firstname" : firstname, "lastname" : lastname, "email" : email, "setup_complete" : False, "niche" : ""}

		# Assigning uid which will be used to create paths in database
		uid = user['localId']

		# Website empty json
		addWebsite = { "website_name" : '', "website_url" : '', "header_text" : "", "links": ["null"] }

		# Making empty json for twitter
		addTwitterDefault = {"followers":0, "following": 0, 'likes': 0, "username": ''}
		addTwitterTweetDefault = { "time" : "", "tweet" : "" }

		addInstagramDefault = { "biography" : "", "business_category_name" : "", "edge_felix_video_timeline" : 0, "edge_follow" : 0, "edge_followed_by" : 0, "edge_media_collections" : 0, "edge_mutual_followed_by" : 0, "edge_saved_media" : 0, "external_url" : "", "external_url_linkshimmed" : "", "full_name" : "" }
		addInstagramPostDefault = [{ "caption" : "", "number_of_comments" : 0, "number_of_likes" : 0, "pic_url" : "", "picture_text" : "", "tips" : ["null"], " success": 0 }]

		# Creating branches
		database.child("users").child(uid).child("account").set(userAccount)
		database.child("users").child(uid).child("website").set(addWebsite)
		database.child("users").child(uid).child("user").set(user)
		database.child("users").child(uid).child("twitter").set(addTwitterDefault)
		database.child("users").child(uid).child("twitter").child("history").child("followers").set(['null'])
		database.child("users").child(uid).child("twitter").child("history").child("following").set(['null'])
		database.child("users").child(uid).child("twitter").child("tweets").set(addTwitterTweetDefault)
		database.child("users").child(uid).child("instagram").set(addInstagramDefault)
		database.child("users").child(uid).child("instagram").child("instagramPosts").set(addInstagramPostDefault)
		database.child("users").child(uid).child("instagram").child("history").child("followers").set(['null'])
		database.child("users").child(uid).child("instagram").child("history").child("following").set(['null'])
		database.child("users").child(uid).child("competition").child("link").set(['null'])
		database.child("users").child(uid).child("competition").child("title").set(['null'])
		database.child("users").child(uid).child("tips").set(['null'])
		database.child("users").child(uid).child("statistics").child("maxAmountOfFollowers").set(0)
		database.child("users").child(uid).child("statistics").child("minAmountOfFollowers").set(0)
		database.child("users").child(uid).child("statistics").child("averageAmountOfFollowers").set(0.0)
		database.child("users").child(uid).child("statistics").child("instagramRecentAvgLikes").set(0.0)
		database.child("users").child(uid).child("statistics").child("instagramRecentAvgComments").set(0.0)
		database.child("users").child(uid).child("statistics").child("instagramRecentAvgDescriptionLen").set(0.0)
		database.child("users").child(uid).child("statistics").child("twitterRecentAvgLikes").set(0.0)
		database.child("users").child(uid).child("statistics").child("twitterRecentAvgComments").set(0.0)
		database.child("users").child(uid).child("statistics").child("twitterRecentAvgDescriptionLen").set(0.0)


	except Exception as e:
		print("problem with creation")
		print(e)
		userData['message'] = 'failed'
		return jsonify(userData)
	
	# Appending data into list ready to return
	userReturn.append(userData)
	userReturn.append(user)
	
	print(userReturn)
	userData['message'] = 'success'

	return userReturn


# Signin Function
@api.route("/signin", methods=['GET', 'POST'])
def signIn():
	# Getting posted data and putting it in a dictionary
	print(request.get_json)
	print(request.json)

	# Getting email and pass
	email = request.json['email']
	password = request.json['password']
	software = request.json['software']

	# Assigning variables to sign in to database
	signIn = signInFunc(email, password)

	print(software)
	if software == "ios":
		print('signIn\n\n\n\n\n\n\n')
		# # Deleting dictionaries from data
		# try:
		# 	del signIn['twitter']['followers']
		# except Exception as e:
		# 	print(e)
		# 	print('Deleting followers failed')
		# try:
		# 	del signIn['user']
		# except Exception as e:
		# 	print(e)
		# 	print('Deleting user failed')
		# try:
		# 	del signIn['twitter']['userData']['entities']
		# except Exception as e:
		# 	print(e)
		# 	print('Deleting userdata entities failed')
		
		# signIn['message'] = 'success'
		# print(signIn)

	return jsonify(signIn)

# Signin function
def signInFunc(email, password):
	# Creating list ready to return later
	userData = dict()
	try:
		# Attemptingto sign in to backend
		user = authe.sign_in_with_email_and_password(email, password)
		print(user)

		# Assigning uid as a variable which will be used to go through branched in for loop
		uid = user['localId']

		# Creating dict to store data from database
		print(user['localId'])
		userReturn = dict(database.child("users").child(uid).get().val())
		

		update = dataUpdating(uid)

	except Exception as e:
		print("Signin error below")
		print(e)
		userData['message'] = 'failed'
		return jsonify(userData)

	try:
		instagramPosts = userReturn['instagram']['instagramPosts']
		formatedPostData = instagramPostsFormat(instagramPosts)
		del userReturn['instagram']['instagramPosts']
		userReturn['instagram']['instagramPosts'] = formatedPostData
	except Exception as e:
		print(e)

	# Appending valid formated data to final dictionary
	# userReturn['user'] = user
	# userReturn['history'] = historyReturned
	# userReturn['website'] = websitesData

	# print('ppppppp\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
	# print(competition)
	# for i in competition:
	# 	print(i)

	# print('pppp\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

	# userReturn['tips'] = returnedTips
	# userReturn['competition'] = competition

	# print(userReturn)
	print('aaalaaaalllalaasdgergertg\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
	# Returning main data
	return userReturn

# Signout Function
@api.route("/signout", methods=['POST'])
def signOut():
	if 'email' in session:
		session.clear()
	else:
		returnValue = 'No one is logged in'

	return jsonify({ 'message' : returnValue})

# Connect Website
@api.route("/connect-website", methods=['GET','POST'])
def connectWebsite():
	userData = dict()
	userReturn = []
	try:
		# Defining variables
		websiteName = request.form['website_name']
		websiteUrl = request.form['website_url']

		if websiteName is not None and websiteUrl is not None:
			print('aaa')
			websiteScrap = websiteScrapping(websiteUrl)
			print('aaa')
			
			websiteData = { "website_name" : websiteName, "website_url" : websiteUrl, "header_text" : websiteScrap[0], "links" : websiteScrap[1] }
			print('aaa')

			# Putting them into sessions
			session['websiteData'] = websiteData

			# Importing data in firebase
			user = session['user']

			uid = user['localId']

			database.child("users").child(uid).child("website").set(websiteData)
			value = 'success'
		else:
			value = 'failed'
		return jsonify(value)
	except Exception as e:
		print('Not dashboard\n\n\n\n\n\n\n')
		print(e)
		print("d")

		# API Request
		try:
			print(request.get_json())

			# Getting posted data
			userData['website_name'] = request.get_json()['website_name']
			userData['website_url'] = request.get_json()['website_url']

			# Defining variables
			websiteName = userData['website_name']
			websiteUrl = userData['website_url']
			
			websiteScrap = websiteScrapping(website_url)
			
			addWebsite = { "website_name" : website_name, "website_url" : website_url, "header_text" : websiteScrap[0], "links" : websiteScrap[1] }

			# Importing data in firebase
			database.child("users").child(uid).child("website").set(websiteData)

			return jsonify(userData)
		except Exception as e:
			 print('opperation failed')
			 print(e)
			 value = 'failed'

			 return jsonify(value)

# Disconnect website function
@api.route("/disconnect-website", methods=['GET','POST'])
def disconnectWebsite():
	try:

		# Getting firebase data
		user = session['user']
		uid = user['localId']

		# Returning website data to default 
		addWebsite = { "website_name" : '', "website_url" : '' }
		database.child("users").child(uid).child("website").set(addWebsite)

		# Trying to put data in session
		try:
			session['websiteData'] = dict(database.child("users").child(uid).child("website").get().val())
		except Exception as e:
			 print('failed to add session')
			 print(e)

		value = 'success'
	except Exception as e:
		 print('Disconnect Failed')
		 print(e)

	return value

# Posting niche
@api.route("/post-niche", methods=['GET','POST'])
def postNiche():
	try:
		print('aaaaaa\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		nichePost = request.form['niche_text']
		
		# Getting data from firebase
		user = session['user']
		uid = user['localId']

		location = database.child("users").child(uid).child("twitter").child("userData").child("location").get().val()
		
		# Getting competitiors on google
		searchResults = googleSearch(nichePost, location, 1)
		print(searchResults)
		compDict = {}
		compDict['link'] = searchResults[1]
		compDict['title'] = searchResults[0]

		# Putting niche in database
		database.child("users").child(uid).child("account").update({'niche' : nichePost })

		# Putting competitors in database
		database.child("users").child(uid).child("competition").set(compDict)
		print('aaaaaa')

		# Putting data in session
		session['competition'] = compDict

		value = 'success'
	except Exception as e:
		print('niche post failed')
		print(e)
		value = 'failed'
	return value

# Disconnecting niche and competition
@api.route("/disconnect-niche", methods=['GET','POST'])
def disconnectNiche():
	try:
		print('disconnecting')
		# Getting firebase data
		user = session['user']
		uid = user['localId']


		# Putting niche in database
		database.child("users").child(uid).child("account").update({'niche' : '' })

		# Resetting competitors in database
		database.child("users").child(uid).child("competition").child("link").set(['null'])
		database.child("users").child(uid).child("competition").child("title").set(['null'])

		# Popping niche from session
		session.pop('competition', None)

		# Assigning message
		value = 'success'
	except Exception as e:
		print(e)
		value = 'failed'
	return value


@api.route("/refresh-search", methods=['GET','POST'])
def refreshSearch():
	try:
		print('aaaaa')
		# Getting firebase data
		user = session['user']
		uid = user['localId']

		# Getting parameter data from firebase
		niche = database.child("users").child(uid).child("account").child("niche").get().val()
		location = database.child("users").child(uid).child("twitter").child("userData").child("location").get().val()

		# Running function
		randomInt = random.randint(1,7)
		searchResults = googleSearch(niche, location, randomInt)

		compDict = {}
		compDict['link'] = searchResults[1]
		compDict['title'] = searchResults[0]
		print(searchResults)

		# Putting data back in firebase
		database.child("users").child(uid).child("competition").set(compDict)

		session['competition'] = compDict

		value = 'success'
	except Exception as e:
		print('Refresh search failed')
		print(e)
		value = 'failed'

	return value

@api.route("/refresh-followers", methods=['GET','POST'])
def refreshFollowers():
	print('aaaaa')
	try:

		currentFollowersShowingName = []
		currentFollowersShowingLocation = []
		followersLocatonList = []
		followersNameList = []
		print('aaaaa')

		# Getting firebase data
		user = session['user']
		uid = user['localId']

		# Getting number of followers
		followers = database.child("users").child(uid).child("twitter").child("followers").child("users").get().val()

		for currentItem in session['followersData'][0]:
			currentFollowersShowingName.append(currentItem)

		for currentItem in session['followersData'][1]:
			currentFollowersShowingLocation.append(currentItem)

		print()
		# counter
		x = 0
		print('aaaaa')

		# For loop getting location and name
		for follow in followers:

			# Checking if name is current
			if follow['name'] in currentFollowersShowingName:
				print('found')
				continue
			x += 1
			followerLocation = follow['location']
			print(followerLocation)
			followersLocatonList.append(followerLocation)

			followerName = follow['name']
			print(followerName)

			followersNameList.append(followerName)

			if x > 9:
				break

		print("x")
		print(x)
		if x < 9:
			print('aaaaa')
			for currentItem in currentFollowersShowingName:
				print(currentItem)
				currentFollowerName = currentItem
				followersNameList.append(currentFollowerName)

			for currentItem in currentFollowersShowingLocation:
				x += 1
				currentFollowerLocation = currentItem
				followersLocatonList.append(currentFollowerLocation)

				if x > 9:
					break
		print(followersNameList)
		print(followersLocatonList)

		data = []
		data.append(followersNameList)
		data.append(followersLocatonList)
		print(data)
		session['followersData'] = data
		value = 'success'
	except Exception as e:
		print(e)
		value = 'failed'

	return value

@api.route("/connect-instagram-api", methods=['GET','POST'])
def connectInstagramAPI():
	try:
		print('connecting instagram api\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		username = request.form['instagram-username']
		returnedData = connectInstagram(username)
		if returnedData == 'failed':
			flash('Connecting Instagram Failed')
			return redirect(url_for('dashboard.home'))
		# Getting user session
		user = session['user']
		uid = user['localId']

		database.child("users").child(uid).child("instagram").update(returnedData[0])
		databaseData = dict(database.child("users").child(uid).get().val())
		instagramDataFomated = instagramPostsFormat(returnedData[1])
		try:
			database.child("users").child(uid).child("instagram").child("instagramPosts").update(instagramDataFomated)
		except Exception as e:
			print(e)
			database.child("users").child(uid).child("instagram").child("instagramPosts").set(instagramDataFomated)
		return redirect(url_for('dashboard.home'))
		print('erghwrthwjrkthjwrt hkwrth\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		session['userInstagramData'] = databaseData['instagram']
	except Exception as e:
		print(e)
		username = request.get_json()['username']
		returnedData = connectInstagram(username)
		database.child("users").child(uid).child("instagram").update(returnedData[0])
		instagramDataFomated = instagramPostsFormat(returnedData[1])
		database.child("users").child(uid).child("instagram").child("instagramPosts").update(instagramDataFomated)
		return returnedData

# Connect instagram function
def connectInstagram(username):
	print('connecting instagram')
	url = 'https://www.instagram.com/' + username + '/'
	instagramConnection = InstagramScraper()
	results = instagramConnection.profile_page_metrics(url)
	instagramPosts = instagramConnection.profile_page_recent_posts(url)
	if not results:
		print('account private')
		return 'failed'
	try:
		private = results['is_private']
		print(private)
	except Exception as e:
		print(e)
		results['is_private'] = 'false'
	returnedData = [results,instagramPosts]
	return returnedData

# Disconnect instagram
@api.route("/disconnect-instagram", methods=['GET', 'POST'])
def disconnectInstagramAPI(uid):
	print('aadfsdfsf')

	addInstagramDefault = { "biography" : "", "business_category_name" : "", "edge_felix_video_timeline" : 0, "edge_follow" : 0, "edge_followed_by" : 0, "edge_media_collections" : 0, "edge_mutual_followed_by" : 0, "edge_saved_media" : 0, "external_url" : "", "external_url_linkshimmed" : "", "full_name" : "" }
	addInstagramPostDefault = [{ "caption" : "", "number_of_comments" : 0, "number_of_likes" : 0, "pic_url" : "", "picture_text" : "", "tips" : ["null"], " success": 0 }]

	# Setting instagram data back to default
	database.child("users").child(uid).child("instagram").remove()
	database.child("users").child(uid).child("instagram").child("history").child("followers").set(['null'])
	database.child("users").child(uid).child("instagram").child("history").child("following").set(['null'])
	database.child("users").child(uid).child("instagram").set(addInstagramDefault)
	database.child("users").child(uid).child("instagram").child("instagramPosts").set(addInstagramPostDefault)

# Disconnect twitter
@api.route("/disconnect-twitter", methods=['GET', 'POST'])
def disconnectTwitterAPI(uid):
	try:
		user = session['user']
		uid = session['localId']
		print('aadfsdfsf')

		addTwitterDefault = {"followers":0, "following": 0, 'likes': 0, "username": ''}
		addTwitterTweetDefault = { "time" : "", "tweet" : "" }

		# Setting twitter data back to default
		database.child("users").child(uid).child("twitter").remove()
		database.child("users").child(uid).child("twitter").set(addTwitterDefault)
		database.child("users").child(uid).child("twitter").child("history").child("followers").set(['null'])
		database.child("users").child(uid).child("twitter").child("history").child("following").set(['null'])
		database.child("users").child(uid).child("twitter").child("tweets").set(addTwitterTweetDefault)

	except Exception as e:
		print(e)
# def disconnectTwitter(uid):

@api.route("/connect-twitter-api", methods=['GET','POST'])
def connectTwitterAPI():
	try:
		print('connecting instagram api')
		print(request.form)
		username = request.form['twitter-username']
		returnedData = connectTwitter(username)
		if returnedData == 'failed':
			flash('Connecting Twitter Failed')
			return redirect(url_for('dashboard.home'))
		# Getting user session
		user = session['user']
		uid = user['localId']
		database.child("users").child(uid).child("twitter").update(returnedData[1])
		database.child("users").child(uid).child("twitter").child("tweets").set(returnedData[0])
		session['userTwitterData'] = returnedData
		return redirect(url_for('dashboard.home'))
	except Exception as e:
		print(e)
		username = request.get_json()['username']
		returnedData = connectTwitter(username)
		database.child("users").child(uid).child("twitter").update(returnedData[1])
		database.child("users").child(uid).child("twitter").child("tweets").update(returnedData[0])
		return returnedData

# Connect twitter function
def connectTwitter(username):
	try:
		print('connecting twitter')
		results = getTwitterData(username)
		return results
	except Exception as e:
		print(e)
		return 'failed'

## GETTING DATA ##

# Twitter
def requestTwitter(uid):
	# Trying to run webscrapping function
	try:
		username = database.child("users").child(uid).child("twitter").child("username").get().val()
		print("Request Twitter\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
		twitterScrapped = getTwitterData(username)
		tweets = twitterScrapped[0]
		twitterStats = twitterScrapped[1]
		print(tweets)
		database.child("users").child(uid).child("twitter").update(twitterStats)
		database.child("users").child(uid).child("twitter").child("tweets").set(tweets)

		# Getting current time 
		now = datetime.now()
		date_time = now.strftime("%m-%d-%Y")
		date_time_api = now.strftime("%m_%d_%Y")


		try:
			print('asdcdoppp')
			# Getting follower history
			historyData = dict(database.child("users").child(uid).child("twitter").child("history").get().val())

			# Counter variable
			print('aaakdmofbwfkgbnwrthirgnbiwsga\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

			counterFollowers = 0
			todayAlreadyIn = False
			followersDateList = []
			followersCountList = []
			print(historyData)
			print('aasnnnnfnfn')

			# Checking if user is new if so updating data
			try:
				print('aasnnnnfnfn')

				if historyData['followers'][0] == 'null':
					database.child("users").child(uid).child("twitter").child("history").child("followers").child(0).set({'followers_count': twitterStats['followers'], 'date': date_time_api })
				if historyData['following'][0] == 'null':
					database.child("users").child(uid).child("twitter").child("history").child("following").child(0).set({'following_count': twitterStats['following'], 'date': date_time_api })
			except Exception as e:
				print('not a new account')
			print('aasnnnnfnfn')
			todayAlreadyIn = False
			for followerItem in historyData['followers']:
				if str(date_time_api) == followerItem['date']:
					todayAlreadyIn = True
					break
				else:
					counterFollowers += 1
			if todayAlreadyIn == False:
				database.child("users").child(uid).child("twitter").child("history").child("followers").child(counterFollowers).set({'followers_count': twitterStats['followers'], 'date': date_time_api })
			print('aasnnnnfnfn')

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

				print(counterFollowing)
				print(date)
				print(followingCount)

				# Appending to list
				followingDateList.append(date)
				followingCountList.append(followingCount)
				counterFollowing += 1
				if date_time_api != followingDateList[-1]:
					database.child("users").child(uid).child("twitter").child("history").child("following").child(counterFollowing).update({'following_count': twitterStats['following'], 'date': date_time_api })
					break
				else:
					continue
		except Exception as e:
			print('Exception for loop')
			print(e)
		print(twitterScrapped)
		return twitterScrapped
	except Exception as e:
		print(e)
		print('twitter login failed')
		return redirect(url_for('dashboard.home'))

# Instagram 
def requestInstagram(uid):
	
	try:
		print("Request Instagram\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

		# Getting user from session
		# user = session['user']
		# print(user)
		
		# # Assigning uid as a variable which will be used to go through branched in for loop
		# uid = user['localId']
		# print('aaa')

		# Getting Data
		try:
			print('aaa')

			# Getting username to create url for instagram
			username = database.child("users").child(uid).child("instagram").child("username").get().val()
			url = 'https://www.instagram.com/' + username + '/'
			instagramConnection = InstagramScraper()
			instagramPosts = instagramConnection.profile_page_recent_posts(url)
			results = instagramConnection.profile_page_metrics(url)

			# Defining variables equal to followers
			numberOfFollowers = results['edge_followed_by']
			numberOfFollowing = results['edge_follow']
			database.child("users").child(uid).child("instagram").update(results)

			databaseData = dict(database.child("users").child(uid).get().val())

			instagramDataFomated = instagramPostsFormat(instagramPosts)
			database.child("users").child(uid).child("instagram").child("instagramPosts").set(instagramDataFomated)
			print("instagramDataFomated\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
			print(instagramDataFomated)
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

		# Checking if instagram is connected
		try:
			instagramData = dict(database.child("users").child(uid).child("instagram").get().val())
		except Exception as e:
			print('instagram not connected')

		return instagramData
	except Exception as e:
		print(e)
		print('Instagram Get Data failed')
		return redirect(url_for('dashboard.home'))

# Getting data and creating sessions after social platform functions run
def dataUpdating(uid):
	databaseData = dict(database.child("users").child(uid).get().val())

	# Getting Tips
	returnedTips = tips(databaseData)
	session['tips'] = returnedTips
	print('aaaalllllaa')

	# Getting stats
	stats = statistics(databaseData, uid)

	try:
		print('gertgwrategqart\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		print(stats)
		instagramRecentAvgLikes = stats['instagramStats']['instagramRecentAvgLikes']
		instagramRecentAvgComments = stats['instagramStats']['instagramRecentAvgComments']
		instagramRecentAvgDescriptionLen = stats['instagramStats']['instagramRecentAvgDescriptionLen']

		averageAmountOfFollowers = stats['avgFollowers']
		minAmountOfFollowers = stats['minFollowers']
		maxAmountOfFollowers = stats['maxFollowers']
		print('asds')
		database.child("users").child(uid).child("statistics").child("averageAmountOfFollowers").set(averageAmountOfFollowers)
		database.child("users").child(uid).child("statistics").child("minAmountOfFollowers").set(minAmountOfFollowers)
		database.child("users").child(uid).child("statistics").child("averageAmountOfFollowers").set(maxAmountOfFollowers)

		database.child("users").child(uid).child("statistics").child("instagramRecentAvgComments").set(instagramRecentAvgComments)
		database.child("users").child(uid).child("statistics").child("instagramRecentAvgDescriptionLen").set(instagramRecentAvgDescriptionLen)
		database.child("users").child(uid).child("statistics").child("instagramRecentAvgDescriptionLen").set(instagramRecentAvgDescriptionLen)

	except Exception as e:
		print(e)
		print("instagram not connected")
	
	session['statistics'] = stats
	
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

	# Getting history
	historyData = history(databaseData)
	print('a')
	print(historyData)
	session['history'] = historyData
	print('aaaa')

	# Getting website data
	websiteData = dict(database.child("users").child(uid).child("website").get().val())
	session['websiteData'] = websiteData
	print(databaseData)
	print(session)
	
	session['statistics'] = stats
	session['followersData'] = followersData
	session['history'] = historyData
	session['websiteData'] = websiteData

