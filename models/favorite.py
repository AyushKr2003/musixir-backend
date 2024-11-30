from models.base import Base
from sqlalchemy import Column, TEXT, ForeignKey
from sqlalchemy.orm import relationship

class FavoriteSongsModel(Base):
    __tablename__ = "favorite_songs"
    id = Column(TEXT, primary_key=True)
    user_id = Column(TEXT, ForeignKey("users.id"))
    song_id = Column(TEXT, ForeignKey("songs.id"))

    song = relationship("SongModel")
    user = relationship("UserModel", back_populates="favorite_songs")