from typing import List, Optional
from datetime import datetime
import strawberry
from enum import Enum


@strawberry.enum
class ReserveTypeEnum(Enum):
    """GraphQL enum for reserve types"""
    BONUS = "Bonus"
    RESOURCE = "Resource"
    MECH = "Mech"
    TACTICAL = "Tactical"


@strawberry.type
class BonusType:
    """GraphQL type for bonuses"""
    id: str
    val: int


@strawberry.type
class DeployableType:
    """GraphQL type for deployables"""
    name: str
    type: str
    size: int
    detail: str


@strawberry.type
class RangeValueType:
    """GraphQL type for range values"""
    type: str
    val: int


@strawberry.type
class DamageValueType:
    """GraphQL type for damage values"""
    type: str
    val: str


@strawberry.type
class ActionType:
    """GraphQL type for actions"""
    name: str
    activation: str
    detail: str
    range: Optional[List[RangeValueType]] = None
    damage: Optional[List[DamageValueType]] = None


@strawberry.type
class SynergyType:
    """GraphQL type for synergies"""
    locations: List[str]
    detail: str


@strawberry.type
class ReserveType:
    """GraphQL type for Reserve"""
    id: str
    name: str
    type: ReserveTypeEnum
    label: str
    description: str
    bonuses: Optional[List[BonusType]] = None
    deployables: Optional[List[DeployableType]] = None
    actions: Optional[List[ActionType]] = None
    synergies: Optional[List[SynergyType]] = None
    created_at: datetime
    updated_at: datetime


@strawberry.input
class BonusInput:
    """GraphQL input for bonuses"""
    id: str
    val: int


@strawberry.input
class DeployableInput:
    """GraphQL input for deployables"""
    name: str
    type: str
    size: int
    detail: str


@strawberry.input
class RangeValueInput:
    """GraphQL input for range values"""
    type: str
    val: int


@strawberry.input
class DamageValueInput:
    """GraphQL input for damage values"""
    type: str
    val: str


@strawberry.input
class ActionInput:
    """GraphQL input for actions"""
    name: str
    activation: str
    detail: str
    range: Optional[List[RangeValueInput]] = None
    damage: Optional[List[DamageValueInput]] = None


@strawberry.input
class SynergyInput:
    """GraphQL input for synergies"""
    locations: List[str]
    detail: str


@strawberry.input
class ReserveInput:
    """GraphQL input for creating/updating reserves"""
    id: str
    name: str
    type: ReserveTypeEnum
    label: str
    description: str
    bonuses: Optional[List[BonusInput]] = None
    deployables: Optional[List[DeployableInput]] = None
    actions: Optional[List[ActionInput]] = None
    synergies: Optional[List[SynergyInput]] = None


@strawberry.input
class ReserveUpdateInput:
    """GraphQL input for updating reserves (all fields optional except id)"""
    name: Optional[str] = None
    type: Optional[ReserveTypeEnum] = None
    label: Optional[str] = None
    description: Optional[str] = None
    bonuses: Optional[List[BonusInput]] = None
    deployables: Optional[List[DeployableInput]] = None
    actions: Optional[List[ActionInput]] = None
    synergies: Optional[List[SynergyInput]] = None


