from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import Token, UserLogin
from app.crud.user import get_user_by_email
from app.utils import verify_password, create_access_token
from jose import JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils import decode_access_token
from typing import Optional

router = APIRouter()
oauth2_scheme = HTTPBearer()

# Hardcoded demo user
DEMO_USER = {
    "email": "admin@demo.com",
    "password": "admin123",
    "full_name": "Demo Admin"
}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Check demo user
    if form_data.username == DEMO_USER["email"] and form_data.password == DEMO_USER["password"]:
        access_token = create_access_token(data={"sub": DEMO_USER["email"]})
        return {"access_token": access_token, "token_type": "bearer"}
    
    # Check database user
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# ✅ Yeh function missing tha
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    token_data = decode_access_token(token)  # utils se import karna hai
    
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user_by_email(db, token_data.email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user