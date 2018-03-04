from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User, Base, Category, Item

engine = create_engine('sqlite:///item_catalog.db')
# engine = create_engine('postgresql://catalog:password@localhost/catalog')
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
user1 = User(name="Stephanie", email="stephanieyan59@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(user1)
session.commit()

# Items for Comedy
category1 = Category(name="Comedy", user_id=1)

session.add(category1)
session.commit()

item1 = Item(name="Step Brothers", user_id=1,
             description="Two aimless middle-aged losers still living at home are forced against their will to become roommates when their parents marry.", category=category1)

session.add(item1)
session.commit()

item2 = Item(name="White Chicks", user_id=1,
             description="Two disgraced FBI agents go way undercover in an effort to protect hotel heiresses the Wilson Sisters from a kidnapping plot.", category=category1)

session.add(item2)
session.commit()

item3 = Item(name="The Hangover", user_id=1, description="Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing. They make their way around the city in order to find their friend before his wedding.", category=category1)

session.add(item3)
session.commit()

# Items for Superhero
category2 = Category(name="Superhero", user_id=1)

session.add(category2)
session.commit()

item1 = Item(name="The Dark Knight", user_id=1, description="When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham, the Dark Knight must accept one of the greatest psychological and physical tests of his ability to fight injustice.", category=category2)

session.add(item1)
session.commit()

item2 = Item(name="Iron Man", user_id=1,
             description="After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil.", category=category2)

session.add(item2)
session.commit()

item3 = Item(name="Wonder Woman", user_id=1,
             description="When a pilot crashes and tells of conflict in the outside world, Diana, an Amazonian warrior in training, leaves home to fight a war, discovering her full powers and true destiny.", category=category2)

session.add(item3)
session.commit()

# Items for Fantasy
category3 = Category(name="Fantasy", user_id=1)

session.add(category3)
session.commit()

item1 = Item(name="The Lord of the Rings", user_id=1,
             description="Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.", category=category3)

session.add(item1)
session.commit()

item2 = Item(name="Harry Potter and the Prisoner of Azkaban", user_id=1,
             description="It's Harry's third year at Hogwarts; not only does he have a new Defense Against the Dark Arts teacher, but there is also trouble brewing. Convicted murderer Sirius Black has escaped the Wizards' Prison and is coming after Harry.", category=category3)

session.add(item2)
session.commit()

item3 = Item(name="The Hobbit", user_id=1,
             description="A reluctant Hobbit, Bilbo Baggins, sets out to the Lonely Mountain with a spirited group of dwarves to reclaim their mountain home, and the gold within it from the dragon Smaug.", category=category3)

session.add(item3)
session.commit()

# Items for Action/Adventure
category4 = Category(name="Action/Adventure", user_id=1)

session.add(category4)
session.commit()

item1 = Item(name="The Bourne Identity", user_id=1,
             description="A man is picked up by a fishing boat, bullet-riddled and suffering from amnesia, before racing to elude assassins and regain his memory.", category=category4)

session.add(item1)
session.commit()

item2 = Item(name="Sherlock Holmes", user_id=1,
             description="Sherlock Holmes and his sidekick Dr. Watson join forces to outwit and bring down their fiercest adversary, Professor Moriarty.", category=category4)

session.add(item2)
session.commit()

item3 = Item(name="John Wick", user_id=1,
             description="An ex-hitman comes out of retirement to track down the gangsters that took everything from him.", category=category4)


session.add(item3)
session.commit()

# Items for Romance
category5 = Category(name="Romance", user_id=1)

session.add(category5)
session.commit()

item1 = Item(name="Love Actually", user_id=1,
             description="Follows the lives of eight very different couples in dealing with their love lives in various loosely interrelated tales all set during a frantic month before Christmas in London, England.", category=category5)

session.add(item1)
session.commit()

item2 = Item(name="Beauty and the Beast", user_id=1,
             description="An adaptation of the fairy tale about a monstrous-looking prince and a young woman who fall in love.", category=category5)

session.add(item2)
session.commit()

item3 = Item(name="La La Land", user_id=1,
             description="While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.", category=category5)


session.add(item3)
session.commit()

categories = session.query(Category).all()
for category in categories:
    print "Add Category: " + category.name
