# backend/routers/courses.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, RootModel
from typing import List, Dict, Any, Optional
import json
import os

router = APIRouter(prefix="/courses", tags=["courses"])

# Путь к файлу с данными курсов
COURSE_DATA_FILE = "course_data.json"

# Модели данных
class Course(BaseModel):
    name: str
    link: str
    description: str
    image: str

class CourseCategory(BaseModel):
    title: str
    courses: List[Course]

class CourseData(RootModel[Dict[str, CourseCategory]]):
    pass

# Функции для работы с файлом данных
def load_course_data():
    """Загружает данные курсов из файла"""
    if os.path.exists(COURSE_DATA_FILE):
        with open(COURSE_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Если файл не существует, создаем пустой
        return {}

def save_course_data(data: dict):
    """Сохраняет данные курсов в файл"""
    with open(COURSE_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Эндпоинты
@router.get("/", response_model=Dict[str, Any])
async def get_all_courses():
    """Получить все курсы"""
    return load_course_data()

@router.get("/{category_id}", response_model=CourseCategory)
async def get_category(category_id: str):
    """Получить категорию курсов по ID"""
    data = load_course_data()
    if category_id not in data:
        raise HTTPException(status_code=404, detail="Category not found")
    return data[category_id]

@router.post("/", response_model=Dict[str, Any])
async def create_category(category: CourseCategory):
    """Создать новую категорию курсов"""
    data = load_course_data()
    # Генерируем новый ID
    new_id = str(max([int(k) for k in data.keys()] + [0]) + 1) if data else "1"
    data[new_id] = category.model_dump()
    save_course_data(data)
    return {"id": new_id, **category.model_dump()}

@router.put("/{category_id}", response_model=CourseCategory)
async def update_category(category_id: str, category: CourseCategory):
    """Обновить категорию курсов"""
    data = load_course_data()
    if category_id not in data:
        raise HTTPException(status_code=404, detail="Category not found")
    data[category_id] = category.model_dump()
    save_course_data(data)
    return category

@router.delete("/{category_id}")
async def delete_category(category_id: str):
    """Удалить категорию курсов"""
    data = load_course_data()
    if category_id not in data:
        raise HTTPException(status_code=404, detail="Category not found")
    del data[category_id]
    save_course_data(data)
    return {"message": "Category deleted successfully"}