import os, io
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
import jwt
from PIL import Image

from database import SessionLocal, Base, engine
from models import User, StudentSubmission, Student

JWT_SECRET = os.getenv("JWT_SECRET", "change_this_secret")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/opt/dipti/uploads")
os.makedirs(os.path.join(UPLOAD_DIR, "students"), exist_ok=True)

auth_scheme = HTTPBearer(auto_error=False)
student_scheme = HTTPBearer(auto_error=False)

app = FastAPI(title="DIPTI Backend API v2")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

Base.metadata.create_all(bind=engine)

def ensure_admin():
    db = SessionLocal()
    try:
        if not db.query(User).filter_by(username="admin").first():
            db.add(User(username="admin", password_hash=bcrypt.hash("admin123"), role="admin"))
            db.commit()
    finally:
        db.close()
ensure_admin()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LoginIn(BaseModel):
    username: str
    password: str

class TokenOut(BaseModel):
    token: str

class StudentIn(BaseModel):
    name: str
    institute: str
    batch: str
    course_name: str
    module: str
    email: EmailStr

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/api/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=payload.username).first()
    if not user or not bcrypt.verify(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = jwt.encode({"sub": user.username, "role": user.role, "kind": "admin"}, JWT_SECRET, algorithm="HS256")
    return {"token": token}

def require_admin(creds: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if not creds:
        raise HTTPException(status_code=401, detail="Missing auth")
    try:
        decoded = jwt.decode(creds.credentials, JWT_SECRET, algorithms=["HS256"])
        if decoded.get("kind") != "admin":
            raise Exception("not admin")
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/students")
def create_student(payload: StudentIn, db: Session = Depends(get_db), user=Depends(require_admin)):
    rec = StudentSubmission(**payload.model_dump())
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return {"id": rec.id, "status": "created"}

# Student registration & auth
@app.post("/api/students/register")
async def student_register(
    name: str = Form(...),
    institute: str = Form(...),
    batch: str = Form(...),
    course_name: str = Form(...),
    module: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if photo.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(400, detail="Only JPEG/PNG allowed")
    if db.query(Student).filter_by(email=str(email)).first():
        raise HTTPException(400, detail="Email already registered")

    raw = await photo.read()
    try:
        im = Image.open(io.BytesIO(raw)).convert("RGB")
    except Exception:
        raise HTTPException(400, detail="Invalid image")
    target = (256, 256)
    im_ratio = im.width / im.height
    tgt_ratio = target[0] / target[1]
    if im_ratio > tgt_ratio:
        new_height = im.height
        new_width = int(new_height * tgt_ratio)
    else:
        new_width = im.width
        new_height = int(new_width / tgt_ratio)
    left = (im.width - new_width)//2
    top = (im.height - new_height)//2
    im_cropped = im.crop((left, top, left+new_width, top+new_height))
    im_resized = im_cropped.resize(target)

    student = Student(
        name=name, institute=institute, batch=batch,
        course_name=course_name, module=module,
        email=str(email), password_hash=bcrypt.hash(password)
    )
    db.add(student); db.commit(); db.refresh(student)

    out_dir = os.path.join(UPLOAD_DIR, "students")
    os.makedirs(out_dir, exist_ok=True)
    img_path = os.path.join(out_dir, f"{student.id}.jpg")
    im_resized.save(img_path, format="JPEG", quality=90)
    student.profile_image_path = f"students/{student.id}.jpg"
    db.commit()

    return {"id": student.id, "status": "registered"}

class StudentLoginIn(BaseModel):
    email: EmailStr
    password: str

@app.post("/api/student/login", response_model=TokenOut)
def student_login(payload: StudentLoginIn, db: Session = Depends(get_db)):
    s = db.query(Student).filter_by(email=str(payload.email)).first()
    if not s or not bcrypt.verify(payload.password, s.password_hash):
        raise HTTPException(401, detail="Invalid email or password")
    token = jwt.encode({"sub": s.email, "sid": s.id, "kind": "student"}, JWT_SECRET, algorithm="HS256")
    return {"token": token}

def require_student(creds: HTTPAuthorizationCredentials = Depends(student_scheme)):
    if not creds:
        raise HTTPException(status_code=401, detail="Missing auth")
    try:
        decoded = jwt.decode(creds.credentials, JWT_SECRET, algorithms=["HS256"])
        if decoded.get("kind") != "student":
            raise Exception("not student")
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/api/student/me")
def student_me(auth=Depends(require_student), db: Session = Depends(get_db)):
    s = db.query(Student).get(auth["sid"])
    if not s:
        raise HTTPException(404, detail="Not found")
    photo_url = f"/uploads/{s.profile_image_path}" if s.profile_image_path else None
    return {
        "id": s.id,
        "name": s.name,
        "email": s.email,
        "institute": s.institute,
        "batch": s.batch,
        "course_name": s.course_name,
        "module": s.module,
        "photo_url": photo_url
    }
