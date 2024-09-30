from fastapi import APIRouter
from fastapi.responses import JSONResponse

router: APIRouter = APIRouter()


async def options_handler():
    return JSONResponse(status_code=200, headers={
        "Access-Control-Allow-Origin": "https://refined-density-297301.web.app",
        "Access-Control-Allow-Methods": "POST, PATCH, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
    })


@router.options("/register")
async def register_options_handler():
    await options_handler()


@router.options("/register/email_verification")
async def register_options_handler():
    await options_handler()


@router.options("/login")
async def login_options_handler():
    await options_handler()


@router.options("/change-password")
async def change_password_options_handler():
    await options_handler()


@router.options("/logout")
async def logout_options_handler():
    await options_handler()


@router.options("/ais_data")
async def ais_data_options_handler():
    await options_handler()


@router.options("/ais_data_A")
async def ais_data_a_options_handler():
    await options_handler()


@router.options("/getusers")
async def getusers_options_handler():
    await options_handler()
