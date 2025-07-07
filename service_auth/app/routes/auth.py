from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schema.user import UserOut
from app.schema.auth import UserSignup, Token, RefreshTokenRequest
from app.db.database import get_db
from app.services.auth_service import signup as signup_service
from app.services.auth_service import signin as signin_service
from app.services.auth_service import get_refresh_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserOut, status_code=status.HTTP_200_OK)
async def signup(user: UserSignup, db: Session = Depends(get_db)):
    """
    Register a new user and return their account information.

    **Request Body (application/json):**
    - `email` (str): User's email address.
    - `password` (str): User's password.
    - `name` (str): Full name of the user.

    **Example:**
    ```json
    {
        "email": "newuser@example.com",
        "password": "12345678",
        "name": "John Doe"
    }
    ```

    **Response (200 OK):**
    Returns the created user information:
    ```json
    {
        "id": 1,
        "email": "newuser@example.com",
        "name": "John Doe",
        "created_at": "2025-07-06T18:00:00Z"
    }
    ```

    - `id`: Unique user ID.
    - `email`: Registered email address.
    - `name`: Full name of the user.
    - `created_at`: Account creation timestamp.
    """
    return await signup_service(user, db)

@router.post("/signin", response_model=Token, status_code=status.HTTP_200_OK)
async def signin(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user and return access and refresh tokens.

    **Request Body (`application/x-www-form-urlencoded`):**
    - `username` (str): User's email address.
    - `password` (str): User's password.

    **Example:**
    ```
    username=user@example.com
    password=12345678
    ```

    **Response (200 OK):**
    Returns a token object:
    ```json
    {
        "access_token": "JWT_TOKEN",
        "refresh_token": "JWT_REFRESH_TOKEN",
        "token_type": "Bearer",
        "expires_in": 1800
    }
    ```

    - `access_token`: JWT for accessing protected routes.
    - `refresh_token`: JWT for generating new tokens.
    - `token_type`: Type of the token (always "Bearer").
    - `expires_in`: Expiration time in seconds (default: 30 minutes).
    """
    return await signin_service(user_credentials, db)

@router.post("/refresh", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Generate a new access token using a valid refresh token.

    **Request Body (`application/json`):**
    - `refresh_token` (str): Valid refresh token.

    **Example:**
    ```json
    {
        "refresh_token": "JWT_REFRESH_TOKEN"
    }
    ```

    **Response (200 OK):**
    Returns a token object:
    ```json
    {
        "access_token": "NEW_JWT_TOKEN",
        "refresh_token": "JWT_REFRESH_TOKEN",
        "token_type": "Bearer",
        "expires_in": 1800
    }
    ```

    - `access_token`: New JWT for accessing protected routes.
    - `refresh_token`: Original or new refresh token.
    - `token_type`: Type of the token (always "Bearer").
    - `expires_in`: Expiration time in seconds.
    """
    return await get_refresh_token(request.refresh_token, db)