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
