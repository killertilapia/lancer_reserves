from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class ReserveType(str, Enum):
    """Reserve type enumeration"""
    BONUS = "Bonus"
    RESOURCE = "Resource"
    MECH = "Mech"
    TACTICAL = "Tactical"


class Bonus(BaseModel):
    """Bonus model for reserves that grant bonuses"""
    id: str
    val: int


class Deployable(BaseModel):
    """Deployable item model"""
    name: str
    type: str
    size: int
    detail: str


class RangeValue(BaseModel):
    """Range value for actions"""
    type: str
    val: int


class DamageValue(BaseModel):
    """Damage value for actions"""
    type: str
    val: str


class Action(BaseModel):
    """Action model for reserves with activatable abilities"""
    name: str
    activation: str
    detail: str
    range: Optional[List[RangeValue]] = None
    damage: Optional[List[DamageValue]] = None


class Synergy(BaseModel):
    """Synergy effect model"""
    locations: List[str]
    detail: str


class ReserveBase(BaseModel):
    """Base reserve schema with common fields"""
    name: str = Field(..., description="Display name of the reserve")
    type: ReserveType = Field(..., description="Type of reserve (Bonus, Resource, Mech, Tactical)")
    label: str = Field(..., description="Category label for the reserve")
    description: str = Field(..., description="Detailed description (HTML-compatible)")
    bonuses: Optional[List[Bonus]] = Field(None, description="Array of bonus effects")
    deployables: Optional[List[Deployable]] = Field(None, description="Array of deployable items")
    actions: Optional[List[Action]] = Field(None, description="Array of activatable actions")
    synergies: Optional[List[Synergy]] = Field(None, description="Array of synergy effects")


class ReserveCreate(ReserveBase):
    """Schema for creating a new reserve"""
    id: str = Field(..., description="Unique identifier (e.g., 'reserve_skill')")


class ReserveUpdate(BaseModel):
    """Schema for updating a reserve (all fields optional)"""
    name: Optional[str] = None
    type: Optional[ReserveType] = None
    label: Optional[str] = None
    description: Optional[str] = None
    bonuses: Optional[List[Bonus]] = None
    deployables: Optional[List[Deployable]] = None
    actions: Optional[List[Action]] = None
    synergies: Optional[List[Synergy]] = None


class ReserveResponse(ReserveBase):
    """Schema for reserve responses"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


