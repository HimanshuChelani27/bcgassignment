
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.roles import Role
from sqlalchemy import Boolean

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    is_verified = Column(Boolean, default=False)
    name= Column(String(100), unique=False, index=True, nullable=False)
    role = relationship("Role", backref="users")


