# backend/models/course.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class CourseCategory(Base):
    __tablename__ = "course_categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)

    # Отношение один-ко-многим с Course
    courses = relationship("Course", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CourseCategory(id={self.id}, title='{self.title}')>"

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    link = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    image = Column(String, nullable=True) # Может быть пустым
    
    # Внешний ключ
    category_id = Column(Integer, ForeignKey("course_categories.id"), nullable=False)

    # Отношение многие-к-одному с CourseCategory
    category = relationship("CourseCategory", back_populates="courses")

    def __repr__(self):
        return f"<Course(id={self.id}, name='{self.name}', category_id={self.category_id})>"