# backend/routers/courses.py
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.course import CourseCategoryCreate, CourseCategoryUpdate, CourseCategoryInDB, CourseCreate, CourseUpdate, CourseInDB
from models.course import CourseCategory, Course
from database import get_db

router = APIRouter(prefix="/courses", tags=["courses"])

# --- Операции с категориями ---

@router.get("/categories/", response_model=List[CourseCategoryInDB])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(CourseCategory).offset(skip).limit(limit).all()
    return categories

@router.post("/categories/", response_model=CourseCategoryInDB, status_code=status.HTTP_201_CREATED)
def create_category(category: CourseCategoryCreate, db: Session = Depends(get_db)):
    db_category = CourseCategory(title=category.title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/categories/{category_id}", response_model=CourseCategoryInDB)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(CourseCategory).filter(CourseCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.put("/categories/{category_id}", response_model=CourseCategoryInDB)
def update_category(category_id: int, category: CourseCategoryUpdate, db: Session = Depends(get_db)):
    db_category = db.query(CourseCategory).filter(CourseCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category.model_dump().items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(CourseCategory).filter(CourseCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return

# --- Операции с курсами ---

@router.get("/", response_model=List[CourseInDB])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses

@router.post("/", response_model=CourseInDB, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, category_id: int, db: Session = Depends(get_db)):
    # Проверяем, существует ли категория
    db_category = db.query(CourseCategory).filter(CourseCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
        
    db_course = Course(
        name=course.name,
        link=course.link,
        description=course.description,
        image=course.image,
        category_id=category_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/{course_id}", response_model=CourseInDB)
def read_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@router.put("/{course_id}", response_model=CourseInDB)
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in course.model_dump().items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return

# --- Получение всех категорий с курсами (для фронтенда) ---
@router.get("/with-courses/", response_model=List[CourseCategoryInDB])
def read_categories_with_courses(db: Session = Depends(get_db)):
    """Получить все категории вместе с их курсами"""
    categories = db.query(CourseCategory).all()
    return categories