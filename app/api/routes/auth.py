from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, UserOut, Token
from app.core.security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/register",
    response_model=UserOut,
    status_code=201,
    summary="Register a new user",
    response_description="The newly created user",
    responses={400: {"description": "Email or username already taken"}},
)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.

    - **username** — must be unique
    - **email** — must be a valid email and unique
    - **password** — will be hashed before storage, never stored in plain text
    """
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post(
    "/login",
    response_model=Token,
    summary="Log in and get a JWT token",
    response_description="A JWT access token valid for 30 minutes",
    responses={401: {"description": "Invalid username or password"}},
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Log in with username and password.

    Returns a **Bearer token** — include it in the `Authorization` header
    of all subsequent requests:
    Authorization: Bearer <your_token>
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get(
    "/me",
    response_model=UserOut,
    summary="Get current user",
    response_description="The currently authenticated user",
)
def get_me(current_user: User = Depends(get_current_user)):
    """Returns the profile of the currently logged in user."""
    return current_user