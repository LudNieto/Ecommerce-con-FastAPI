from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schema.user import UserOut, UserUpdate
from app.core.security import get_current_user
from app.services.user_service import get_user_by_id, update_user, deactivate_user


router = APIRouter(prefix="/user", tags=["User"])

@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_my_user(current_user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get the authenticated user's profile information.

    **Headers:**
    - `Authorization`: Bearer access token.

    **Example:**
    ```
    Authorization: Bearer JWT_ACCESS_TOKEN
    ```

    **Response (200 OK):**
    Returns the authenticated user's information:
    ```json
    {
        "id": 1,
        "email": "user@example.com",
        "name": "Jane Doe",
        "created_at": "2025-07-06T18:00:00Z"
    }
    ```

    - `id`: Unique user ID.
    - `email`: Registered email address.
    - `name`: Full name of the user.
    - `is_active`: Indicates if the account is active (true/false).
    - `created_at`: Date and time when the account was created.
    """
    return await get_user_by_id(current_user_id, db)

@router.put("/update", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_my_user(
    user_update: UserUpdate, 
    current_user_id: int = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Update the authenticated user's profile information.
    
    **Headers:**
    - `Authorization`: Bearer access token.
    
    **Example:**
    ```
    Authorization: Bearer JWT_ACCESS_TOKEN
    ```
    
    **Request Body (JSON):**
    You can send one or more of the following fields:
    ```json
    {
        "name": "Jane Doe",
        "email": "user@example.co",
        "password": "newsecurepassword",
        "is_active": true
    }
    ```
    
    - name: (optional) New full name of the user.
    
    - email: (optional) New email address.
    
    - password: (optional) New password.
    
    - is_active: (optional) Change the active status (true/false).
    
    **Response (200 OK):**
    Returns the updated user information:
    
    ```json
    {
        "id": 1,
        "email": "user@example.co",
        "name": "Jane Doe",
        "is_active": true,
        "created_at": "2025-07-06T18:00:00Z"
    }
    ```

    - id: Unique user ID.
    
    - email: Updated email address.
    
    - full_name: Updated full name.

    - is_active: Indicates if the account is active (true/false).
    
    - created_at: Account creation date and time.
    """
    return await update_user(current_user_id, user_update, db)

@router.delete("/deactivate", response_model=UserOut, status_code=status.HTTP_200_OK)
async def deactivate_my_user(
    current_user_id: int = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Deactivate the authenticated user's account (soft delete).

    This endpoint allows the authenticated user to deactivate their account. Typically, this sets the `is_active` field to `false` without deleting the data from the database.

    **Headers:**
    - `Authorization`: Bearer access token.

    **Example:**
    ```
    Authorization: Bearer JWT_ACCESS_TOKEN
    ```

    **Request Body:**
    No body is required for this request.

    **Response (200 OK):**
    Returns the deactivated user information:

    ```json
    {
        "id": 1,
        "email": "user@example.com",
        "name": "Jane Doe",
        "is_active": false,
        "created_at": "2025-07-06T18:00:00Z"
    }
    ```

    - id: Unique user ID.

    - email: Registered email address.

    - name: Full name of the user.

    - is_active: Indicates if the account is active (false after deactivation).

    - created_at: Account creation date and time.
    """
    return await deactivate_user(current_user_id, db)