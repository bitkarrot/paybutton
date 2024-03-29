import asyncio

from fastapi import APIRouter

from lnbits.db import Database
from lnbits.helpers import template_renderer
from lnbits.tasks import catch_everything_and_restart

db = Database("ext_paybutton")

paybutton_ext: APIRouter = APIRouter(prefix="/paybutton", tags=["paybutton"])

paybutton_static_files = [
    {
        "path": "/paybutton/static",
        "name": "paybutton_static",
    }
]


def paybutton_renderer():
    return template_renderer(["paybutton/templates"])


from .tasks import wait_for_paid_invoices
from .views import *  # noqa: F401,F403
from .views_api import *  # noqa: F401,F403


def paybutton_start():
    loop = asyncio.get_event_loop()
    loop.create_task(catch_everything_and_restart(wait_for_paid_invoices))
