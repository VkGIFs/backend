from fastapi import APIRouter, Body, Depends

from backend.core.auth.handlers import verify_sync_token
from backend.db.connection.transaction import Transaction
from backend.exceptions import UserAlreadyRegisteredError
from backend.models.user import UserModel
from backend.schemas.user import UserCreateView


router = APIRouter(dependencies=[Depends(verify_sync_token)])


@router.post("/registration")
async def create_user(body: UserCreateView = Body(...)) -> str:
    """Create new user from telegram id"""

    async with Transaction():
        user = await UserModel.get_by_telegram_id(telegram_id=body.telegram_id)
        if user:
            raise UserAlreadyRegisteredError

        new_user = await UserModel.create(telegram_id=body.telegram_id, vk_access_token=body.vk_access_token)
        return str(new_user.id)
