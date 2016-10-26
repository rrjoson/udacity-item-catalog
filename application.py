from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User

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
	return "This will show the list of categories."

@app.route('/catalog/<int:catalog_id>')
@app.route('/catalog/<int:catalog_id>/items')
def showCategory(catalog_id):
	return "This will show the list of items of a category."

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>')
def showCategoryItem(catalog_id, item_id):
	return "This will show a single item of a category."

@app.route('/catalog/add')
def addCategory():
	return "This will let you add a category."

@app.route('/catalog/<int:catalog_id>/edit')
def editCategory(catalog_id):
	return "This will let you edit a category."

@app.route('/catalog/<int:catalog_id>/delete')
def deleteCategory(catalog_id):
	return "This will let you delete a category."

@app.route('/catalog/<int:catalog_id>/items/add')
def addCategoryItem(catalog_id):
	return "This will let you add a category item."

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/edit')
def editCategoryItem(catalog_id, item_id):
	return "This will let you edit a category item."

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/delete')
def deleteCategoryItem(catalog_id, item_id):
	return "This will let you delete a category item."

@app.route('/login')
def login():
	return "This will show links to fb and google login."

@app.route('/logout')
def logout():
	return "This will log you out and redirect you to the catalog page."

@app.route('/fbconnect')
def fbconnect():
	return "This will log you in. (Facebook)"

@app.route('/fbdisconnect')
def fbdisconnect():
	return "This will log you out. (Facebook)"

@app.route('/gconnect')
def gconnect():
	return "This will log you in. (Google)"

@app.route('/gdicconnect')
def gdisconnect():
	return "This will log you out. (Google)"

@app.route('/catalog/JSON')
def showCategoriesJSON():
	return "This will show the list of categories in JSON format."

@app.route('/catalog/<int:catalog_id>/JSON')
@app.route('/catalog/<int:catalog_id>/items/JSON')
def showCategoryJSON(catalog_id):
	return "This will show the list of items of a category in JSON format."

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/JSON')
def showCategoryItemJSON(catalog_id, item_id):
	return "This will show a single item of a category in JSON format."

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)