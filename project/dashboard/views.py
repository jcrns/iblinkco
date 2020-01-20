# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, Blueprint, request, jsonify, g, url_for, make_response

# Importing twitter api
from project.social_apis import twitterConnect, firebaseConnect, websiteScrapping, getTwitterData, InstagramScraper

# Importing Login Required
from project.decorators import login_required

# Importing formating function
from project.users.views import creationFormating

# Importing tips function
from project.api.views import tips, history, websites, statistics, instagramPostsFormat, requestTwitter, requestInstagram, stream, dataUpdating

# Importing counter tool
import itertools

# Importing time
import time

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
	# Getting user credentials
	user = session['user']
	uid = user['localId']
	print(uid)

	# Getting setup complete variable
	setup_complete = database.child("users").child(uid).child("account").child("setup_complete").get().val()

	# Checking if user email is confirmed
	try:
		verifiedCheck = database.child("verified-accounts").child(uid).get().val()
		print(verifiedCheck)
		if verifiedCheck == True:
			pass
		else:
			return redirect(url_for('users.verifyNow'))
	except Exception as e:
		print(e)
		return redirect(url_for('users.verifyNow'))

	if setup_complete == True:
		try:
			twitterRequest = requestTwitter(uid)
			# Decoding data in function
			userTwitterData = "userTwitterData"
			twitterFormatted = decodeJsonData(twitterRequest, userTwitterData)
		except Exception as e:
			print(e)

		try:
			instagramRequest = requestInstagram(uid)
			userInstagramData = "userInstagramData"
			instagramFormatted = decodeJsonData(instagramRequest, userInstagramData)
		except Exception as e:
			print(e)

		# Getting all data
		databaseData = dict(database.child("users").child(uid).get().val())

		# Updating sessions and starts with this func
		sessionRequest = dataUpdating(uid, databaseData)
		formatData = creationFormating(databaseData)


		# Running function to get sorted data
		formattedInStream = stream(twitterFormatted, instagramFormatted)
		print(formattedInStream)

		# Putting sorted data in session
		session['stream'] = formattedInStream
		session['statistics'] = sessionRequest[0]
		session['history'] = sessionRequest[1]
		session['websiteData'] = sessionRequest[2]
		session['competition'] = sessionRequest[3]

		print("agwejgwrgbwretkgubwru")
		# t1 = time.time()
		# total = t1-t0
		# print(total)
	return render_template('dashboard/home.html')

# Function decodes returned json from API
def decodeJsonData(commonObj, sessionName):
	try:
		commonObj = commonObj.json
	except Exception as e:
		print(e)
		commonObj = commonObj
	# Checking if function fails
	if commonObj == 'failed':
		# Because function failed changing to 0 for stream function
		commonObj = 0
		if session.get(sessionName):
			session.pop(sessionName)
	else:
		# If function doesn't fail we put returned data in session
		session[sessionName] = commonObj

	return commonObj

# Setup and Website Update
@dashboard.route('/setup-update', methods=['GET', 'POST'])
def updateSetupAndWebsite():
	# Attemptingto sign in to backend
	user = session['user']


	# Assigning uid as a variable which will be used to go through branched in for loop
	uid = user['localId']
	setup_completed = { "setup_complete": True }
	# session['setup_complete'] = True

	# Adding Setup Complete to Database
	database.child("users").child(uid).child("account").update({ "setup_complete": True })

	# Checking is instagram and twiter is in session
	try:
		twitter_exist = session['userTwitterData']
		twitterConnected = True
	except Exception as e:
		print(e)
		print("twiiter not connected")
		twitterConnected = False

	try:
		instagram_exist = session['userInstagramData']
		instagramConnected = True
	except Exception as e:
		print(e)
		print("Instagram not connected")
		instagramConnected = False

	# Checking if instagram and twitter are connect else saying they are needed
	if instagramConnected == False and twitterConnected == False:
		flash('Twitter Or Instagram needed')
		return redirect(url_for('dashboard.home'))

	return redirect(url_for('dashboard.home'))


