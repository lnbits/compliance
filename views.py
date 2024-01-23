from http import HTTPStatus

from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse

from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.settings import settings

from . import compliance_ext, compliance_renderer
from .crud import get_compliance

temps = Jinja2Templates(directory="temps")


#######################################
##### ADD YOUR PAGE ENDPOINTS HERE ####
#######################################


# Backend admin page

@compliance_ext.get("/", response_class=HTMLResponse)
async def index(request: Request, user: User = Depends(check_user_exists)):
    return compliance_renderer().TemplateResponse(
        "compliance/index.html", {"request": request, "user": user.dict()}
    )


# Frontend shareable page

@compliance_ext.get("/{compliance_id}")
async def compliance(request: Request, compliance_id):
    compliance = await get_compliance(compliance_id, request)
    if not compliance:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Compliance does not exist."
        )
    return compliance_renderer().TemplateResponse(
        "compliance/compliance.html",
        {
            "request": request,
            "compliance_id": compliance_id,
            "lnurlpay": compliance.lnurlpay,
            "lnurlwithdraw": compliance.lnurlwithdraw,
            "web_manifest": f"/compliance/manifest/{compliance_id}.webmanifest",
        },
    )


# Manifest for public page, customise or remove manifest completely

@compliance_ext.get("/manifest/{compliance_id}.webmanifest")
async def manifest(compliance_id: str):
    compliance= await get_compliance(compliance_id)
    if not compliance:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Compliance does not exist."
        )

    return {
        "short_name": settings.lnbits_site_title,
        "name": compliance.name + " - " + settings.lnbits_site_title,
        "icons": [
            {
                "src": settings.lnbits_custom_logo
                if settings.lnbits_custom_logo
                else "https://cdn.jsdelivr.net/gh/lnbits/lnbits@0.3.0/docs/logos/lnbits.png",
                "type": "image/png",
                "sizes": "900x900",
            }
        ],
        "start_url": "/compliance/" + compliance_id,
        "background_color": "#1F2234",
        "description": "Minimal extension to build on",
        "display": "standalone",
        "scope": "/compliance/" + compliance_id,
        "theme_color": "#1F2234",
        "shortcuts": [
            {
                "name": compliance.name + " - " + settings.lnbits_site_title,
                "short_name": compliance.name,
                "description": compliance.name + " - " + settings.lnbits_site_title,
                "url": "/compliance/" + compliance_id,
            }
        ],
    }