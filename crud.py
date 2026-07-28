from sqlalchemy.orm import Session
from models import Student


def create_student(db: Session, student):
    new_student = Student(
        name=student.name,
        age=student.age,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student
def get_students(db: Session):
    return db.query(Student).all()