from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Post(db.Model):
    __tablename__ = 'posts'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, id, note, image):
        self.userID = id
        self.note = note
        self.image = image

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "userID": self.userID,
            "note": self.note,
            "image": self.image,
            "base64": str(file_encode)
        }
        
class Stock_Transactions(db.Model):
    __tablename__ = 'stock_transactions'
   
    # define the stock schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _uid = db.Column(db.String(255), unique=False, nullable=False)
    _symbol = db.Column(db.String(255),unique=False,nullable=False)
    _transaction_type = db.Column(db.String(255),unique=False,nullable=False)
    _quantity = db.Column(db.String(255),unique=False,nullable=False)
    _transaction_amount = db.Column(db.Integer, nullable=False)
    # constructor of a User object, initializes the instance variables within object (self)

    def _init_(self,uid,symbol,transaction_type,quantity,transaction_amount):
        self._uid = uid
        self._symbol = symbol
        self._transaction_type = transaction_type
        self._quantity = quantity
        self._transaction_amount = transaction_amount
    
    # uid
    @property
    def uid(self):
        return self._uid
    
    @uid.setter
    def uid(self,uid):
        self._uid = uid
        
    # symbol
    @property
    def symbol(self):
        return self._symbol
    
    @symbol.setter
    def symbol(self,symbol):
        self._symbol = symbol
        
    # transaction type
    @property
    def transaction_type(self):
        return self._transaction_type
    
    @transaction_type.setter
    def transaction_type(self,transaction_type):
        self._transaction_type = transaction_type
        
    #quantity
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self,quantity):
        self._quantity = quantity
        
    #transaction amount
    @property
    def transaction_amount(self):
        return self._transaction_amount
    
    @transaction_amount.setter
    def transaction_amount(self,transaction_amount):
        self._transaction_amount = transaction_amount
        
        
     # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())
    
    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None
        
    
    # CRUD update: updates user name, password, phone
    # returns self

    def update(self,uid="",symbol="",transaction_type="",quantity="",transaction_amount=""):
        """only updates values with length"""
        if len(uid) > 0:
            self.uid = uid
        if len(symbol) > 0:
            self.symbol = symbol
        if len(transaction_type) > 0:
            self.transaction_type = transaction_type
        if len(quantity) > 0:
            self.quantity = quantity
        if len(transaction_amount) > 0:
            self.transaction_amount = transaction_amount           
        db.session.commit()
        return self
    
    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "symbol": self.symbol,
            "transaction_type": self.transaction_type,
            "quantity": self.quantity,
            "transaction_amount": self.transaction_amount
        }

class Stocks(db.Model):
    _tablename_ = 'stocks'
    
    # define the stock schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _symbol = db.Column(db.String(255),unique=False,nullable=False)
    _company = db.Column(db.String(255),unique=False,nullable=False)
    _quantity = db.Column(db.Integer,unique=False,nullable=False)
    _sheesh = db.Column(db.Integer,unique=False,nullable=False)
    
    # constructor of a User object, initializes the instance variables within object (self)
    def _init_(self,symbol,company,quantity,sheesh):
        self._symbol = symbol
        self._company = company
        self._quantity = quantity
        self._sheesh = sheesh
# symbol
    @property
    def symbol(self):
        return self._symbol
    
    @symbol.setter
    def symbol(self,symbol):
        self._symbol = symbol
#company
    @property
    def company(self):
        return self._company
    
    @company.setter
    def company(self,company):
        self._company = company
#quantity
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self,quantity):
        self._quantity = quantity

#cost
    @property
    def sheesh(self):
        return self._sheesh
    
    @sheesh.setter
    def sheesh(self,sheesh):
        self._sheesh = sheesh
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())
    
    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None
        
     # CRUD update: updates user name, password, phone
    # returns self
    def update(self,symbol="",company="",quantity=None):
        """only updates values with length"""
        if len(symbol) > 0:
            self.symbol = symbol
        #if sheesh > 0:
           # self.sheesh = sheesh
        if len(company) > 0:
            self.company = company
        if quantity is not None:
            self.quantity = quantity
        
        db.session.commit()
        return self
    
    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "company": self.company,
            "quantity": self.quantity,
            "sheesh": self.sheesh,
        }
    # Builds working data for testing
    def initUsers():
        with app.app_context():
            """Create database and tables"""
            db.create_all()

class House(db.Model):
    _tablename_ = 'houses'
    
    # define the house schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)

    _price = db.Column(db.Numeric, nullable=False)
    _beds = db.Column(db.Integer, nullable=False)
    _baths = db.Column(db.Integer, nullable=False)
    _address = db.Column(db.String(255), nullable=False)
    _lat = db.Column(db.String(255), nullable=False)
    _long = db.Column(db.String(255), nullable=False)
    _sqfeet = db.Column(db.Integer, nullable=False)
    _image = db.Column(db.String(255), nullable=False)
    
    
    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self,price,beds,baths, address, lat, long, sqfeet, image="image"):
        self._price = price
        self._beds = beds
        self._baths = baths
        self._address = address
        self._lat = lat
        self._long = long
        self._sqfeet = sqfeet
        self._image = image
        #fill rest
# price
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self,price):
        self._price = price
#beds
    @property
    def beds(self):
        return self._beds
    
    @beds.setter
    def beds(self,beds):
        self._beds = beds
#baths
    @property
    def baths(self):
        return self._baths
    
    @baths.setter
    def baths(self,baths):
        self._baths = baths
#address

    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self,address):
        self._address = address
#lat
    @property
    def lat(self):
        return self._lat
    
    @lat.setter
    def lat(self,lat):
        self._lat = lat
#long
    
    @property
    def long(self):
        return self._long
    
    @long.setter
    def long(self,long):
        self._long = long
#sqfeet
        
    @property
    def sqfeet(self):
        return self._sqfeet
    
    @sqfeet.setter
    def sqfeet(self,sqfeet):
        self._sqfeet = sqfeet

#image
        
    @property
    def image(self):
        return self._image
    
    @image.setter
    def image(self,image):
        self._image = image

    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())
    
    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None
        
     # CRUD update: updates user name, password, phone
    # returns self
    def update(self,price="",beds="", baths="", sqft="", address="", image=""):
        """only updates values with length"""
        if price != "":
            self.price = price
        if beds != "":
            self.beds = beds
        if baths != "":
            self.baths = baths
        if sqft != "":
            self.sqfeet = sqft
        if address != "":
            self.address = address
        if image != "":
            self.image = image
        db.session.commit()
        return self
    
    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
        "price": "$"+str(int(self.price)),
        "beds": self.beds,
        "baths": self.baths,
        "address": self.address,
        "lat": self.lat,
        "long": self.long,
        "sqfeet":self.sqfeet,
        "image":self.image
    }

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    # Builds working data for testing
    def initUsers():
        with app.app_context():
            """Create database and tables"""
            db.create_all()


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _dob = db.Column(db.Date)
    _pnum = db.Column(db.String(255), unique=False, nullable=True)
    _role = db.Column(db.String(20), default="User", nullable=False)
    _stockmoney = db.Column(db.Integer, unique=False, nullable=False)

    
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, pnum, stockmoney, password="123qwerty", dob=date.today(), role="User"): #role="User"
        self._name = name
        self._uid = uid
        self._stockmoney = stockmoney
        self.set_password(password)
        self._dob = dob
        self._pnum = pnum
        self._role = role

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def stockmoney(self):
        return self._stockmoney
    
    # a setter function, allows name to be updated after initial object creation
    @stockmoney.setter
    def stockmoney(self, stockmoney):
        self._stockmoney = stockmoney
    
    @property
    def role(self):
        return self._role
    
    @role.setter
    def role(self, role):
        self._role = role

    def is_admin(self):
        return self._role == "Admin"
    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
    @property
    def password(self):
        return self._password[0:10] + "..." # because of security only show 1st characters

    # update password, this is conventional setter
    def set_password(self, password):
        """Create a hashed password."""
        self._password = generate_password_hash(password, "pbkdf2:sha256", salt_length=10)

    # check password parameter versus stored/encrypted password
    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def dob(self):
        dob_string = self._dob.strftime('%m-%d-%Y')
        return dob_string
    
    # dob should be have verification for type date
    @dob.setter
    def dob(self, dob):
        self._dob = dob
    
    @property
    def age(self):
        today = date.today()
        return today.year - self._dob.year - ((today.month, today.day) < (self._dob.month, self._dob.day))

    @property
    def pnum(self):
        return self._pnum
    
    @pnum.setter
    def pnum(self, pnum):
        self._pnum = pnum
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            print(IntegrityError)
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "stockmoney": self.stockmoney,
            "dob": self.dob,
            "age": self.age,
            "pnum": self.pnum,
            "role": self.role, 
            "posts": [post.read() for post in self.posts]
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", password="", pnum="", stockmoney=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        if len(pnum) > 0:
            self.pnum = pnum
        if stockmoney == '':
            self.stockmoney = stockmoney
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        
            