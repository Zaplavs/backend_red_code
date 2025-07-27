# backend/schemas/course.py
from pydantic import BaseModel
from typing import List, Optional

# Базовые схемы
class CourseBase(BaseModel):
    name: str
    link: str
    description: str
    image: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CourseInDB(CourseBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True

class CourseCategoryBase(BaseModel):
    title: str

class CourseCategoryCreate(CourseCategoryBase):
    pass

class CourseCategoryUpdate(CourseCategoryBase):
    pass

class CourseCategoryInDB(CourseCategoryBase):
    id: int
    courses: List[CourseInDB] = []

    class Config:
        from_attributes = True