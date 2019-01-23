from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///itemcatlogwithusers.db')
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
User1 = User(name="saranya murugesan", email="mailsarancse@gmail.com",
             picture='https://lh3.googleusercontent.com/-hQYpYmjljq4/A\
             AAAAAAAAAI/AAAAAAAAAFI/-MJrcm_DPyY/photo.jpg')
session.add(User1)
session.commit()

# Category Soccer
category1 = Category(user_id=1, name="Soccer")

session.add(category1)
session.commit()


# Category Basketball
category2 = Category(user_id=1, name="Basketball")

session.add(category2)
session.commit()


# Category Baseball
category3 = Category(user_id=1, name="Baseball")

session.add(category3)
session.commit()


# Category Frisbee
category4 = Category(user_id=1, name="Frisbee")

session.add(category4)
session.commit()


# Category Snowboarding
category5 = Category(user_id=1, name="Snowboarding")

session.add(category5)
session.commit()


# Category Rockclimbing
category6 = Category(user_id=1, name="Rockclimbing")

session.add(category6)
session.commit()


# Category Foosball
category7 = Category(user_id=1, name="Foosball")

session.add(category7)
session.commit()


# Category Skating
category8 = Category(user_id=1, name="Skating")

session.add(category8)
session.commit()


# Category Hockey
category9 = Category(user_id=1, name="Hockey")

session.add(category9)
session.commit()


# Items for Soccer
Item1 = Item(user_id=1, title="Soccer cleats",
             description="The shoes", category=category1)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, title="Jersey", description="The shirt",
             category=category1)

session.add(Item2)
session.commit()


# Items for Baseball
Item3 = Item(user_id=1, title="Bat", description="The bat", category=category3)

session.add(Item3)
session.commit()


# Items for Snowboarding
Item4 = Item(user_id=1, title="Snowboard", description="Best for any terrain \
             and conditions. All-mountain snowboards perform anywhere on a \
             mountain-- groomed runs, backcountry, evenpark and pipe. They \
             may be directional (meaning downhill only) or twin-tip (for \
             riding switch, meaning either direction).Most boarders ride \
             all-mountain boards. Because of their versatility, all-mountain\
             boards are good for beginners who are still learning what terrain\
             they like. ", category=category5)

session.add(Item4)
session.commit()


# Items for Soccer
Item5 = Item(user_id=1, title="Shinguards", description="Shinguards",
             category=category1)

session.add(Item5)
session.commit()


# Items for Soccer
Item6 = Item(user_id=1, title="Two Shinguards", description="Two Shinguards",
             category=category1)

session.add(Item6)
session.commit()


# Items for Frisbee
Item7 = Item(user_id=1, title="Frisbee", description="Frisbee",
             category=category4)

session.add(Item7)
session.commit()


# Items for Snowboarding
Item8 = Item(user_id=1, title="Goggles", description="Goggles",
             category=category5)

session.add(Item8)
session.commit()


# Items for Hockey
Item9 = Item(user_id=1, title="Stick", description="Hockey stick",
             category=category9)

session.add(Item9)
session.commit()


print "added category and items!"
