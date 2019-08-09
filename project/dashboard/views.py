# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, Blueprint, request, jsonify, g, url_for, make_response

# Importing twitter api
from project.social_apis import twitterConnect, firebaseConnect, websiteScrapping, getTwitterData, InstagramScraper

# Importing Login Required
from project.decorators import login_required

# Importing formating function
from project.users.views import creationFormating

# Importing tips function
from project.api.views import tips, history, websites, statistics, instagramPostsFormat, requestTwitter, requestInstagram, dataUpdating

# Importing counter tool
import itertools

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
	# if session.get('twitter_oauth') is not None:
	# 	# Running twitter request function if session exist
	# Getting data
	user = session['user']
	uid = user['localId']
	databaseData = dict(database.child("users").child(uid).get().val())
	setup_complete = databaseData['account']['setup_complete']

	userVerified = False

	if setup_complete == True:
		try:
			twitterRequest = requestTwitter(uid)
			try:
				twitterFormatted = twitterRequest.json
			except Exception as e:
				print(e)
				twitterFormatted = twitterRequest
			if twitterFormatted == 'failed':
				if session.get('userTwitterData'):
					session.pop('userTwitterData')
			else:
				session['userTwitterData'] = twitterFormatted
		except Exception as e:
			print(e)
			# if session.get('userTwitterData'):
			# 	session.pop('userTwitterData')
		try:
			instagramRequest = requestInstagram(uid)
			try:
				instagramFormatted = instagramRequest.json
			except Exception as e:
				print(e)
				instagramFormatted = instagramRequest
			

			if instagramFormatted == 'failed':
				if session.get('userInstagramData'):
					session.pop('userInstagramData')
			else:
				session['userInstagramData'] = instagramFormatted

		except Exception as e:
			print(e)
			print("aergergqergqrthetyjtyrgkwr thwkrth wtyhk ety etjyektyjytjetyj\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

		sessionRequest = dataUpdating(uid)
		formatData = creationFormating(databaseData)
		print(twitterFormatted)
		try:
			verifiedUsers = database.child("verified-accounts").get().val()
			print(verifiedUsers)

			for user in verifiedUsers:
				if user['email'] == session['email']:
					userVerified = True
					break
			if userVerified == False:
				return redirect(url_for('users.verifyNow'))
		except Exception as e:
			print(e)
			return redirect(url_for('users.verifyNow'))

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
		twitterConnected = True
	except Exception as e:
		print(e)
		print("twiiter not connected")
		twitterConnected = False

	try:
		print('aaff\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		# Getting session data
		instagram_exist = session['userInstagramData']
		
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
		instagramConnected = True
	except Exception as e:
		print(e)
		print("Instagram not connected")
		instagramConnected = False

	if instagramConnected == False and twitterConnected == False:
		flash('Twitter Or Instagram needed')
		return redirect(url_for('dashboard.home'))
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


