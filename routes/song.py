from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session, joinedload
from middleware.auth_middleware import auth_middleware
from models.song import SongModel
from pydantic_schema.favorite_song_schema import FavoriteSongSchema
from models.favorite import FavoriteSongsModel
import cloudinary
import cloudinary.uploader
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Configuration       
cloudinary.config( 
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

@router.post("/upload", status_code=201)
def upload_song(song: UploadFile = File(...), 
                thumbnail: UploadFile = File(...), 
                song_name: str = Form(...), 
                artist: str = Form(...), 
                hex_color: str = Form(...), 
                db: Session = Depends(get_db),
                auth_dic = Depends(auth_middleware)):
    
    try:
        song_id = str(uuid.uuid4())
        song_url = cloudinary.uploader.upload(
                    song.file, 
                    public_id=song_id, 
                    resource_type="auto", 
                    folder=f"songs/{song_id}"
                )
        thumbnail_url =  cloudinary.uploader.upload(
                    thumbnail.file, 
                    public_id=song_id, 
                    resource_type="image", 
                    folder=f"songs/{song_id}"
        )

        song_db = SongModel(
                id = song_id,
                song_name = song_name,
                artist = artist,
                hex_color = hex_color,
                thumbnail_url = thumbnail_url['url'],
                song_url = song_url['url']
        )

        db.add(song_db)
        db.commit()
        db.refresh(song_db)

        return song_db
    except Exception as e:
        print(e)
        raise HTTPException(500, f"Failed to upload files to cloud storage: {str(e)}")

@router.get('/list')
def get_songs(db: Session = Depends(get_db), auth_dic = Depends(auth_middleware)):

    songs = db.query(SongModel).all()
    return songs


@router.post('/favorite')
def favorite_song(fav_song: FavoriteSongSchema, db: Session = Depends(get_db), auth_dic = Depends(auth_middleware)):
    user_id = auth_dic.get("id")
    song_id = fav_song.id
    # check if user already has favorite song
    favorite_song = db.query(FavoriteSongsModel).filter(FavoriteSongsModel.user_id == user_id, FavoriteSongsModel.song_id == song_id).first()
    if favorite_song:
        db.delete(favorite_song)
        db.commit()
        return {'message': False}
    else:
        id = str(uuid.uuid4())
        favorite_song = FavoriteSongsModel(
            id = id,
            user_id = user_id,
            song_id = song_id
        )
        db.add(favorite_song)
        db.commit()
        return {'message': True}

@router.get('/list/favorites')
def get_favorite_songs(db: Session = Depends(get_db), auth_dic = Depends(auth_middleware)):
    user_id = auth_dic.get("id")
    favorite_songs = db.query(FavoriteSongsModel).filter(FavoriteSongsModel.user_id == user_id).options(joinedload(FavoriteSongsModel.song)).all()
    return favorite_songs