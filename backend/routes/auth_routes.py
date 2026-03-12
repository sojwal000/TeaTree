"""
Authentication routes: register, login, profile
"""
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from backend.database import get_database
from backend.models import UserRegister, UserLogin, UserResponse, Token
from backend.auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister):
    """Create a new user account."""
    db = get_database()

    # Check if email already exists
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_doc = {
        "user_id": str(uuid.uuid4()),
        "name": user.name,
        "email": user.email,
        "password_hash": get_password_hash(user.password),
        "created_at": datetime.utcnow(),
    }
    await db.users.insert_one(user_doc)

    return UserResponse(
        user_id=user_doc["user_id"],
        name=user_doc["name"],
        email=user_doc["email"],
        created_at=user_doc["created_at"],
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Authenticate user and return JWT token."""
    db = get_database()
    user = await db.users.find_one({"email": credentials.email})

    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(data={"sub": user["user_id"]})
    return Token(access_token=access_token)


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile."""
    return UserResponse(
        user_id=current_user["user_id"],
        name=current_user["name"],
        email=current_user["email"],
        created_at=current_user["created_at"],
    )


@router.put("/profile", response_model=UserResponse)
async def update_profile(name: str, current_user: dict = Depends(get_current_user)):
    """Update user profile name."""
    db = get_database()
    await db.users.update_one(
        {"user_id": current_user["user_id"]},
        {"$set": {"name": name}}
    )
    current_user["name"] = name
    return UserResponse(
        user_id=current_user["user_id"],
        name=current_user["name"],
        email=current_user["email"],
        created_at=current_user["created_at"],
    )
