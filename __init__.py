from flask import Flask, render_template
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item

app = Flask(__name__)

# Connect to catalog database
# engine = create_engine('sqlite:///item_catalog.db')
engine = create_engine('postgresql://catalog:password@localhost/catalog')
Base.metadata.bind = engine

# Create session
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog')
def showCatalog():
    return render_template('catalog.html')


@app.route('/catalog/<int:category_id>')
@app.route('/catalog/<int:category_id>/items/')
def showCategory(category_id):
    return render_template('category.html')


@app.route('/catalog/<int:category_id>/items/<int:item_id>/')
def showItem(category_id, item_id):
    return render_template('item.html')


@app.route('/catalog/create', methods=['GET', 'POST'])
@login_required
def addItem():
    return render_template('addItem.html')


@app.route(
    '/catalog/<int:category_id>/items/<int:item_id>/edit',
    methods=['GET', 'POST'])
@login_required
def editItem(category_id, item_id):
    return render_template('editItem.html')


@app.route(
    '/catalog/<int:category_id>/items/<int:item_id>/delete',
    methods=['GET', 'POST'])
@login_required
def deleteItem(category_id, item_id):
    return render_template('deleteItem.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/logout')
def logout():
    return "This will log you out and redirect you to the homepage."


@app.route('/gconnect', methods=['POST'])
def gconnect():
    return "This will log you in. (Google)"


@app.route('/gdisconnect')
def gdisconnect():
    return "This will log you out. (Google)"


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    return "This will log you in. (Facebook)"


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
