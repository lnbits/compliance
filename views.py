from http import HTTPStatus

from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse

from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.settings import settings

from . import compliance_ext, compliance_renderer

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

@compliance_ext.get("/{region}")
async def compliance(request: Request, region):
    return compliance_renderer().TemplateResponse(
        "compliance/compliance.html",
        {
            "request": request,
            "region": region,
            "web_manifest": f"/compliance/manifest/{region}.webmanifest",
        },
    )


# Manifest for public page, customise or remove manifest completely

@compliance_ext.get("/manifest/{region}.webmanifest")
async def manifest(compliance_id: str):
    regionDoc = api_compliance(region)
    if not regionDoc:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Compliance doc does not exist."
        )

    return {
        "short_name": settings.lnbits_site_title,
        "name": region + " compliance doc" " - " + settings.lnbits_site_title,
        "icons": [
            {
                "src": settings.lnbits_custom_logo
                if settings.lnbits_custom_logo
                else "https://cdn.jsdelivr.net/gh/lnbits/lnbits@0.3.0/docs/logos/lnbits.png",
                "type": "image/png",
                "sizes": "900x900",
            }
        ],
        "start_url": "/compliance/" + region,
        "background_color": "#1F2234",
        "description": "Complaince doc for " + region + " - " + settings.lnbits_site_title,
        "display": "standalone",
        "scope": "/compliance/" + region,
        "theme_color": "#1F2234",
        "shortcuts": [
            {
                "name": region + " - " + settings.lnbits_site_title,
                "short_name": region,
                "description": region + " - " + settings.lnbits_site_title,
                "url": "/compliance/" + region,
            }
        ],
    }