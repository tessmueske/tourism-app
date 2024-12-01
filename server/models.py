from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt
from config import db
from flask_mail import Message

bcrypt = Bcrypt()

traveler_advertiser = db.Table('traveler_advertiser',
    db.Column('traveler_id', db.Integer, db.ForeignKey('travelers.id'), primary_key=True),
    db.Column('advertiser_id', db.Integer, db.ForeignKey('advertisers.id'), primary_key=True))

traveler_island = db.Table('traveler_island',
    db.Column('traveler_id', db.Integer, db.ForeignKey('travelers.id'), primary_key=True),
    db.Column('island_id', db.Integer, db.ForeignKey('islands.id'), primary_key=True))

traveler_localexpert = db.Table('traveler_localexpert',
    db.Column('traveler_id', db.Integer, db.ForeignKey('travelers.id'), primary_key=True),
    db.Column('localexpert_id', db.Integer, db.ForeignKey('localexperts.id'), primary_key=True))

traveler_activity = db.Table(
    'traveler_activity',
    db.Column('traveler_id', db.Integer, db.ForeignKey('travelers.id'), primary_key=True),
    db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True))
    
localexpert_island = db.Table('localexpert_island',
    db.Column('localexpert_id', db.Integer, db.ForeignKey('localexperts.id'), primary_key=True),
    db.Column('island_id', db.Integer, db.ForeignKey('islands.id'), primary_key=True))

localexpert_activity = db.Table('localexpert_activity',
    db.Column('localexpert_id', db.Integer, db.ForeignKey('localexperts.id'), primary_key=True),
    db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True))

advertiser_localexpert = db.Table('advertiser_localexpert',
    db.Column('advertiser_id', db.Integer, db.ForeignKey('advertisers.id'), primary_key=True),
    db.Column('localexpert_id', db.Integer, db.ForeignKey('localexperts.id'), primary_key=True))

advertiser_island = db.Table('advertiser_island',
    db.Column('advertiser_id', db.Integer, db.ForeignKey('advertisers.id'), primary_key=True),
    db.Column('island_id', db.Integer, db.ForeignKey('islands.id'), primary_key=True))

advertiser_activity = db.Table('advertiser_activity',
    db.Column('advertiser_id', db.Integer, db.ForeignKey('advertisers.id'), primary_key=True),
    db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True))

island_activity = db.Table('island_activity',
    db.Column('island_id', db.Integer, db.ForeignKey('islands.id'), primary_key=True),
    db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True))

traveler_post = db.Table('traveler_post',
    db.Column('traveler_id', db.Integer, db.ForeignKey('travelers.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True))

localexpert_post = db.Table('localexpert_post',
    db.Column('localexpert_id', db.Integer, db.ForeignKey('localexperts.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True))

advertiser_post = db.Table('advertiser_post',
    db.Column('advertiser_id', db.Integer, db.ForeignKey('advertisers.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True))

island_post = db.Table('island_post',
    db.Column('island_id', db.Integer, db.ForeignKey('islands.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True))

activity_post = db.Table('activity_post',
    db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True))

class Traveler(db.Model, SerializerMixin):
    __tablename__ = 'travelers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=True, unique=False)
    age = db.Column(db.Integer, nullable=True, unique=False)
    bio = db.Column(db.String, nullable=True, unique=False)
    gender = db.Column(db.String, nullable=True, unique=False)

    islands = db.relationship('Island', secondary=traveler_island, back_populates ='travelers')
    localexperts = db.relationship('LocalExpert', secondary=traveler_localexpert, back_populates='travelers')
    advertisers = db.relationship('Advertiser', secondary=traveler_advertiser, back_populates='travelers')
    activities = db.relationship ('Activity', secondary=traveler_activity, back_populates='travelers')
    posts = db.relationship('Post', secondary=traveler_post, back_populates='travelers')

    serialize_rules = ('-islands.travelers', '-localexperts.travelers', '-advertisers.travelers', '-activities.travelers')

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password is not a readable attribute.")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

class LocalExpert(db.Model, SerializerMixin):
    __tablename__ = 'localexperts'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    notes = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default="pending") #pending, approved, or rejected
    name = db.Column(db.String, nullable=True, unique=False)
    age = db.Column(db.Integer, nullable=True, unique=False)
    bio = db.Column(db.String, nullable=True, unique=False)
    gender = db.Column(db.String, nullable=True, unique=False)

    islands = db.relationship('Island', secondary=localexpert_island, back_populates='localexperts')
    travelers = db.relationship('Traveler', secondary=traveler_localexpert, back_populates='localexperts')
    activities = db.relationship ('Activity', secondary=localexpert_activity, back_populates='localexperts')
    advertisers = db.relationship('Advertiser', secondary=advertiser_localexpert, back_populates='localexperts')
    posts = db.relationship('Post', secondary=localexpert_post, back_populates='localexperts')

    serialize_rules = ('-islands.localexperts', '-travelers.localexperts', '-activities.localexperts')

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password is not a readable attribute.")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

class Advertiser(db.Model, SerializerMixin):
    __tablename__ = 'advertisers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    notes = db.Column(db.String, nullable=True) #for signup
    status = db.Column(db.String, default="pending") #pending, approved, or rejected
    name = db.Column(db.String, nullable=True, unique=False)
    age = db.Column(db.Integer, nullable=True, unique=False)
    bio = db.Column(db.String, nullable=True, unique=False)
    gender = db.Column(db.String, nullable=True, unique=False)

    islands = db.relationship('Island', secondary=advertiser_island, back_populates='advertisers')
    travelers = db.relationship('Traveler', secondary=traveler_advertiser, back_populates='advertisers')
    activities = db.relationship ('Activity', secondary=advertiser_activity, back_populates='advertisers')
    localexperts = db.relationship('LocalExpert', secondary=advertiser_localexpert, back_populates='advertisers')
    posts = db.relationship('Post', secondary=advertiser_post, back_populates='advertisers')

    serialize_rules = ('-islands.advertisers', '-travelers.advertisers', '-activities.advertisers')

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password is not a readable attribute.")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    subject = db.Column(db.String)
    text = db.Column(db.String)
    hashtag = db.Column(db.String)

    localexperts = db.relationship('LocalExpert', secondary=localexpert_post, back_populates='posts')
    advertisers = db.relationship('Advertiser', secondary=advertiser_post, back_populates='posts')
    travelers = db.relationship('Traveler', secondary=traveler_post, back_populates='posts')
    activities = db.relationship('Activity', secondary=activity_post, back_populates='posts')
    islands = db.relationship('Island', secondary=island_post, back_populates='posts')

    serialize_rules = ('-travelers.posts', '-localexperts.posts', '-advertisers.posts', '-activities.posts', '-islands.posts')

class Activity(db.Model, SerializerMixin): 
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)

    islands = db.relationship('Island', secondary=island_activity, back_populates='activities')
    localexperts = db.relationship('LocalExpert', secondary=localexpert_activity, back_populates='activities')
    travelers = db.relationship('Traveler', secondary=traveler_activity, back_populates='activities')
    advertisers = db.relationship('Advertiser', secondary=advertiser_activity, back_populates='activities')
    posts = db.relationship('Post', secondary=activity_post, back_populates='activities')

    serialize_rules = ('-islands.activities', '-localexperts.activities', '-travelers.activities', '-advertisers.activities')

class Island(db.Model, SerializerMixin):
    __tablename__ = 'islands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
 
    localexperts = db.relationship('LocalExpert', secondary=localexpert_island, back_populates='islands')
    advertisers = db.relationship('Advertiser', secondary=advertiser_island, back_populates='islands')
    travelers = db.relationship('Traveler', secondary=traveler_island, back_populates='islands')
    activities = db.relationship('Activity', secondary=island_activity, back_populates='islands')
    posts = db.relationship('Post', secondary=island_post, back_populates='islands')

    serialize_rules = ('-localexperts.islands', '-advertisers.islands', '-travelers.islands', '-activities.islands')
