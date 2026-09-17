from fastapi import APIRouter
from starlette import status

router_auth = APIRouter(prefix="/Auth" , tags=["Authentification"])


@router_auth.post("", status_code=status.HTTP_200_OK)
async def inscription ():
    return{"msg":"bonjour"}


