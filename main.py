from crud import create_student,get_students
from fastapi import FastAPI, Depends,HTTPException
from schemas import StudentCreate, StudentResponse
from sqlalchemy.orm import Session

from database import SessionLocal,Base,engine
from models import Student as StudentDB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}


@app.get("/about")
def about():
    return {
        "name": "Madhu",
        "course": "FastAPI"
    }


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id
    }


@app.get("/search")
def search(name: str):
    return {
        "search_name": name
    }




@app.post("/students",response_model=StudentResponse)
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student=create_student(db,student)
    return new_student 
    

@app.get("/students",response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    

    return students
@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
        status_code=404,
        detail="Student not found"
        ) 
    return student
@app.put("/students/{student_id}",response_model=StudentResponse)
def update_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    existing_student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if existing_student is None:
        raise HTTPException(
        status_code=404,
        detail="Student not found"
        ) 

    existing_student.name = student.name
    existing_student.age = student.age
    existing_student.course = student.course

    db.commit()
    db.refresh(existing_student)

    return existing_student
        


@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    existing_student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if existing_student is None:
        raise HTTPException(

        status_code=404,
        detail="Student not found"
        ) 

    db.delete(existing_student)
    db.commit()

    return {
        "message": "Student deleted successfully",
        "student_id": student_id
    }
