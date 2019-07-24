# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, Blueprint, jsonify

# Importing conf email
from flask_mail import Mail, Message

# Importing forms
from project.users.forms import RegistrationForm, LoginForm, ContactUs

# Importing login_required function
from project.decorators import login_required

# Importing the request library for API
import requests

# Importing auth functions
from project.api.views import createUserFunc, signInFunc

# Defining Blueprint var
users = Blueprint('users', __name__, template_folder='templates', static_folder='static')

def creationFormating(returnedData):
    print("Beggining Format")
    # Defining User Varibles
    email = returnedData['account']['email']
    firstname = returnedData['account']['firstname']
    lastname = returnedData['account']['lastname']
    try:
        websiteName = returnedData['website']['website_name']
        session['website_name'] = websiteName

        websiteUrl = returnedData['website']['website_url']
        session['website_url'] = websiteUrl
    except Exception as e:
        print(e)
        print('website not connected')

    # Storing returned data
    session['name'] = str(firstname) + " " + str(lastname)
    session['email'] = email


    # Attempting to format unrequired data
    try:
        setup_complete = returnedData['account']['setup_complete']
        session['setup_complete'] = setup_complete
        niche = returnedData['account']['niche']
        session['niche'] = niche

    except Exception as e:
        print("Setup incomplete\n\n\n\n\n")
        print(e)

    # Checking for twitter
    try:
        requestedTwitterUserData = ['description', 'friends_count', 'followers_count', 'location', 'name', 'screen_name']
        returnedTwitterUserData = dict()

        # Defining variables equal to json data
        twitterData = returnedData['twitter']

        for i in requestedTwitterUserData:
            userItem = returnedData['twitter']['userData'][i]
            returnedTwitterUserData[i] = userItem
            print(userItem)
        returnedTwitterUserData['tweets'] = returnedData['twitter']['tweets']
        session['userTwitterData'] = returnedTwitterUserData
        # session['twitter'] = twitterData
    except Exception as e:
        print('Twitter not connected')
        print(e)

# Register page url and function
@users.route("/register", methods=['GET', 'POST'])
def register():
    
    # Defining a variable equal to a form
    form = RegistrationForm()

    # Checking if form is valid
    if form.validate_on_submit():

        try:
            # Running auth function
            createUser = createUserFunc(form.email.data, form.password.data, form.firstname.data, form.lastname.data, 'web')

            # Getting returned data
            returnedData = createUser
            print('aaaa')
            email = returnedData[0]['email']
            firstname = returnedData[0]['firstname']
            lastname = returnedData[0]['lastname']

            # Storing returned data
            session['user'] = returnedData[1]
            session['name'] = str(firstname) + " " + str(lastname)
            session['email'] = email

            # Alerting user account was created
            flash(f'Account Created for {form.email.data} !', 'success')
            return redirect(url_for('dashboard.home'))
        except Exception as e:
            print(e)
            flash(f'Failed to Create Account')

    return render_template('users/register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():

    # Defining a variable equal to a form
    form = LoginForm()

    # Checking if form is valid
    if form.validate_on_submit():

        # Running auth function
        finalizedData = signInFunc(form.email.data, form.password.data)
        print("finalizedData\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(finalizedData)
        print("finalizedData\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        try:
            print('aaaaaa')
            print(finalizedData)
            session['user'] = finalizedData['user']
            session['tips'] = finalizedData['tips']
            returnedData = finalizedData['user']

            # print(finalizedData[1])
            # print(returnedData)

            # Getting history

            # # Getting followers' data
            # session['followersData'] = finalizedData['twitter']['followersFormated']

            # Stream
            print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

            print(finalizedData['website'])

            print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
            
            # Getting website data
            session['websiteData'] = finalizedData['website']
            # print(finalizedData[5])

            # print(finalizedData[2]) 
        except Exception as e:
            print(e)
            return redirect(url_for('users.login'))
            flash(f'signin failed')

        try:
            print('sssssss\n\n\n\n\n\n\n\n\n')
            session['competition'] = finalizedData['competition']  
            print(session['competition'])
        except Exception as e:
            print(e)
            print('sssssss\n\n\n\n\n\n\n\n\n')

            print('no competition')
        try:

            createFormat = creationFormating(finalizedData)
            session.permanent = True
            print(finalizedData['tips'])
            print('aaaa')

            return redirect(url_for('dashboard.home'))

        except Exception as e:
            print("e")
            print(e)
            flash(f'signin failed')
        print("aaaaaa")
    return render_template('users/login.html', title="Login", form=form)

@users.route("/logout")
@login_required 
def logout():
    session.clear()
    flash("You have been logged out")
    return redirect(url_for('homepage.home'))