# Importing all needed Flask classes
from flask import Flask, session, redirect, Blueprint, request, jsonify, g, url_for, make_response, Response

# Firebase connection
from project.social_apis import firebaseConnect, websiteScrapping, googleSearch

# Tools for for loops
import itertools

# Importing random
import random

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
		# Twitter variables
		twitterDescription = userReturn['twitter']['userData']['description']
		twitterName = userReturn['twitter']['userData']['name']
		twitterLocation = userReturn['twitter']['userData']['location']
		twitterFollowing = userReturn['twitter']['userData']['friends_count']

		# Trying to get website variables
		try:
			websiteName = userReturn['website']['website_name']
			websiteUrl = userReturn['website']['website_url']
			websiteLinks = userReturn['website']['links']
			
		except Exception as e:
			print('Website tips not working/setup')
			print(e)

		twitterDescriptionLen = len(twitterDescription)

		twitterFollowers = history(userReturn)

		print('\n\n\n\n\n\n\n\n\n\n\n')
		print(twitterFollowers)
		twitterFollowerNumberList = twitterFollowers[1]
		print(twitterFollowerNumberList)

		# Finding out static trend with for loop
		twitterDaysStatic = 0
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
				twitterDaysStatic += 1
				print(twitterDaysStatic)
			else:
				break
		print('\n\n\n\n\n\n\n\n\n\n\n\n\ndaysStatic')
		print(twitterDaysStatic)

		# Trying to give other tips
		try:
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
			print('no unrequired tips')
			print(e)

		# Competition
		competition = userReturn['competition']

		if competition['title'][0] == 'null':
			competitionNoneTip = "Find your competition as soon as possible"
			tips.append(competitionNoneTip)


		# If conditions are true tips will be given to user
		
		# Programming tips
		if twitterDescriptionLen < 160:
			twitterDescriptionLenMessage = "Only " + str(twitterDescriptionLen) + "/180 of your characters have been used for your bio. Explain who you are!"
			tips.append(twitterDescriptionLenMessage)
		if "#" not in twitterDescription:
			twitterDescriptionNoHashtagsMessage = "No Hashtags Found. Try adding hashtags to your bio!"
			tips.append(twitterDescriptionNoHashtagsMessage)
		if twitterLocation == "":
			twitterLocationIsNoneMessage = "No location found! Add your location so people know where you are located"
			tips.append(twitterLocationIsNoneMessage)
		if twitterDaysStatic >= 3:
			twitterDaysStaticTip = "Followers on twitter haven't changed in the last " + str(twitterDaysStatic) + " days. Try posting more and engaging with people."
			tips.append(twitterDaysStaticTip)
		if twitterFollowing < 100:
			twitterFollowingTips = "You are only following " + str(twitterFollowing) + " people. Try following more people in your niche."
			tips.append(twitterFollowingTips)
		
		# Website Tip
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

# Get History
def history(userReturn):
	print('historyaaaa')
	try:
		print(userReturn['twitter']['history'])
		# print("userReturn['twitter']['history']")
		history = userReturn['twitter']['history']
		print('aaaa')
		history['followers']
		dateList = []
		followerList = []
		print('aggg')
		for followerItem in history['followers']:
			print(followerItem)
			date = followerItem['date']
			followersCount = followerItem['followers_count']

			# Appending to list
			dateList.append(date)
			followerList.append(followersCount)
		data = []
		data.append(dateList)
		data.append(followerList)
		return data
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

		# Creating branches
		database.child("users").child(uid).child("account").set(userAccount)
		database.child("users").child(uid).child("website").set(addWebsite)
		database.child("users").child(uid).child("user").set(user)
		database.child("users").child(uid).child("twitter").child("history").child("followers").set(['null'])
		database.child("users").child(uid).child("twitter").child("history").child("following").set(['null'])
		database.child("users").child(uid).child("twitter").child("followersFormated").set([ ['null'], ['null'] ])
		database.child("users").child(uid).child("competition").child("link").set(['null'])
		database.child("users").child(uid).child("competition").child("title").set(['null'])
		database.child("users").child(uid).child("tips").set(['null'])

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
		# Deleting dictionaries from data
		try:
			del signIn['twitter']['followers']
			del signIn['twitter']['userData']['contributors_enabled']
			del signIn['twitter']['userData']['created_at']
			del signIn['twitter']['userData']['default_profile']
			del signIn['twitter']['userData']['default_profile_image']
			del signIn['twitter']['userData']['follow_request_sent']
			del signIn['twitter']['userData']['geo_enabled']
			del signIn['twitter']['userData']['has_extended_profile']
			del signIn['twitter']['userData']['id']
			del signIn['twitter']['userData']['id_str']
			del signIn['twitter']['userData']['is_translation_enabled']
			del signIn['twitter']['userData']['is_translator']
			del signIn['twitter']['userData']['listed_count']
			del signIn['twitter']['userData']['needs_phone_verification']
			del signIn['twitter']['userData']['notifications']
			del signIn['twitter']['userData']['profile_background_color']
			del signIn['twitter']['userData']['profile_background_title']
			del signIn['twitter']['userData']['profile_image_url']
			del signIn['twitter']['userData']['profile_image_url_https']
			del signIn['twitter']['userData']['profile_link_color']
			del signIn['twitter']['userData']['profile_sidebar_border_color']
			del signIn['twitter']['userData']['profile_sidebar_fill_color']
			del signIn['twitter']['userData']['profile_text_color']
			del signIn['twitter']['userData']['profile_use_background_image']
			del signIn['twitter']['userData']['protected']
			del signIn['twitter']['userData']['suspended']
			del signIn['twitter']['userData']['translator_type']
		except Exception as e:
			print(e)
			print('Deleting followers failed')
		try:
			del signIn['user']
		except Exception as e:
			print(e)
			print('Deleting user failed')
		try:
			del signIn['twitter']['userData']['entities']
		except Exception as e:
			print(e)
			print('Deleting userdata entities failed')
		
		signIn['message'] = 'success'
		print(signIn)

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
		

		# Tips
		print("Tips\n\n\n\n\n\n\n\n\n")
		returnedTips = tips(userReturn)
		print(returnedTips)

		# History
		historyReturned = history(userReturn)

		try:
			# Getting followers data
			followersData = followerData(userReturn)
			userReturn['twitter']['followersFormated'] = followersData
		
		except Exception as e:
			print(e)

		# Getting website data
		websitesData = websites(userReturn)

		# Attempting to get competition results
		try:
			competition = dict(database.child("users").child(uid).child("competition").get().val())
		except Exception as e:
			competition = database.child("users").child(uid).child("competition").get().val()
			print('comp none')
			print(e)

	except Exception as e:
		print("Signin error below")
		print(e)
		userData['message'] = 'failed'
		return jsonify(userData)


	# Appending valid formated data to final dictionary
	userReturn['user'] = user
	userReturn['history'] = historyReturned
	userReturn['website'] = websitesData

	print('ppppppp\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
	# For loop to return iterating strings from firebase into list for other platforms
	print(followersData)
	for i in followersData:
		print(i)
	print(competition)
	for i in competition:
		print(i)

	print('pppp\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

	# userFinal.append(user)
	# userFinal.append(returnedTips)
	# userFinal.append(historyReturned)
	# userFinal.append(followersData)
	# userFinal.append(websitesData)
	# userFinal.append(competition)

	userReturn['tips'] = returnedTips
	userReturn['competition'] = competition

	# print(userReturn)
	print('aaalaaaalllalaa')
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
		print('aaaaaa')
		nichePost = request.form['niche_text']
		
		# Getting data from firebase
		user = session['user']
		uid = user['localId']

		location = database.child("users").child(uid).child("twitter").child("userData").child("location").get().val()
		
		# Getting competitiors on google
		searchResults = googleSearch(nichePost, location, 1)
		print(searchResults)
		compDict = {}
		compDict['link'] = searchResults[0]
		compDict['title'] = searchResults[1]

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
		compDict['link'] = searchResults[0]
		compDict['title'] = searchResults[1]
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

# GOOGLE SEARCH

# # Search Function
# @api.route("/search-form", methods=['GET', 'POST'])
# def searchForm():
# 	print('searching')

# 	search = request.form['search']
# 	connect = googleConnect(search)
# 	print(connect)

# 	return jsonify(connect)





