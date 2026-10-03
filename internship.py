from pydantic import BaseModel


class InternshipCreate(BaseModel):
    title: str
    company: str
    location: str
    description: str
    skills: str
    category: str = "General"


class InternshipResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    description: str
    skills: str
    category: str | None = "General"

    class Config:
        from_attributes = True