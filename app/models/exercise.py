from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Exercise(Base):
    __tablename__ = "exercises"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String, nullable=False)
    description  = Column(Text)
    category     = Column(String)
    muscle_group = Column(String)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=True)
    gif_url      = Column(String, nullable=True)

    owner = relationship("User", foreign_keys=[user_id])