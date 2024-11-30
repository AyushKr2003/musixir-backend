from models.base import Base
from sqlalchemy import Column, TEXT, VARCHAR, LargeBinary
from sqlalchemy.orm import relationship

# SQLAlchemy Model for database
class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(TEXT, primary_key=True)
    name = Column(VARCHAR(100))
    email = Column(VARCHAR(100))
    password = Column(LargeBinary)

    favorite_songs = relationship("FavoriteSongsModel", back_populates="user")