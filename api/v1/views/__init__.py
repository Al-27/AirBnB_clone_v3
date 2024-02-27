"""
Please refer to the documentation provided in the README.md,
which can be found at gorpyter's PyPI URL: https://pypi.org/project/gorpyter/
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *