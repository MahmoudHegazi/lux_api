#!/usr/bin/env python3
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()



class BakeryLinks(Base):
    __tablename__ = 'bakery_links'

    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    market_place = Column(String(50))
    last_update = Column(String(255))
    last_update_text = Column(String(255))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'url': self.url,
            'market_place':self.market_place,
            'last_update':self.last_update,
            'last_update_text':self.last_update_text,
        }

class Bakery(Base):
    __tablename__ = 'bakery'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(String(60))
    image = Column(String(350))
    market_place = Column(String(50))
    last_update = Column(String(255))
    last_update_text = Column(String(255))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'market_place':self.market_place,
            'last_update':self.last_update,
            'last_update_text':self.last_update_text,
        }


class EggsLinks(Base):
    __tablename__ = 'eggs_links'

    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    market_place = Column(String(50))
    last_update = Column(String(255))
    last_update_text = Column(String(255))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'url': self.url,
            'market_place':self.market_place,
            'last_update':self.last_update,
            'last_update_text':self.last_update_text,
        }

class Eggs(Base):
    __tablename__ = 'eggs'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(String(60))
    image = Column(String(350))
    market_place = Column(String(50))
    last_update = Column(String(255))
    last_update_text = Column(String(255))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'market_place':self.market_place,
            'last_update':self.last_update,
            'last_update_text':self.last_update_text,
        }


class SeafoodLinks(Base):
    __tablename__ = 'seafood_links'

    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    market_place = Column(String(50))
    last_update = Column(String(255))
    last_update_text = Column(String(255))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'url': self.url,
            'market_place':self.market_place,
            'last_update':self.last_update,
            'last_update_text':self.last_update_text,
        }

class Seafood(Base):
    __tablename__ = 'seafood'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(String(60))
    image = Column(String(350))
    market_place = Column(String(50))
    last_update = Column(String(255))
    last_update_text = Column(String(255))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'market_place':self.market_place,
            'last_update':self.last_update,
            'last_update_text':self.last_update_text,
        }


class FruitsLinks(Base):
    __tablename__ = 'fruits_links'

    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    market_place = Column(String(50))
    last_update = Column(String(255))
    last_update_text = Column(String(255))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'url': self.url,
            'market_place':self.market_place,
            'last_update':self.last_update,
            'last_update_text':self.last_update_text,
        }

class Fruits(Base):
    __tablename__ = 'fruits'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(String(60))
    image = Column(String(350))
    market_place = Column(String(50))
    last_update = Column(String(255))
    last_update_text = Column(String(255))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'market_place':self.market_place,
            'last_update':self.last_update,
            'last_update_text':self.last_update_text,
        }


class FreshmeatLinks(Base):
    __tablename__ = 'fresh_meat_links'

    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    market_place = Column(String(50))
    last_update = Column(String(255))
    last_update_text = Column(String(255))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'url': self.url,
            'market_place':self.market_place,
            'last_update':self.last_update,
            'last_update_text':self.last_update_text,
        }

class FreshMeat(Base):
    __tablename__ = 'freshmeat'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(String(60))
    image = Column(String(350))
    market_place = Column(String(50))
    last_update = Column(String(255))
    last_update_text = Column(String(255))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'market_place':self.market_place,
            'last_update':self.last_update,
            'last_update_text':self.last_update_text,
        }


class FreshVegetablesLinks(Base):
    __tablename__ = 'fresh_vegetables_links'

    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    market_place = Column(String(50))
    last_update = Column(String(255))
    last_update_text = Column(String(255))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'url': self.url,
            'market_place':self.market_place,
            'last_update':self.last_update,
            'last_update_text':self.last_update_text,
        }

class FreshVegetables(Base):
    __tablename__ = 'freshvegetables'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(String(60))
    image = Column(String(350))
    market_place = Column(String(50))
    last_update = Column(String(255))
    last_update_text = Column(String(255))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'market_place':self.market_place,
            'last_update':self.last_update,
            'last_update_text':self.last_update_text,
        }

class NoodlesSupplementsLinks(Base):
    __tablename__ = 'noodles_supplements_links'

    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    market_place = Column(String(50))
    last_update = Column(String(255))
    last_update_text = Column(String(255))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'url': self.url,
            'market_place':self.market_place,
            'last_update':self.last_update,
            'last_update_text':self.last_update_text,
        }

class NoodlesSupplements(Base):
    __tablename__ = 'noodles_supplements'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(String(60))
    image = Column(String(350))
    market_place = Column(String(50))
    last_update = Column(String(255))
    last_update_text = Column(String(255))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'market_place':self.market_place,
            'last_update':self.last_update,
            'last_update_text':self.last_update_text,
        }

class OtherFreshFoodLinks(Base):
    __tablename__ = 'other_fresh_food_links'

    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    market_place = Column(String(50))
    last_update = Column(String(255))
    last_update_text = Column(String(255))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'url': self.url,
            'market_place':self.market_place,
            'last_update':self.last_update,
            'last_update_text':self.last_update_text,
        }

class OtherFreshFood(Base):
    __tablename__ = 'other_fresh_food'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(String(60))
    image = Column(String(350))
    market_place = Column(String(50))
    last_update = Column(String(255))
    last_update_text = Column(String(255))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'market_place':self.market_place,
            'last_update':self.last_update,
            'last_update_text':self.last_update_text,
        }
engine = create_engine('sqlite:///api_scaner.db')
Base.metadata.create_all(engine)
