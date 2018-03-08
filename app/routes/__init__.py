from flask import Blueprint

bs = Blueprint('bs', __name__)

from . import business
from . import user
from . import reviews