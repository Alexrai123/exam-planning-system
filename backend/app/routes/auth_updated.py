from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Any

from ..core.security import create_access_token, verify_password
from ..core.config import settings
from ..db.base import get_db
from ..models.user import User, UserRole
from ..models.grupa import Grupa
from ..schemas.auth import Token, UserCreate, UserLogin
from ..schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)) -> Any:
    """
    Register a new user
    """
    # Check if user with this email already exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )
    
    # Create new user
    from ..core.security import get_password_hash
    user = User(
        name=user_in.name,
        email=user_in.email,
        password=get_password_hash(user_in.password),
        role=user_in.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # Check if user with this email exists
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Check if password is correct
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Dependency to get current user
def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Get the current user from the token
    """
    from jose import jwt, JWTError
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user

# Dependency to check if user is professor
def is_professor(current_user: User = Depends(get_current_user)) -> User:
    """
    Check if user is a professor
    """
    if current_user.role != UserRole.PROFESSOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user

# Dependency to check if user is secretariat
def is_secretariat(current_user: User = Depends(get_current_user)) -> User:
    """
    Check if user is from secretariat
    """
    if current_user.role.upper() != UserRole.SECRETARIAT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user

# Dependency to check if user is a group leader
def is_group_leader(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> User:
    """
    Check if user is a group leader
    """
    if current_user.role.upper() != UserRole.STUDENT:
        # If not a student, they can't be a group leader
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can be group leaders",
        )
    
    # Check if the user is a leader of any group
    group = db.query(Grupa).filter(Grupa.leader_id == current_user.id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a group leader",
        )
    
    return current_user

# Dependency to check if user is a student
def is_student(current_user: User = Depends(get_current_user)) -> User:
    """
    Check if user is a student
    """
    if current_user.role.upper() != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can access this resource",
        )
    
    return current_user
