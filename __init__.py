import asyncio

from fastapi import APIRouter
from lnbits.db import Database
from lnbits.helpers import template_renderer
from lnbits.tasks import catch_everything_and_restart

# Pointless, but LNbits complains if there is no database.
db = Database("ext_compliance")

compliance_ext: APIRouter = APIRouter(
    prefix="/compliance", tags=["Compliance"]
)

temp_static_files = [
    {
        "path": "/compliance/static",
        "name": "compliance_static",
    }
]

def compliance_renderer():
    return template_renderer(["compliance/templates"])

from .views import *
from .views_api import *