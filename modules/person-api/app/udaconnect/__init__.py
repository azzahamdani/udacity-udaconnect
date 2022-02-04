import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# from app.udaconnect.models import Connection, Location, Person  # noqa
# from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema  # noqa

from app.udaconnect.models import Person  # noqa
from app.udaconnect.schemas import PersonSchema  # noqa


def register_routes(api, app, root="api"):
    from app.udaconnect.controllers import api as udaconnect_api

    api.add_namespace(udaconnect_api, path=f"/{root}")
