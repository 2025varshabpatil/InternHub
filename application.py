from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    internship_id: int
    student_name: str
    email: str
    phone: str = ""


class ApplicationResponse(BaseModel):
    id: int
    internship_id: int
    student_name: str
    email: str
    phone: str | None
    status: str

    class Config:
        from_attributes = True