# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, Blueprint, jsonify, request

# Importing forms
from project.users.forms import RegistrationForm, LoginForm, ContactUs

# Importing login_required function
from project.decorators import login_required

# Importing the request library for API
import requests

# Importing auth functions
from project.api.views import createUserFunc, signInFunc, userVerified

# Adding flask mail for email verification and password reset
from flask_mail import Mail, Message

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


from project.__init__ import mail, safeTimedUrlSerializer
from itsdangerous import SignatureExpired

# Register page url and function
@users.route("/register", methods=['GET', 'POST'])
def register():
    
    # Defining a variable equal to a form
    form = RegistrationForm()

    # Checking if form is valid
    if form.validate_on_submit():

        try:
            print('user')

            # Running auth function
            createUser = createUserFunc(form.email.data, form.password.data, form.firstname.data, form.lastname.data)
            print(createUser)
            print('aaaa')
            user = createUser[1]
            uid = user['localId']
            emailDict = { "email" : form.email.data, "uid" : uid }
            token = safeTimedUrlSerializer.dumps(emailDict, salt='email-confirm')

            # Sending email
            link = url_for('users.confirmEmail', token=token, _external=True)
            send = sendEmailVerified(form.email.data, link)

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
            flash(f'Email Confirmation Sent to {form.email.data} ! If not seen in your inbox check junk mail.', 'success')
            return redirect(url_for('users.login'))
        except Exception as e:
            print(e)
            flash(f'Failed to Create Account')

    return render_template('users/register.html', title='Register', form=form)


# Function sending email to new users
def sendEmailVerified(email, link):

    # Creating msg
    msg = Message('Confirm Email', sender='iblinkcompany@gmail.com', recipients=[email] )

    # Creating body email
    msg.body = 'Confirm your email now! {}'.format(link)

    try:
        # Sending email
        mail.send(msg)
        return 'success'
    except Exception as e:
        print(e)
        return 'failed'

# Creating url for email 
@users.route("/confirm_email/<token>", methods=['GET', 'POST'])
def confirmEmail(token):
    try:
        emailDict = safeTimedUrlSerializer.loads(token, salt='email-confirm', max_age=6000)
        email = emailDict['email']
        uid = emailDict['uid']
        # Running function for
        verified = userVerified(uid)
        return render_template('users/confirm_email.html', title='Email Confirmed', email=email)
    except SignatureExpired:
        return '<h1>Url Expired</h1>'

# Creating verify now page
@users.route("/verify-now", methods=['GET', 'POST'])
def verifyNow():
    email = session['email']
    user = session['user']
    uid = user['localId']
    emailDict = { "email" : email, "uid" : uid }

    if request.method == 'POST':
        token = safeTimedUrlSerializer.dumps(emailDict, salt='email-confirm')

        # Sending email
        link = url_for('users.confirmEmail', token=token, _external=True)
        send = sendEmailVerified(email, link)

        flash(f'Confirmation Email Sent')
    return render_template('users/verify_now.html', title='Confirm Email')


# Login page
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

            # Putting data in recieved data in sessions
            session['user'] = finalizedData['user']
            session['tips'] = finalizedData['tips']
            session['websiteData'] = finalizedData['website']
            session['competition'] = finalizedData['competition']  

        except Exception as e:
            print(e)
            return redirect(url_for('users.login'))
            flash(f'signin failed')

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