from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

# Models go here!

class Traveler(db.Model, SerializerMixin):
     __tablename__ = 'travelers'

class Island(db.Model, SerializerMixin):
     __tablename__ = 'islands'

class Guide(db.Model, SerializerMixin):
     __tablename__ = 'guides'

class LocalExpert(db.Model, SerializerMixin):
     __tablename__ = 'localexperts'

class Advertiser(db.Model, SerializerMixin):
     __tablename__ = 'advertisers'