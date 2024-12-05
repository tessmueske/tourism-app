from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt
from config import db

bcrypt = Bcrypt()

traveler_advertiser = db.Table('traveler_advertiser',
    db.Column('traveler_id', db.Integer, db.ForeignKey('travelers.id'), primary_key=True),
    db.Column('advertiser_id', db.Integer, db.ForeignKey('advertisers.id'), primary_key=True))

traveler_localexpert = db.Table('traveler_localexpert',
    db.Column('traveler_id', db.Integer, db.ForeignKey('travelers.id'), primary_key=True),
    db.Column('localexpert_id', db.Integer, db.ForeignKey('localexperts.id'), primary_key=True))

advertiser_localexpert = db.Table('advertiser_localexpert',
    db.Column('advertiser_id', db.Integer, db.ForeignKey('advertisers.id'), primary_key=True),
    db.Column('localexpert_id', db.Integer, db.ForeignKey('localexperts.id'), primary_key=True))

traveler_post = db.Table('traveler_post',
    db.Column('traveler_id', db.Integer, db.ForeignKey('travelers.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True))

localexpert_post = db.Table('localexpert_post',
    db.Column('localexpert_id', db.Integer, db.ForeignKey('localexperts.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True))

advertiser_post = db.Table('advertiser_post',
    db.Column('advertiser_id', db.Integer, db.ForeignKey('advertisers.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True))

traveler_hashtag = db.Table('traveler_hashtag',
    db.Column('traveler_id', db.Integer, db.ForeignKey('travelers.id'), primary_key=True),
    db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtags.id'), primary_key=True))

localexpert_hashtag = db.Table('localexpert_hashtag',
    db.Column('localexpert_id', db.Integer, db.ForeignKey('localexperts.id'), primary_key=True),
    db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtags.id'), primary_key=True))

advertiser_hashtag = db.Table('advertiser_hashtag',
    db.Column('advertiser_id', db.Integer, db.ForeignKey('advertisers.id'), primary_key=True),
    db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtags.id'), primary_key=True))

post_hashtag = db.Table('post_hashtag',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtags.id'), primary_key=True))

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

    hashtags = db.relationship('Hashtag', secondary=traveler_hashtag, back_populates='travelers')
    localexperts = db.relationship('LocalExpert', secondary=traveler_localexpert, back_populates='travelers')
    advertisers = db.relationship('Advertiser', secondary=traveler_advertiser, back_populates='travelers')
    posts = db.relationship('Post', secondary=traveler_post, back_populates='travelers')

    serialize_rules = ('-hashtags.travelers', '-localexperts.travelers', '-advertisers.travelers', '-posts.travelers')

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

    hashtags = db.relationship('Hashtag', secondary=localexpert_hashtag, back_populates='localexperts')
    travelers = db.relationship('Traveler', secondary=traveler_localexpert, back_populates='localexperts')
    advertisers = db.relationship('Advertiser', secondary=advertiser_localexpert, back_populates='localexperts')
    posts = db.relationship('Post', secondary=localexpert_post, back_populates='localexperts')

    serialize_rules = ('-hashtags.localexperts', '-travelers.localexperts', '-advertisers.localexperts', '-posts.localexperts')

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

    hashtags = db.relationship('Hashtag', secondary=advertiser_hashtag, back_populates='advertisers')
    travelers = db.relationship('Traveler', secondary=traveler_advertiser, back_populates='advertisers')
    localexperts = db.relationship('LocalExpert', secondary=advertiser_localexpert, back_populates='advertisers')
    posts = db.relationship('Post', secondary=advertiser_post, back_populates='advertisers')

    serialize_rules = ('-hashtags.advertisers', '-travelers.advertisers', '-localexperts.advertisers', '-posts.advertisers')

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
    body = db.Column(db.String)

    traveler_id = db.Column(db.Integer, db.ForeignKey('travelers.id'), nullable=True)
    localexpert_id = db.Column(db.Integer, db.ForeignKey('localexperts.id'), nullable=True)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertisers.id'), nullable=True)

    hashtags = db.relationship('Hashtag', secondary='post_hashtag', back_populates='posts')
    localexperts = db.relationship('LocalExpert', secondary=localexpert_post, back_populates='posts')
    advertisers = db.relationship('Advertiser', secondary=advertiser_post, back_populates='posts')
    travelers = db.relationship('Traveler', secondary=traveler_post, back_populates='posts')

    serialize_rules = ('-hashtags.posts','-travelers.posts', '-localexperts.posts', '-advertisers.posts')

class Hashtag(db.Model, SerializerMixin):
    __tablename__ = 'hashtags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    posts = db.relationship('Post', secondary=post_hashtag, back_populates='hashtags')
    localexperts = db.relationship('LocalExpert', secondary=localexpert_hashtag, back_populates='hashtags')
    travelers = db.relationship('Traveler', secondary=traveler_hashtag, back_populates='hashtags')
    advertisers = db.relationship('Advertiser', secondary=advertiser_hashtag, back_populates='hashtags')

    serialize_rules = ('-posts.hashtags', '-localexperts.hashtags', '-travelers.hashtags', '-advertisers.hashtags')
