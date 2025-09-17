from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="admin")

class StudentSubmission(Base):
    __tablename__ = "student_submissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    institute = Column(String(120), nullable=False)
    batch = Column(String(120), nullable=False)
    course_name = Column(String(120), nullable=False)
    module = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    institute = Column(String(120), nullable=False)
    batch = Column(String(120), nullable=False)
    course_name = Column(String(120), nullable=False)
    module = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    profile_image_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
