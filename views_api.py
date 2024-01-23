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
async def api_compliances(
    req: Request, all_wallets: 
    bool = Query(False)
):
    wallet_ids = [wallet.wallet.id]
    if all_wallets:
        user = await get_user(wallet.wallet.user)
        wallet_ids = user.wallet_ids if user else []
    return [compliance.dict() for compliance in await get_compliances(wallet_ids, req)]

## Get a single record

@compliance_ext.get("/api/v1/{region}", status_code=HTTPStatus.OK)
async def api_compliance(
    req: Request,
    region: str):
    compliance = await get_region(region)
    if not compliance:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Record does not exist."
        )
    return myextension.dict()



return FileResponse(file_location, media_type='application/octet-stream',filename=file_name)