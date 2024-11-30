from fastapi import HTTPException, APIRouter, Depends,Header
from database import get_db
from models.user import UserModel
from middleware.auth_middleware import auth_middleware
from pydantic_schema.user_schema import UserCreate, UserLogin
from sqlalchemy.orm import Session, joinedload
import uuid
import bcrypt
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.post("/signup", status_code=201)
def signup(user: UserCreate, db: Session=Depends(get_db)):

    user_db = db.query(UserModel).filter(UserModel.email == user.email).first()

    if user_db:
        raise HTTPException(400, "User already exists")
    
    # Hash the password before storing
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    user_db = UserModel(
        id=str(uuid.uuid4()), 
        name=user.name, 
        email=user.email, 
        password=hashed_password
    )

    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@router.post("/login")
def login(user:UserLogin, db: Session = Depends(get_db)):
    user_db = db.query(UserModel).filter(UserModel.email == user.email).first()

    if not user_db :
        raise HTTPException(400, "User does not exist")
    
    is_match = bcrypt.checkpw(user.password.encode('utf-8'), user_db.password)

    if not is_match:
        raise HTTPException(400, "Invalid credentials")
    
    token = jwt.encode({"id": user_db.id}, os.getenv("PASSWORD_KEY"), algorithm="HS256")

    return {"token": token, "user": user_db}

@router.get("/")
def current_user(db: Session = Depends(get_db), user_dic = Depends(auth_middleware)):
    user_id = user_dic.get("id")
    user = db.query(UserModel).filter(UserModel.id == user_id).options(joinedload(UserModel.favorite_songs)).first()

    if not user:
        raise HTTPException(404, "User not found")
    
    return user

    pass