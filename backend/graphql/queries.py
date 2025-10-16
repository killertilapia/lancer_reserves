from typing import List, Optional
import strawberry
from strawberry.types import Info
from sqlalchemy.orm import Session
from sqlalchemy import func
import random

from backend.models.reserves import Reserve
from backend.graphql.schema import ReserveType, ReserveTypeEnum, BonusType, DeployableType, ActionType, SynergyType, RangeValueType, DamageValueType


def convert_reserve_to_graphql(db_reserve: Reserve) -> ReserveType:
    """Convert SQLAlchemy Reserve model to GraphQL ReserveType"""
    
    # Convert bonuses
    bonuses = None
    if db_reserve.bonuses:
        bonuses = [BonusType(**b) for b in db_reserve.bonuses]
    
    # Convert deployables
    deployables = None
    if db_reserve.deployables:
        deployables = [DeployableType(**d) for d in db_reserve.deployables]
    
    # Convert actions
    actions = None
    if db_reserve.actions:
        actions = []
        for a in db_reserve.actions:
            action_dict = dict(a)
            if action_dict.get('range'):
                action_dict['range'] = [RangeValueType(**r) for r in action_dict['range']]
            if action_dict.get('damage'):
                action_dict['damage'] = [DamageValueType(**d) for d in action_dict['damage']]
            actions.append(ActionType(**action_dict))
    
    # Convert synergies
    synergies = None
    if db_reserve.synergies:
        synergies = [SynergyType(**s) for s in db_reserve.synergies]
    
    return ReserveType(
        id=db_reserve.id,
        name=db_reserve.name,
        type=ReserveTypeEnum[db_reserve.type.upper()] if db_reserve.type.upper() in ReserveTypeEnum.__members__ else ReserveTypeEnum.BONUS,
        label=db_reserve.label,
        description=db_reserve.description,
        bonuses=bonuses,
        deployables=deployables,
        actions=actions,
        synergies=synergies,
        created_at=db_reserve.created_at,
        updated_at=db_reserve.updated_at,
    )


@strawberry.type
class Query:
    @strawberry.field
    def reserves(
        self,
        info: Info,
        type: Optional[ReserveTypeEnum] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ReserveType]:
        """Get all reserves with optional filtering"""
        db: Session = info.context["db"]
        query = db.query(Reserve)
        
        if type:
            query = query.filter(Reserve.type == type.value)
        
        db_reserves = query.offset(skip).limit(limit).all()
        return [convert_reserve_to_graphql(r) for r in db_reserves]
    
    @strawberry.field
    def reserve(self, info: Info, id: str) -> Optional[ReserveType]:
        """Get a specific reserve by ID"""
        db: Session = info.context["db"]
        db_reserve = db.query(Reserve).filter(Reserve.id == id).first()
        
        if not db_reserve:
            return None
        
        return convert_reserve_to_graphql(db_reserve)
    
    @strawberry.field
    def reserves_by_label(self, info: Info, label: str) -> List[ReserveType]:
        """Get reserves by label (case-insensitive search)"""
        db: Session = info.context["db"]
        db_reserves = db.query(Reserve).filter(
            func.lower(Reserve.label).contains(label.lower())
        ).all()
        
        return [convert_reserve_to_graphql(r) for r in db_reserves]
    
    @strawberry.field
    def random_reserves(
        self,
        info: Info,
        count: int = 1,
        type: Optional[ReserveTypeEnum] = None
    ) -> List[ReserveType]:
        """Get random reserves with optional type filtering"""
        db: Session = info.context["db"]
        query = db.query(Reserve)
        
        if type:
            query = query.filter(Reserve.type == type.value)
        
        all_reserves = query.all()
        
        if not all_reserves:
            return []
        
        # Select random reserves without replacement
        selected_count = min(count, len(all_reserves))
        random_reserves = random.sample(all_reserves, selected_count)
        
        return [convert_reserve_to_graphql(r) for r in random_reserves]

