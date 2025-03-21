# pylint: disable=too-many-positional-arguments,too-few-public-methods,too-many-arguments
# ignores too-many-arguments because it's normal using create tokens function

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer

from src.settings import Settings, get_settings


sync_token = HTTPBearer()


async def verify_sync_token(
    credentials: HTTPBearer = Security(sync_token), settings: Settings = Depends(get_settings)
) -> str:
    """
    Verify the sync token from the header.
    Returns the token if valid, raises HTTPException if invalid.
    """

    if not credentials:
        raise HTTPException(status_code=401, detail="Sync token is missing")

    token = credentials.credentials  # type: ignore
    if token != settings.SYNC_TOKEN.get_secret_value():
        raise HTTPException(status_code=401, detail="Invalid sync token")

    return token
