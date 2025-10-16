from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
import json
import random

from backend.database import get_db
from backend.models.reserves import Reserve
from backend.schemas.reserves import ReserveCreate, ReserveUpdate, ReserveResponse, ReserveType

router = APIRouter()


@router.post("/", response_model=ReserveResponse, status_code=201)
def create_reserve(reserve: ReserveCreate, db: Session = Depends(get_db)):
    """Create a new reserve"""
    # Check if reserve with this ID already exists
    existing_reserve = db.query(Reserve).filter(Reserve.id == reserve.id).first()
    if existing_reserve:
        raise HTTPException(status_code=400, detail=f"Reserve with id '{reserve.id}' already exists")
    
    db_reserve = Reserve(
        id=reserve.id,
        name=reserve.name,
        type=reserve.type.value,
        label=reserve.label,
        description=reserve.description,
        bonuses=[b.model_dump() for b in reserve.bonuses] if reserve.bonuses else None,
        deployables=[d.model_dump() for d in reserve.deployables] if reserve.deployables else None,
        actions=[a.model_dump() for a in reserve.actions] if reserve.actions else None,
        synergies=[s.model_dump() for s in reserve.synergies] if reserve.synergies else None,
    )
    
    db.add(db_reserve)
    db.commit()
    db.refresh(db_reserve)
    return db_reserve


@router.get("/", response_model=List[ReserveResponse])
def list_reserves(
    type: Optional[ReserveType] = Query(None, description="Filter by reserve type"),
    label: Optional[str] = Query(None, description="Filter by label"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """List all reserves with optional filtering and pagination"""
    query = db.query(Reserve)
    
    if type:
        query = query.filter(Reserve.type == type.value)
    
    if label:
        query = query.filter(func.lower(Reserve.label).contains(label.lower()))
    
    reserves = query.offset(skip).limit(limit).all()
    return reserves


@router.get("/type/{reserve_type}", response_model=List[ReserveResponse])
def get_reserves_by_type(
    reserve_type: ReserveType,
    db: Session = Depends(get_db)
):
    """Get all reserves of a specific type"""
    reserves = db.query(Reserve).filter(Reserve.type == reserve_type.value).all()
    return reserves


@router.get("/random", response_model=List[ReserveResponse])
def get_random_reserves(
    count: int = Query(1, ge=1, le=50, description="Number of random reserves to return"),
    type: Optional[ReserveType] = Query(None, description="Filter by reserve type before random selection"),
    db: Session = Depends(get_db)
):
    """Get random reserves with optional type filtering"""
    query = db.query(Reserve)
    
    if type:
        query = query.filter(Reserve.type == type.value)
    
    all_reserves = query.all()
    
    if not all_reserves:
        raise HTTPException(status_code=404, detail="No reserves found matching the criteria")
    
    # Select random reserves without replacement
    selected_count = min(count, len(all_reserves))
    random_reserves = random.sample(all_reserves, selected_count)
    
    return random_reserves


@router.get("/{reserve_id}", response_model=ReserveResponse)
def get_reserve(reserve_id: str, db: Session = Depends(get_db)):
    """Get a specific reserve by ID"""
    reserve = db.query(Reserve).filter(Reserve.id == reserve_id).first()
    if not reserve:
        raise HTTPException(status_code=404, detail=f"Reserve with id '{reserve_id}' not found")
    return reserve


@router.put("/{reserve_id}", response_model=ReserveResponse)
def update_reserve(reserve_id: str, reserve_update: ReserveUpdate, db: Session = Depends(get_db)):
    """Update a reserve"""
    db_reserve = db.query(Reserve).filter(Reserve.id == reserve_id).first()
    if not db_reserve:
        raise HTTPException(status_code=404, detail=f"Reserve with id '{reserve_id}' not found")
    
    # Update only provided fields
    update_data = reserve_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if field in ["bonuses", "deployables", "actions", "synergies"] and value is not None:
            # Convert Pydantic models to dicts for JSON storage
            setattr(db_reserve, field, [item.model_dump() if hasattr(item, 'model_dump') else item for item in value])
        elif field == "type" and value is not None:
            setattr(db_reserve, field, value.value)
        else:
            setattr(db_reserve, field, value)
    
    db.commit()
    db.refresh(db_reserve)
    return db_reserve


@router.delete("/{reserve_id}", status_code=204)
def delete_reserve(reserve_id: str, db: Session = Depends(get_db)):
    """Delete a reserve"""
    db_reserve = db.query(Reserve).filter(Reserve.id == reserve_id).first()
    if not db_reserve:
        raise HTTPException(status_code=404, detail=f"Reserve with id '{reserve_id}' not found")
    
    db.delete(db_reserve)
    db.commit()
    return None


@router.post("/import", response_model=List[ReserveResponse])
def import_reserves(reserves_data: List[ReserveCreate], db: Session = Depends(get_db)):
    """Bulk import reserves from JSON data"""
    imported_reserves = []
    
    for reserve_data in reserves_data:
        # Check if reserve already exists
        existing_reserve = db.query(Reserve).filter(Reserve.id == reserve_data.id).first()
        if existing_reserve:
            continue  # Skip existing reserves
        
        db_reserve = Reserve(
            id=reserve_data.id,
            name=reserve_data.name,
            type=reserve_data.type.value,
            label=reserve_data.label,
            description=reserve_data.description,
            bonuses=[b.model_dump() for b in reserve_data.bonuses] if reserve_data.bonuses else None,
            deployables=[d.model_dump() for d in reserve_data.deployables] if reserve_data.deployables else None,
            actions=[a.model_dump() for a in reserve_data.actions] if reserve_data.actions else None,
            synergies=[s.model_dump() for s in reserve_data.synergies] if reserve_data.synergies else None,
        )
        
        db.add(db_reserve)
        imported_reserves.append(db_reserve)
    
    db.commit()
    
    for reserve in imported_reserves:
        db.refresh(reserve)
    
    return imported_reserves

