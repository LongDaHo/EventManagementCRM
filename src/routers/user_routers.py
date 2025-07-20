from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List

from services.user_services import create_user, get_user_based_on_query
from models.crm_items import User
from models.query_inputs import UserQueryInput

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/create-user")
async def create_user_handler(user: User):
    await create_user(user)
    return JSONResponse(content={"message": "User created successfully"}, status_code=200)

@user_router.post("/get-users")
async def get_users_handler(queries: List[UserQueryInput]):
    try:
        responses = await get_user_based_on_query(queries)
        return JSONResponse(content=responses, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": str(e)}, status_code=200)