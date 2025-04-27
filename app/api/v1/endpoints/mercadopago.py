from fastapi import APIRouter, status, Depends, HTTPException, Request
from app.services.mercadopago_service import MercadoPagoService
from app.core.permissions import PermissionChecker
from app.models.user import User
from app.models.role import Role
from app.schemas.mercadopago import CheckoutRequest
from app.api.deps import get_db
from sqlmodel import Session



router = APIRouter(tags=["Mercado Pago Integration"])


@router.get("/get-auth-url", status_code=status.HTTP_200_OK)
async def get_auth_url(
    current_user: User = Depends(PermissionChecker([Role.SELLER]))
):
    return {
        "auth_url": MercadoPagoService.get_authorization_url(current_user.id)
    }


@router.get("/connect", status_code=status.HTTP_200_OK)
async def connect(
    code: str, 
    state: str,
    db: Session = Depends(get_db)
):
    try:
        user_id = int(state)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid state format")
    
    return await MercadoPagoService.connect(
        code=code,
        user_id=user_id,
        db=db
    )


@router.post("/create-checkout", status_code=status.HTTP_200_OK)
async def create_checkout(
    checkout_data: CheckoutRequest,
    current_user: User = Depends(PermissionChecker([Role.SELLER])),
    db: Session = Depends(get_db)
):
    return await MercadoPagoService.create_checkout(
        user=current_user,
        checkout_data=checkout_data,
        db=db
    )


@router.post("/webhook")
async def webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    data = await request.json()
    print(data)
    return {"status": "received", "data": data}