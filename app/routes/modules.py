from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Module
from ..schemas import ModuleOut, ModuleUpdate

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("", response_model=List[ModuleOut])
def list_modules(db: Session = Depends(get_db)):
    return db.query(Module).order_by(Module.id).all()


@router.patch("/{module_id}", response_model=ModuleOut)
def rename_module(
    module_id: int,
    payload: ModuleUpdate,
    db: Session = Depends(get_db),
):
    module = db.query(Module).filter(Module.id == module_id).first()
    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    module.name = payload.name
    db.commit()
    db.refresh(module)
    return module
