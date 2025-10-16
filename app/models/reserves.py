from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON
from app.database import Base


class Reserve(Base):
    """SQLAlchemy model for Lancer reserves"""
    
    __tablename__ = "reserves"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False, index=True)  # Bonus, Resource, Mech, Tactical
    label = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    
    # Optional JSON fields for flexible data storage
    bonuses = Column(JSON, nullable=True)
    deployables = Column(JSON, nullable=True)
    actions = Column(JSON, nullable=True)
    synergies = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Reserve(id={self.id}, name={self.name}, type={self.type})>"


