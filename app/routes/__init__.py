from flask import Blueprint

bs = Blueprint('bs', __name__)
auth = Blueprint('auth', __name__)

from . import business
from . import user
from . import reviews