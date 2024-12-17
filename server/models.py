from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from flask_bcrypt import Bcrypt
from config import db
from datetime import datetime

bcrypt = Bcrypt()

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

    posts = db.relationship('Post', back_populates='traveler')

    serialize_rules = ('-posts.traveler',)

    @property
    def role(self):
        return "traveler"

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

    posts = db.relationship('Post', back_populates='localexpert')

    serialize_rules = ('-posts.localexpert',)

    @property
    def role(self):
        return "local expert"

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

    posts = db.relationship('Post', back_populates='advertiser')

    serialize_rules = ('-posts.advertiser',)

    @property
    def role(self):
        return "advertiser"

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
    date = db.Column(db.DateTime, default=func.now(), nullable=True)
    subject = db.Column(db.String)
    body = db.Column(db.String)
    comments = db.Column(db.JSON, nullable=True, default=[])

    traveler_id = db.Column(db.Integer, db.ForeignKey('travelers.id'), nullable=True)
    localexpert_id = db.Column(db.Integer, db.ForeignKey('localexperts.id'), nullable=True)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertisers.id'), nullable=True)

    hashtags = db.relationship('Hashtag', secondary=post_hashtag, back_populates='posts')
    localexpert = db.relationship('LocalExpert', back_populates='posts')
    advertiser = db.relationship('Advertiser', back_populates='posts')
    traveler = db.relationship('Traveler', back_populates='posts')

    serialize_rules = ('-hashtags.posts','-traveler.posts', '-localexpert.posts', '-advertiser.posts')

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=func.now(), nullable=True)
    text = db.Column(db.String)

    traveler_id = db.Column(db.Integer, db.ForeignKey('travelers.id'), nullable=True)
    localexpert_id = db.Column(db.Integer, db.ForeignKey('localexperts.id'), nullable=True)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertisers.id'), nullable=True)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @property
    def role(self):
        if self.traveler_id:
            return "traveler"
        elif self.localexpert_id:
            return "local expert"
        elif self.advertiser_id:
            return "advertiser"
        return "unknown"

class Hashtag(db.Model, SerializerMixin):
    __tablename__ = 'hashtags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    posts = db.relationship('Post', secondary=post_hashtag, back_populates='hashtags')

    serialize_rules = ('-posts.hashtags', '-localexperts.hashtags', '-travelers.hashtags', '-advertisers.hashtags')