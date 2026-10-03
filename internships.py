from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.internship import Internship
from app.schemas.internship import (
    InternshipCreate,
    InternshipResponse
)


router = APIRouter(
    prefix="/internships",
    tags=["Internships"]
)


# GET ALL INTERNSHIPS
@router.get(
    "/",
    response_model=list[InternshipResponse]
)
def get_internships(
    db: Session = Depends(get_db)
):
    return db.query(Internship).all()


# CREATE INTERNSHIP
@router.post(
    "/",
    response_model=InternshipResponse
)
def create_internship(
    internship: InternshipCreate,
    db: Session = Depends(get_db)
):

    new_internship = Internship(
        title=internship.title,
        company=internship.company,
        location=internship.location,
        description=internship.description,
        skills=internship.skills,
        category=internship.category
    )

    db.add(new_internship)
    db.commit()
    db.refresh(new_internship)

    return new_internship


# GET ONE INTERNSHIP
@router.get(
    "/{internship_id}",
    response_model=InternshipResponse
)
def get_internship(
    internship_id: int,
    db: Session = Depends(get_db)
):

    internship = db.query(Internship).filter(
        Internship.id == internship_id
    ).first()

    if not internship:
        raise HTTPException(
            status_code=404,
            detail="Internship not found"
        )

    return internship


# UPDATE INTERNSHIP
@router.put(
    "/{internship_id}",
    response_model=InternshipResponse
)
def update_internship(
    internship_id: int,
    internship: InternshipCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Internship).filter(
        Internship.id == internship_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Internship not found"
        )

    existing.title = internship.title
    existing.company = internship.company
    existing.location = internship.location
    existing.description = internship.description
    existing.skills = internship.skills
    existing.category = internship.category

    db.commit()
    db.refresh(existing)

    return existing


# DELETE INTERNSHIP
@router.delete("/{internship_id}")
def delete_internship(
    internship_id: int,
    db: Session = Depends(get_db)
):

    internship = db.query(Internship).filter(
        Internship.id == internship_id
    ).first()

    if not internship:
        raise HTTPException(
            status_code=404,
            detail="Internship not found"
        )

    db.delete(internship)
    db.commit()

    return {
        "message": "Internship deleted successfully"
    }