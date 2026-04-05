from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from models.database import get_db
from models.models import Student
from models.schemas import StudentCreate, StudentResponse, StudentUpdate

# Initialize router
router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=StudentResponse)

#Create a new student record.
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    db_student = db.query(Student).filter(Student.reg_no == student.reg_no).first()
    if db_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration number already exists"
        )
    
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/", response_model=List[StudentResponse])

#Retrieve list of students with optional searc
def get_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Student)
    
    if search:
        query = query.filter(
            or_(
                Student.name.ilike(f"%{search}%"),
                Student.reg_no.ilike(f"%{search}%"),
                Student.department.ilike(f"%{search}%")
            )
        )
    
    students = query.offset(skip).limit(limit).all()
    return students

@router.get("/{student_id}", response_model=StudentResponse)

#Retrieve a specific student by ID.
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student

@router.get("/reg/{reg_no}", response_model=StudentResponse)

#Retrieve a specific student by registration number.
def get_student_by_reg_no(
    reg_no: str,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.reg_no == reg_no).first()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student

@router.put("/{student_id}", response_model=StudentResponse)

# Update an existing student record.
def update_student(
    student_id: int,
    student_update: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    update_data = student_update.dict(exclude_unset=True)
    
    #Check for registration number conflicts
    if "reg_no" in update_data:
        existing_student = db.query(Student).filter(
            Student.reg_no == update_data["reg_no"],
            Student.id != student_id
        ).first()
        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration number already exists"
            )
    
    #Apply updates
    for field, value in update_data.items():
        setattr(student, field, value)
    
    db.commit()
    db.refresh(student)
    return student

@router.delete("/{student_id}")

#Delete a student record.
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}
