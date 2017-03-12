from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    auction_items = relationship("Item", backref="owner")
    bids_placed = relationship("Bid", backref="bidder")
    
    def __str__(self):
        return ("User {!r}: username={!r}, password = {!r}".format(self.id, self.username, self.password,))


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bids = relationship("Bid", backref="item_bid_on")


class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    
    bidder_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    
    def __str__(self):
        return ("Bid: {!r} for price {!r}".format(self.id, self.price,))
    
    
Base.metadata.create_all(engine)



##creating users
mike = User(username="Mike", password="1234abc")
steve = User(username="Steve", password="1234abc")
carl = User(username="Carl", password="1234abc")

session.add_all(mike, steve, carl)
session.commit()

##creating items
baseball = Item(name="Baseball")
mike.auction_items.append(baseball)
print(mike, mike.auction_items)
print(baseball.owner.username)

session.add(baseball)
session.commit()

## adding bids
bid1 = Bid(10.50)
bid2 = Bid(20.75)
bid3 = Bid(11.30)
bid4 = Bid(50.9)
steve.bids_placed.append(bid1, bid2)
carl.bids_placed.append(bid3, bid4)

session.add_all(bid1,bid2,bid3,bid4)
session.commit()