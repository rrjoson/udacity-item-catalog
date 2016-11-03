from flask import Flask, render_template, url_for, request, redirect, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from flask import session as login_session
import random, string

app = Flask(__name__)

# Connect to Database
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/catalog')
def showCategories():
	# Get all categories
	categories = session.query(Category).all()

	# Get lastest 5 category items added
	categoryItems = session.query(CategoryItem).all()

	return render_template('categories.html', categories = categories, categoryItems = categoryItems)

@app.route('/catalog/<int:catalog_id>')
@app.route('/catalog/<int:catalog_id>/items')
def showCategory(catalog_id):
	# Get all categories
	categories = session.query(Category).all()

	# Get category
	category = session.query(Category).filter_by(id = catalog_id).first()

	# Get name of category
	categoryName = category.name

	# Get all items of a specific category
	categoryItems = session.query(CategoryItem).filter_by(category_id = catalog_id).all()

	# Get count of category items
	categoryItemsCount = session.query(CategoryItem).filter_by(category_id = catalog_id).count()

	return render_template('category.html', categories = categories, categoryItems = categoryItems, categoryName = categoryName, categoryItemsCount = categoryItemsCount)

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>')
def showCategoryItem(catalog_id, item_id):
	# Get category item
	categoryItem = session.query(CategoryItem).filter_by(id = item_id).first()

	return render_template('categoryItem.html', categoryItem = categoryItem)

@app.route('/catalog/add', methods=['GET', 'POST'])
def addCategoryItem():
	# Check if user is logged in

	if request.method == 'POST':
		# Add category item
		newCategoryItem = CategoryItem(name = request.form['name'], description = request.form['description'], category_id = request.form['category'], user_id = 1)
		session.add(newCategoryItem)
		session.commit()

		return redirect(url_for('showCategories'))
	else:
		# Get all categories
		categories = session.query(Category).all()

		return render_template('addCategoryItem.html', categories = categories)

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/edit', methods=['GET', 'POST'])
def editCategoryItem(catalog_id, item_id):
	# Check if user is logged in

	# Check if logged in user is creator of category item

	# Get category item
	categoryItem = session.query(CategoryItem).filter_by(id = item_id).first()

	# Get all categories
	categories = session.query(Category).all()

	if request.method == 'POST':
		if request.form['name']:
			categoryItem.name = request.form['name']
		if request.form['description']:
			categoryItem.description = request.form['description']
		if request.form['category']:
			categoryItem.category_id = request.form['category']
		return redirect(url_for('showCategoryItem', catalog_id = categoryItem.category_id ,item_id = categoryItem.id))
	else:
		return render_template('editCategoryItem.html', categories = categories, categoryItem = categoryItem)

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteCategoryItem(catalog_id, item_id):
	# Check if user is logged in

	# Check if logged in user is creator of category item

	# Get category item
	categoryItem = session.query(CategoryItem).filter_by(id = item_id).first()

	if request.method == 'POST':
		session.delete(categoryItem)
		session.commit()
		return redirect(url_for('showCategory', catalog_id = categoryItem.category_id))
	else:
		return render_template('deleteCategoryItem.html', categoryItem = categoryItem)

@app.route('/login')
def login():
	# Create anti-forgery state token
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state

	return render_template('login.html', STATE=state)

@app.route('/logout')
def logout():
	return "This will log you out and redirect you to the catalog page."

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
	# Validate anti-forgery state token
	if request.args.get('state') != login_session['state']:
	    response = make_response(json.dumps('Invalid state parameter.'), 401)
	    response.headers['Content-Type'] = 'application/json'
	    return response

	return "This will log you in. (Facebook)"

@app.route('/fbdisconnect')
def fbdisconnect():
	return "This will log you out. (Facebook)"

@app.route('/gconnect', methods=['POST'])
def gconnect():
	# Validate anti-forgery state token
	if request.args.get('state') != login_session['state']:
	    response = make_response(json.dumps('Invalid state parameter.'), 401)
	    response.headers['Content-Type'] = 'application/json'
	    return response

	return "This will log you in. (Google)"

@app.route('/gdicconnect')
def gdisconnect():
	return "This will log you out. (Google)"

@app.route('/catalog/JSON')
def showCategoriesJSON():
	categories = session.query(Category).all()
	return jsonify(categories = [category.serialize for category in categories])

@app.route('/catalog/<int:catalog_id>/JSON')
@app.route('/catalog/<int:catalog_id>/items/JSON')
def showCategoryJSON(catalog_id):
	categoryItems = session.query(CategoryItem).filter_by(category_id = catalog_id).all()
	return jsonify(categoryItems = [categoryItem.serialize for categoryItem in categoryItems])

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/JSON')
def showCategoryItemJSON(catalog_id, item_id):
	categoryItem = session.query(CategoryItem).filter_by(id = item_id).first()
	return jsonify(categoryItem = [categoryItem.serialize])

if __name__ == '__main__':
	app.debug = True
	app.secret_key = 'super_secret_key'
	app.run(host = '0.0.0.0', port = 5000)