#!/usr/bin/python3
"""This api module """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

if app_views is not None:
    from .index import *
    from .states import *
    from .cities import *
    from .amenities import *
    from .users import *
    from .places import *
    from .places_reviews import *
