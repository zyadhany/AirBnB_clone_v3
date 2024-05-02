#!/usr/bin/python3
"""This module to make dp storage"""

import models
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {
            'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
            }


class DBStorage:
    """This class manages dp storage of hbnb"""
    __engine = None
    __session = None

    def __init__(self):
        """init for dp sttorage"""
        SQL_USER = getenv('HBNB_MYSQL_USER')
        SQL_PWD = getenv('HBNB_MYSQL_PWD')
        SQL_HOST = getenv('HBNB_MYSQL_HOST')
        SQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(SQL_USER, SQL_PWD,
                                             SQL_HOST, SQL_DB),
                                      pool_pre_ping=True)
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def delete(self, obj=None):
        """delete object from storage"""
        if obj is None:
            return
        self.__session.delete(obj)

    def close(self):
        """ deserializing the JSON file to objects """
        self.__session.remove()

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        res = {}
        if cls is None:
            cls = classes.keys()
        else:
            cls = [cls]

        for ind in cls:
            if ind not in classes:
                continue
            que = self.__session.query(classes[ind]).all()
            for obj in que:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                res[key] = obj
        return (res)

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.__session.add(obj)

    def save(self):
        """Saves storage dictionary to file"""
        self.__session.commit()

    def reload(self):
        """Loads storage dictionary from file"""
        Base.metadata.create_all(self.__engine)
        ses = sessionmaker(expire_on_commit=False,
                           bind=self.__engine)
        Session = scoped_session(ses)
        self.__session = Session
