#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models


class Amenity(BaseModel, Base):
    """ The amenity class """
    __tablename__ = 'amenities'

    if models.storage_t == "db":
        name = Column(String(128), nullable=False)
    else:
        name = ""
