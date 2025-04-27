# mercadopago_service.py
import httpx
from fastapi import status
from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.schemas.mercadopago import CheckoutRequest
from app.models.user import User
from sqlmodel import Session
from fastapi import HTTPException

class MercadoPagoService:
    @staticmethod
    def get_authorization_url(user_id: int):
        return (
            f"https://auth.mercadopago.com/authorization"
            f"?client_id={settings.MP_CLIENT_ID}"
            f"&response_type=code"
            f"&redirect_uri={settings.DOMAIN}/api/v1/mercadopago/connect"
            f"&state={user_id}"
        )

    @staticmethod
    async def connect(code: str, user_id: int, db: Session):
        tokens = await MercadoPagoService._exchange_code(code)
        
        user_repo = UserRepository(db)
        user = user_repo.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.mercadopago_access_token = tokens["access_token"]
        user.mercadopago_refresh_token = tokens.get("refresh_token")
        
        user_repo.update_tokens(user, tokens)
        return {"status": "success", "merchant_id": tokens.get("user_id")}

    @staticmethod
    async def _exchange_code(code: str):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://api.mercadopago.com/oauth/token",
                    data={
                        "client_secret": settings.MP_CLIENT_SECRET,
                        "client_id": settings.MP_CLIENT_ID,
                        "grant_type": "authorization_code",
                        "code": code,
                        "redirect_uri": f"{settings.DOMAIN}/api/v1/mercadopago/connect"
                    }
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail="Error en la autenticación con MercadoPago"
                )
            
    @staticmethod
    async def create_checkout(user: User, checkout_data: CheckoutRequest, db: Session):
        if not user.mercadopago_access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario no tiene vinculada cuenta de MercadoPago"
            )
        
        payload = {
            "items": [
                {
                    "title": item.title,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "description": item.description or "",
                    "currency_id": "ARS" 
                } for item in checkout_data.items
            ],
            "back_urls": {
                "success": checkout_data.success_url,
                "failure": checkout_data.failure_url,
                "pending": checkout_data.pending_url
            },
            "auto_return": "approved",
            "notification_url": f"{settings.DOMAIN}/api/v1/mercadopago/webhook",
            "marketplace_fee": 500,
            "metadata": {
                "user_id": user.id,
                "email": user.email
            }
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://api.mercadopago.com/checkout/preferences",
                    headers={
                        "Authorization": f"Bearer {user.mercadopago_access_token}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Error en MercadoPago: {e.response.text}"
                )
        
        preference = response.json()
        return {
            "checkout_url": preference["init_point"],
            "preference_id": preference["id"]
        }