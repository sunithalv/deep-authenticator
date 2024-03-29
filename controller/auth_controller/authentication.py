from datetime import datetime, timedelta
from typing import Optional
import sys

from fastapi import APIRouter, HTTPException, Request, Response, status
from jose import JWTError, jwt
from pydantic import BaseModel
from starlette.responses import JSONResponse, RedirectResponse

from face_auth.business_val.user_val import LoginValidation, RegisterValidation
from face_auth.constant.auth_constant import ALGORITHM, SECRET_KEY
from face_auth.entity.user import User
from face_auth.exception import AppException


class Login(BaseModel):
    """Base model for login
    """

    email_id: str
    password: str


class Register(BaseModel):
    """
    Base model for register
    """

    Name: str
    username: str
    email_id: str
    ph_no: int
    password1: str
    password2: str


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={"401": {"description": "Not Authorized!!!"}},
)


# Getting current user for embedding generation/comparison
async def get_current_user(request: Request):
    """This function is used to get the current user

    Args:
        request (Request): Request from the route

    Returns:
        dict: Returns the username and uuid of the user
    """
    try:
        secret_key = SECRET_KEY
        algorithm = ALGORITHM

        token = request.cookies.get("access_token")
        if token is None:
            return None

        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        uuid: str = payload.get("sub")
        username: str = payload.get("username")

        if uuid is None or username is None:
            return logout(request)
        return {"uuid": uuid, "username": username}
    except JWTError:
        raise HTTPException(status_code=404, detail="Detail Not Found")
    except Exception as e:
        msg = "Error while getting current user"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": msg}
        )
        return response


def create_access_token(
    uuid: str, username: str, expires_delta: Optional[timedelta] = None
) -> str:
    """This function is used to create the access token

    Args:
        uuid (str): uuid of the user
        username (str): username of the user

    Raises:
        e: _description_

    Returns:
        _type_: _description_
    """

    try:
        secret_key = SECRET_KEY
        algorithm = ALGORITHM

        #Define payload of JWT token
        encode = {"sub": uuid, "username": username}
        #If value is set for expire, add value to current time
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        encode.update({"exp": expire})
        # return jwt.encode(encode, Configuration().SECRET_KEY, algorithm=Configuration().ALGORITHM)
        return jwt.encode(encode, secret_key, algorithm=algorithm)
    except Exception as e:
        raise AppException(e,sys)


@router.post("/token")
async def login_for_access_token(response: Response, login) -> dict:
    """Set the access token

    Returns:
        dict: response
    """

    try:
        user_validation = LoginValidation(login.email_id, login.password)
        user = user_validation.authenticate_user_login()
        if not user:
            return {"status": False, "uuid": None, "response": response}
        #Token expires after 15 minutes
        token_expires = timedelta(minutes=15)
        token = create_access_token(
            user["UUID"], user["username"], expires_delta=token_expires
        )
        response.set_cookie(key="access_token", value=token, httponly=True)
        return {"status": True, "uuid": user["UUID"], "response": response}
    except Exception as e:
        msg = "Failed to generate access token"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": msg}
        )
        return {"status": False, "uuid": None, "response": response}


@router.get("/", response_class=JSONResponse)
async def authentication_loginpage(request: Request):
    """Login GET route

    Returns:
        _type_: JSONResponse
    """
    try:
        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content={"message": "Authentication Page"}
        )
    except Exception as e:
        raise AppException(e,sys)


@router.post("/", response_class=JSONResponse)
async def login(request: Request, login: Login):
    """Route for User Login

    Returns:
        _type_: Login Response
    """
    try:
        #response = RedirectResponse(url="/application/", status_code=status.HTTP_302_FOUND)
        msg = "Login Successful"
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": msg}
        )
        token_response = await login_for_access_token(response=response, login=login)
        if not token_response["status"]:
            msg = "Incorrect Username and password"
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": False, "message": msg},
            )
            # return RedirectResponse(url="/", status_code=status.HTTP_401_UNAUTHORIZED, headers={"msg": msg})
        # msg = "Login Successfull"
        # response = JSONResponse(status_code=status.HTTP_200_OK, content={"message": msg}, headers={"uuid": "abda"})
        response.headers["uuid"] = token_response["uuid"]

        return response

    except HTTPException:
        msg = "UnKnown Error"
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"status": False, "message": msg},
        )
        # return RedirectResponse(url="/", status_code=status.HTTP_401_UNAUTHORIZED, headers={"msg": msg})
    except Exception as e:
        msg = "User NOT Found"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status": False, "message": msg},
        )
        return response



@router.get("/register", response_class=JSONResponse)
async def authentication_registerpage(request: Request):
    """Route for User Registration

    Returns:
        _type_: Register Response
    """
    try:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Registration Page"}
        )
    except Exception as e:
        raise e


@router.post("/register", response_class=JSONResponse)
async def register_user(request: Request, register: Register):

    """Post request to register a user

    Args:
        request (Request): Request Object
        register (Register):    Name: str
                                username: str
                                email_id: str
                                ph_no: int
                                password1: str
                                password2: str

    Raises:
        e: If the user registration fails

    Returns:
        _type_: Will redirect to the embedding generation route and return the UUID of user
    """
    try:
        name = register.Name
        username = register.username
        password1 = register.password1
        password2 = register.password2
        email_id = register.email_id
        ph_no = register.ph_no

        # Add uuid to the session
        user = User(name, username, email_id, ph_no, password1, password2)
        request.session["uuid"] = user.uuid_
        # Validation of the user input data to check the format of the data
        user_registration = RegisterValidation(user)
        validate_registration = user_registration.validate_registration()
        if not validate_registration["status"]:
            msg = validate_registration["msg"]
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": False, "message": msg},
            )
            return response

        # Save user if the validation is successful
        validation_status = user_registration.authenticate_user_registration()

        msg = "Registration Successful...Please Login to continue"
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": True, "message": validation_status["msg"]},
            headers={"uuid": user.uuid_},
        )
        return response
    except Exception as e:
        raise e
        # msg="Registration failed"
        # response = JSONResponse(
        #     status_code=status.HTTP_404_NOT_FOUND,
        #     content={"status": False, "message": msg})
        #return response 


@router.get("/logout")
async def logout(request: Request):
    """Route for User Logout

    Returns:
        _type_: Logout Response
    """
    try:
        msg = "You have been logged out"
        response =  RedirectResponse(url="/auth/", status_code=status.HTTP_302_FOUND, headers={"msg": msg})
        response.delete_cookie(key="access_token")
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content={"status": True, "message": msg}
        )
        return response
    except Exception as e:
        raise e
