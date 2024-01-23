from http import HTTPStatus
import json

import httpx
from fastapi import Depends, Query, Request
from lnurl import decode as decode_lnurl
from loguru import logger
from starlette.exceptions import HTTPException
from starlette.responses import FileResponse

from lnbits.core.crud import get_user
from lnbits.core.models import Payment
from lnbits.core.services import create_invoice
from lnbits.core.views.api import api_payment
from lnbits.decorators import (
    WalletTypeInfo,
    check_admin,
    get_key_type,
    require_admin_key,
    require_invoice_key,
)

from . import compliance_ext


#######################################
##### ADD YOUR API ENDPOINTS HERE #####
#######################################

## Get all possible regions

@compliance_ext.get("/api/v1/regions", status_code=HTTPStatus.OK)
async def api_compliances():
    url = "https://raw.githubusercontent.com/lnbits/Compiance/main/static/docs/region.json"
    try:
        response = await httpx.get(url)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail="Unable to fetch data from the URL")

    data = response.json()
    return data

## Get a single record from a region

@compliance_ext.get("/api/v1/{region}", status_code=HTTPStatus.OK)
async def api_compliance(
    region: str
):
    url = f"https://raw.githubusercontent.com/lnbits/Compiance/main/static/docs/{region}/README.md"
    try:
        response = await httpx.get(url)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail="Unable to fetch data from the URL")
    return response
