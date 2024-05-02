#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
"""
place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))
"""


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    # city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review",  backref="places", cascade="delete")
    # amenities = relationship("Amenity", secondary="place_amenity",
    #                         viewonly=False)

    if models.storage_t != 'db':
        @property
        def reviews(self):
            ''' get list of cities related to State '''
            res = []

            reviews = models.storage.all('Review')
            for rev in reviews.values():
                if rev.place_id == self.id:
                    res.append(rev)
            return (res)

        @property
        def amenities(self):
            ''' get list of cities related to State '''
            res = []

            amenities = models.storage.all('Amenity')
            for amin in amenities.values():
                if amin.place_id == self.id:
                    res.append(amin)
            return (res)
