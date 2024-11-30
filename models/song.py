from models.base import Base
from sqlalchemy import Column, TEXT, VARCHAR, LargeBinary

class SongModel(Base):
    __tablename__ = "songs"

    id = Column(TEXT, primary_key=True)
    song_name = Column(VARCHAR(100))
    artist = Column(VARCHAR(100))
    hex_color = Column(VARCHAR(6))
    thumbnail_url = Column(TEXT)
    song_url = Column(TEXT)