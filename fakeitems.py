from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy_utils import database_exists, drop_database, create_database

from database_setup import Category, CategoryItem, User, Base

engine = create_engine('sqlite:///itemcatalog.db')

# Clear database
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
user1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(user1)
session.commit()

# Items for Strings
category1 = Category(name="strings", user_id=1)

session.add(category1)
session.commit()

item1 = CategoryItem(name="violin", user_id=1, category=category1)

session.add(item1)
session.commit()

item2 = CategoryItem(name="viola", user_id=1, category=category1)

session.add(item2)
session.commit()

item3 = CategoryItem(name="cello", user_id=1, category=category1)

session.add(item3)
session.commit()

# Items for Strings
category2 = Category(name="woodwinds", user_id=1)

session.add(category1)
session.commit()

item1 = CategoryItem(name="flute", user_id=1, category=category2)

session.add(item1)
session.commit()

item2 = CategoryItem(name="piccolo", user_id=1, category=category2)

session.add(item2)
session.commit()

item3 = CategoryItem(name="oboe", user_id=1, category=category2)

session.add(item3)
session.commit()

# Items for Strings
category3 = Category(name="percussion", user_id=1)

session.add(category1)
session.commit()

item1 = CategoryItem(name="marimba", user_id=1, category=category3)

session.add(item1)
session.commit()

item2 = CategoryItem(name="timpani", user_id=1, category=category3)

session.add(item2)
session.commit()

item3 = CategoryItem(name="xylophone", user_id=1, category=category3)

session.add(item3)
session.commit()

categories = session.query(Category).all()
for category in categories:
    print "Category: " + category.name