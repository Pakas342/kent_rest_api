from fastapi import FastAPI, HTTPException, Response
from sqlmodel import select

from database import create_db_structure, SessionDep
from models import Student, StudentBase

app = FastAPI()

create_db_structure()


@app.get('/')
def index():
    return "Please access the url /docs for getting the documentation on this APIs methods"


@app.get('/students', response_model=list[Student])
def get_students(db: SessionDep, offset: int = 0, limit: int = 10) -> [Student]:
    statement = select(Student).offset(offset).limit(limit)
    students = db.exec(statement).all()
    return students


@app.post('/students', response_model=Student)
def create_student(db: SessionDep, student: StudentBase) -> Student:
    new_student = Student.model_validate(student)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@app.get('/students/{student_id}', response_model=Student)
def get_single_student(db: SessionDep, student_id: int):
    try:
        student = db.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail='Student with given id not found')
        return student
    except Exception as e:
        raise e


@app.delete('/students/{student_id}')
def delete_student(db: SessionDep, student_id: int):
    try:
        student = db.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail='Student with given id not found')
        db.delete(student)
        db.commit()
        return Response(status_code=204)
    except Exception as e:
        raise e


@app.put('/students/{student_id}', response_model=Student)
def update_student(db: SessionDep, student_id: int, student: StudentBase):
    try:
        student_to_update = db.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail='Student with given id not found')
        student_to_update.sqlmodel_update(student)
        db.add(student_to_update)
        db.commit()
        db.refresh(student_to_update)
        return student_to_update
    except Exception as e:
        raise e
