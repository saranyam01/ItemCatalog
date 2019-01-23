from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from sqlalchemy.sql.functions import func

# New imports for login step
from flask import session as login_session
import random
import string

# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///itemcatlogwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
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
        response = make_response(json.dumps("Token's user ID doesn't \
            match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already \
            connected.'), 200)
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

    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src = "'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


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


# DISCONNECT - Revoke a current user's token and reset their login_session
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
        response = make_response(json.dumps('Failed to revoke token \
            for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Displays all Categories in JSON format
@app.route('/catalog/JSON')
def dispCategoryJSON():
    categories = session.query(Category).all()
    return jsonify(category=[i.serialize for i in categories])


# Displays a Category and items for selected category in JSON format
@app.route('/catalog/<int:category_id>/JSON')
def dispCategoryItemsJSON1(category_id):
    category = session.query(Category).filter(Category.id == category_id).one()
    category_items = session.query(Item).filter(Item.cat_id ==
                                                category_id).all()
    return jsonify(category=[category.serialize],
                   items=([k.serialize for k in category_items]))


# Displays all items in JSON format
@app.route('/items/JSON')
def dispCategoryJSON1():
    items = session.query(Item).all()
    return jsonify(Items=[i.serialize for i in items])


# Displays all Categories and Latest add items
@app.route('/')
@app.route('/catalog')
def dispCategory():
    categories = session.query(Category).all()
    items = session.query(Item, Category).filter(
        Item.cat_id == Category.id).add_columns(
        Item.title, Category.name).order_by(Item.id.desc()).limit(9).all()
    if 'username' not in login_session:
        return render_template('publiccatalog.html',
                               categories=categories,
                               items=items)
    else:
        return render_template('catalog.html',
                               categories=categories,
                               items=items)


# Displays all Categories and items for selected category
@app.route('/catalog/<int:category_id>/items')
def dispCategoryItems(category_id):
    categories = session.query(Category).all()
    categoryn = session.query(Item, Category).filter(
        Item.cat_id == Category.id, Item.cat_id == category_id).add_columns(
        func.count(Item.id).label('ccount'), Category.name.label('cname'),
        Category.id.label('cid')).group_by(Item.cat_id).one()
    items = session.query(Item, Category).filter(
        Item.cat_id == Category.id, Item.cat_id == category_id).add_columns(
        Item.title, Category.name).order_by(Item.id.desc()).limit(9).all()
    return render_template('items.html',
                           categories=categories,
                           items=items,
                           categoryn=categoryn)


# Create a new item
@app.route('/catalog/new', methods=['GET', 'POST'])
def newItem():
    catall = session.query(Category).all()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if not request.form['title'] or not request.form['description']:
            flash('Enter title and description details')
            return redirect(url_for('newItem'))
        itemToAdd = Item(title=request.form['title'],
                         description=request.form['description'],
                         cat_id=request.form['category_id'],
                         user_id=login_session['user_id'])
        session.add(itemToAdd)
        flash('New Item %s Successfully Created' % itemToAdd.title)
        session.commit()
        return redirect(url_for('dispCategory'))
    else:
        return render_template('newitem.html', catall=catall)


# Display the description of a item
@app.route('/catalog/<int:category_id>/<string:titleinp>')
def dispCategoryItemdesc(category_id, titleinp):
    itemd = session.query(Item).filter(
        Item.cat_id == category_id, Item.title == titleinp).add_columns(
        Item.title, Item.description, Item.user_id).one()
    if 'username' not in login_session or \
            itemd.user_id != login_session['user_id']:
        return render_template('publicdesc.html', itemd=itemd)
    else:
        return render_template('desc.html', itemd=itemd)


# Edit a item
@app.route('/catalog/<string:titleinp>/edit', methods=['GET', 'POST'])
def editItem(titleinp):
    if 'username' not in login_session:
        return redirect('/login')
    itemToEdit = session.query(Item).filter(Item.title == titleinp).one()
    itemd = session.query(Item).filter(Item.title == titleinp).add_columns(
        Item.cat_id, Item.title, Item.description).one()
    if request.method == 'POST':
        if request.form['title']:
            itemToEdit.title = request.form['title']
        if request.form['description']:
            itemToEdit.description = request.form['description']
        if request.form['category_id']:
            itemToEdit.cat_id = request.form.get('category_id')
        itemToEdit.id = itemToEdit.id
        itemToEdit.user_id = login_session['user_id']
        session.add(itemToEdit)
        flash('Item %s Successfully Edited' % itemToEdit.title)
        session.commit()
        return redirect(url_for('dispCategory'))
    else:
        return render_template('edititem.html',
                               itemToEdit=itemToEdit,
                               itemd=itemd)
# return 'This page is for editing item %s' % cat_id


# Delete a item
@app.route('/catalog/<string:titleinp>/delete', methods=['GET', 'POST'])
def deleteItem(titleinp):
    itemToDelete = session.query(Item).filter(Item.title == titleinp).one()
    itemd = session.query(Item).filter(Item.title == titleinp).add_columns(
        Item.cat_id, Item.title, Item.description).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(itemToDelete)
        flash('Item %s Successfully Deleted' % itemToDelete.title)
        session.commit()
        return redirect(url_for('dispCategory'))
    else:
        return render_template('deleteitem.html',
                               itemToDelete=itemToDelete,
                               itemd=itemd)
# return "This page is for deleting item %s"%titleinp


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'username' in login_session:
        gdisconnect()
        del login_session['gplus_id']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        return redirect(url_for('dispCategory'))
    else:
        flash("You were not logged in")
        return redirect(url_for('dispCategory'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=False)
