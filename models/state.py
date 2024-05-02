#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import models
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City",  backref="state", cascade="delete")

    if models.storage_t != 'db':
        @property
        def cities(self):
            ''' get list of cities related to State '''
            res = []

            cities = models.storage.all('City')
            for cit in cities.values():
                if cit.state_id == self.id:
                    res.append(cit)
            return (res)
