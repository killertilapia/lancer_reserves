from typing import List
import strawberry
from strawberry.types import Info
from sqlalchemy.orm import Session

from backend.models.reserves import Reserve
from backend.graphql.schema import ReserveType, ReserveInput, ReserveUpdateInput
from backend.graphql.queries import convert_reserve_to_graphql


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_reserve(self, info: Info, input: ReserveInput) -> ReserveType:
        """Create a new reserve"""
        db: Session = info.context["db"]
        
        # Check if reserve already exists
        existing = db.query(Reserve).filter(Reserve.id == input.id).first()
        if existing:
            raise Exception(f"Reserve with id '{input.id}' already exists")
        
        # Convert input to dict for JSON fields
        bonuses_data = None
        if input.bonuses:
            bonuses_data = [{"id": b.id, "val": b.val} for b in input.bonuses]
        
        deployables_data = None
        if input.deployables:
            deployables_data = [
                {"name": d.name, "type": d.type, "size": d.size, "detail": d.detail}
                for d in input.deployables
            ]
        
        actions_data = None
        if input.actions:
            actions_data = []
            for a in input.actions:
                action_dict = {
                    "name": a.name,
                    "activation": a.activation,
                    "detail": a.detail,
                }
                if a.range:
                    action_dict["range"] = [{"type": r.type, "val": r.val} for r in a.range]
                if a.damage:
                    action_dict["damage"] = [{"type": d.type, "val": d.val} for d in a.damage]
                actions_data.append(action_dict)
        
        synergies_data = None
        if input.synergies:
            synergies_data = [
                {"locations": s.locations, "detail": s.detail}
                for s in input.synergies
            ]
        
        # Create reserve
        db_reserve = Reserve(
            id=input.id,
            name=input.name,
            type=input.type.value,
            label=input.label,
            description=input.description,
            bonuses=bonuses_data,
            deployables=deployables_data,
            actions=actions_data,
            synergies=synergies_data,
        )
        
        db.add(db_reserve)
        db.commit()
        db.refresh(db_reserve)
        
        return convert_reserve_to_graphql(db_reserve)
    
    @strawberry.mutation
    def update_reserve(self, info: Info, id: str, input: ReserveUpdateInput) -> ReserveType:
        """Update an existing reserve"""
        db: Session = info.context["db"]
        
        db_reserve = db.query(Reserve).filter(Reserve.id == id).first()
        if not db_reserve:
            raise Exception(f"Reserve with id '{id}' not found")
        
        # Update fields if provided
        if input.name is not None:
            db_reserve.name = input.name
        if input.type is not None:
            db_reserve.type = input.type.value
        if input.label is not None:
            db_reserve.label = input.label
        if input.description is not None:
            db_reserve.description = input.description
        
        if input.bonuses is not None:
            db_reserve.bonuses = [{"id": b.id, "val": b.val} for b in input.bonuses]
        
        if input.deployables is not None:
            db_reserve.deployables = [
                {"name": d.name, "type": d.type, "size": d.size, "detail": d.detail}
                for d in input.deployables
            ]
        
        if input.actions is not None:
            actions_data = []
            for a in input.actions:
                action_dict = {
                    "name": a.name,
                    "activation": a.activation,
                    "detail": a.detail,
                }
                if a.range:
                    action_dict["range"] = [{"type": r.type, "val": r.val} for r in a.range]
                if a.damage:
                    action_dict["damage"] = [{"type": d.type, "val": d.val} for d in a.damage]
                actions_data.append(action_dict)
            db_reserve.actions = actions_data
        
        if input.synergies is not None:
            db_reserve.synergies = [
                {"locations": s.locations, "detail": s.detail}
                for s in input.synergies
            ]
        
        db.commit()
        db.refresh(db_reserve)
        
        return convert_reserve_to_graphql(db_reserve)
    
    @strawberry.mutation
    def delete_reserve(self, info: Info, id: str) -> bool:
        """Delete a reserve"""
        db: Session = info.context["db"]
        
        db_reserve = db.query(Reserve).filter(Reserve.id == id).first()
        if not db_reserve:
            raise Exception(f"Reserve with id '{id}' not found")
        
        db.delete(db_reserve)
        db.commit()
        
        return True
    
    @strawberry.mutation
    def import_reserves(self, info: Info, reserves: List[ReserveInput]) -> List[ReserveType]:
        """Bulk import reserves"""
        db: Session = info.context["db"]
        imported = []
        
        for reserve_input in reserves:
            # Skip if already exists
            existing = db.query(Reserve).filter(Reserve.id == reserve_input.id).first()
            if existing:
                continue
            
            # Convert input to dict for JSON fields
            bonuses_data = None
            if reserve_input.bonuses:
                bonuses_data = [{"id": b.id, "val": b.val} for b in reserve_input.bonuses]
            
            deployables_data = None
            if reserve_input.deployables:
                deployables_data = [
                    {"name": d.name, "type": d.type, "size": d.size, "detail": d.detail}
                    for d in reserve_input.deployables
                ]
            
            actions_data = None
            if reserve_input.actions:
                actions_data = []
                for a in reserve_input.actions:
                    action_dict = {
                        "name": a.name,
                        "activation": a.activation,
                        "detail": a.detail,
                    }
                    if a.range:
                        action_dict["range"] = [{"type": r.type, "val": r.val} for r in a.range]
                    if a.damage:
                        action_dict["damage"] = [{"type": d.type, "val": d.val} for d in a.damage]
                    actions_data.append(action_dict)
            
            synergies_data = None
            if reserve_input.synergies:
                synergies_data = [
                    {"locations": s.locations, "detail": s.detail}
                    for s in reserve_input.synergies
                ]
            
            db_reserve = Reserve(
                id=reserve_input.id,
                name=reserve_input.name,
                type=reserve_input.type.value,
                label=reserve_input.label,
                description=reserve_input.description,
                bonuses=bonuses_data,
                deployables=deployables_data,
                actions=actions_data,
                synergies=synergies_data,
            )
            
            db.add(db_reserve)
            imported.append(db_reserve)
        
        db.commit()
        
        for reserve in imported:
            db.refresh(reserve)
        
        return [convert_reserve_to_graphql(r) for r in imported]


