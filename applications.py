from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.application import Application
from app.models.internship import Internship
from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse
)


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


# CREATE APPLICATION
@router.post(
    "/",
    response_model=ApplicationResponse
)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):

    internship = db.query(Internship).filter(
        Internship.id == application.internship_id
    ).first()

    if not internship:
        raise HTTPException(
            status_code=404,
            detail="Internship not found"
        )

    new_application = Application(
        internship_id=application.internship_id,
        student_name=application.student_name,
        email=application.email,
        phone=application.phone,
        status="Applied"
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


# GET ALL APPLICATIONS
@router.get(
    "/",
    response_model=list[ApplicationResponse]
)
def get_applications(
    db: Session = Depends(get_db)
):

    return db.query(Application).all()


# GET ONE APPLICATION
@router.get(
    "/{application_id}",
    response_model=ApplicationResponse
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db)
):

    application = db.query(Application).filter(
        Application.id == application_id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application