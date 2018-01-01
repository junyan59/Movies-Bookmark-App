from flask import Flask, jsonify, render_template, redirect, url_for, request
from flask import flash, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import httplib2
import requests
import os
import random
import string

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']

# Connect to catalog database
# engine = create_engine('sqlite:///item_catalog.db')
engine = create_engine('postgresql://catalog:password@localhost/catalog')
Base.metadata.bind = engine

# Create session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Homepage - Show all movie categories


@app.route('/')
@app.route('/catalog')
def showCatalog():
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Item).order_by(asc(Item.name))
    return render_template('catalog.html', categories=categories, items=items)

# Show category Items


@app.route('/catalog/<int:category_id>')
@app.route('/catalog/<int:category_id>/items/')
def showCategory(category_id):
    categories = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(id=category_id).first()
    categoryName = category.name
    items = session.query(Item).filter_by(
        category_id=category_id).order_by(asc(Item.name))
    count = session.query(
        Item).filter_by(category_id=category_id).count()
    return render_template(
        'category.html', categories=categories, items=items,
        categoryName=categoryName, count=count)

# Show an specific movie item


@app.route('/catalog/<int:category_id>/items/<int:item_id>/')
def showItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    creator = getUserInfo(item.user_id)
    return render_template('item.html', item=item, creator=creator)

# Create a new movie item


@app.route('/catalog/create', methods=['GET', 'POST'])
@login_required
def addItem():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please add a movie name for the category.')
            return redirect(url_for('addItem'))
        if not request.form['description']:
            flash('Please add a description for the movie.')
            return redirect(url_for('addItem'))
        newItem = Item(name=request.form['name'], description=request.form[
            'description'], category_id=request.form['category'],
            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New Item %s Successfully Created' % newItem.name)
        return redirect(url_for('showCatalog'))
    else:
        categories = session.query(Category).order_by(asc(Category.name))
        return render_template('addItem.html', categories=categories)

# Edit a movie item


@app.route(
    '/catalog/<int:category_id>/items/<int:item_id>/edit',
    methods=['GET', 'POST'])
@login_required
def editItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    creator = getUserInfo(item.user_id)
    if creator.id != login_session['user_id']:
        return redirect(url_for('showCatalog'))
    categories = session.query(Category).order_by(asc(Category.name))
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['category']:
            item.category_id = request.form['category']
        if request.form['description']:
            item.description = request.form['description']
        session.add(item)
        session.commit()
        flash('Categroy Item %s Successfully Edited' % item.name)
        return redirect(url_for(
            'showItem', category_id=item.category_id, item_id=item.id))
    else:
        return render_template(
            'editItem.html', categories=categories, item=item)

# Delete a movie item


@app.route(
    '/catalog/<int:category_id>/items/<int:item_id>/delete',
    methods=['GET', 'POST'])
@login_required
def deleteItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    creator = getUserInfo(item.user_id)
    if creator.id != login_session['user_id']:
        return redirect(url_for('showCatalog'))
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showCategory', category_id=item.category_id))
    else:
        return render_template('deleteItem.html', item=item)


# Login - Create anti-forgery state token
@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/logout')
def logout():
    return "This will log you out and redirect you to the homepage."


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate anti-forgery state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
            "Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            "Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # See if user exists
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h2>Log In Successfully, '
    output += login_session['username']
    output += '!</h2>'

    return output


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    # Validate anti-forgery state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Gets access token
    access_token = request.data
    print "access token received %s " % access_token

    # Gets info from fb clients secrets
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_secret']

    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.11/me"

    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.11/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.11/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # See if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h2>Log In Successfully, '
    output += login_session['username']
    output += '!</h2>'
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    return "This will log you out. (Facebook)"


@app.route('/catalog/JSON')
def catalogJSON():
    return "This will show the list of categories in JSON format."


@app.route('/catalog/<int:category_id>/items/JSON')
def categoryJSON(category_id):
    return "This will show the list of items of a category in JSON format."


@app.route('/catalog/<int:category_id>/items/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    return "This will show a single item of a category in JSON format."

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='localhost', port=8000)
