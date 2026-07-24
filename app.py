import os
import re
import shutil
import io
from uuid import uuid4

from fastapi import FastAPI, Request, Form, HTTPException, Query, File, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import pandas as pd
from passlib.context import CryptContext

from database import engine, Base, SessionLocal
from models import Student, User

app = FastAPI(title="Student Management System")

# Password Hashing Setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Static & Uploads Directory Setup
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Validation Constants
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB Limit


# Helper Function: Email Regex Validation
def is_valid_email(email: str) -> bool:
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(email_regex, email) is not None


# Helper Function: Default Admin Creation
def create_default_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "Farmeen").first()
    if not admin:
        hashed_pwd = pwd_context.hash("hani021")
        default_user = User(username="Farmeen", hashed_password=hashed_pwd)
        db.add(default_user)
        db.commit()
    db.close()

create_default_admin()


# Helper Function: Get Current Logged-in User
def get_current_user(request: Request):
    return request.cookies.get("user_session")


# ---------------- LOGIN & LOGOUT ROUTES ----------------

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if get_current_user(request):
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(request=request, name="login.html")


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    if not user or not pwd_context.verify(password, user.hashed_password):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Invalid Username or Password!"}
        )

    response = RedirectResponse("/", status_code=303)
    response.set_cookie(key="user_session", value=username, httponly=True)
    return response


@app.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie(key="user_session")
    return response


# ---------------- CHANGE USERNAME & PASSWORD ROUTES ----------------

@app.get("/change-username", response_class=HTMLResponse)
def change_username_page(request: Request):
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(request=request, name="change_username.html", context={"username": current_user})


@app.post("/change-username")
def change_username(request: Request, new_username: str = Form(...)):
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    existing_user = db.query(User).filter(User.username == new_username).first()
    if existing_user:
        db.close()
        return templates.TemplateResponse(
            request=request,
            name="change_username.html",
            context={"username": current_user, "error": "Username already taken!"}
        )

    user = db.query(User).filter(User.username == current_user).first()
    if user:
        user.username = new_username
        db.commit()
    db.close()

    response = RedirectResponse("/", status_code=303)
    response.set_cookie(key="user_session", value=new_username, httponly=True)
    return response


@app.get("/change-password", response_class=HTMLResponse)
def change_password_page(request: Request):
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(request=request, name="change_password.html", context={"username": current_user})


@app.post("/change-password")
def change_password(request: Request, old_password: str = Form(...), new_password: str = Form(...)):
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    user = db.query(User).filter(User.username == current_user).first()

    if not user or not pwd_context.verify(old_password, user.hashed_password):
        db.close()
        return templates.TemplateResponse(
            request=request,
            name="change_password.html",
            context={"username": current_user, "error": "Incorrect old password!"}
        )

    user.hashed_password = pwd_context.hash(new_password)
    db.commit()
    db.close()

    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie(key="user_session")
    return response


# ---------------- DASHBOARD & CRUD ROUTES ----------------

from sqlalchemy import func

@app.get("/", response_class=HTMLResponse)
def home(request: Request, search: str = Query(default="")):
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    
    if search:
        students = db.query(Student).filter(Student.name.contains(search)).all()
    else:
        students = db.query(Student).all()

    total_students = db.query(Student).count()
    male_students = db.query(Student).filter(Student.gender == "Male").count()
    female_students = db.query(Student).filter(Student.gender == "Female").count()

    # Course-wise statistics calculate karein
    course_data = db.query(Student.course, func.count(Student.id)).group_by(Student.course).all()
    
    # Chart labels aur counts pass karne ke liye prepare karein
    course_labels = [c[0] for c in course_data] if course_data else []
    course_counts = [c[1] for c in course_data] if course_data else []

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "students": students,
            "search": search,
            "total_students": total_students,
            "male_students": male_students,
            "female_students": female_students,
            "course_labels": course_labels,  # Chart.js Labels
            "course_counts": course_counts,  # Chart.js Counts
            "username": current_user
        },
    )

@app.get("/add", response_class=HTMLResponse)
def add_student_page(request: Request):
    if not get_current_user(request):
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(request=request, name="add_student.html")


@app.post("/add")
async def add_student(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    course: str = Form(...),
    email: str = Form(...),
    photo: UploadFile = File(None)
):
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse("/login", status_code=303)

    # 1. Validation: Age Limit
    if age < 15 or age > 60:
        return templates.TemplateResponse(
            request=request, name="add_student.html", context={"error": "Age must be between 15 and 60!"}
        )

    # 2. Validation: Email Format
    if not is_valid_email(email):
        return templates.TemplateResponse(
            request=request, name="add_student.html", context={"error": "Please enter a valid email address!"}
        )

    photo_path = None
    if photo and photo.filename:
        extension = os.path.splitext(photo.filename)[1].lower()
        if extension not in ALLOWED_EXTENSIONS:
            return templates.TemplateResponse(
                request=request, name="add_student.html", context={"error": "Only JPG, PNG, and WEBP formats allowed!"}
            )

        contents = await photo.read()
        if len(contents) > MAX_FILE_SIZE:
            return templates.TemplateResponse(
                request=request, name="add_student.html", context={"error": "Image size must be less than 2MB!"}
            )

        await photo.seek(0)
        unique_filename = f"{uuid4().hex}{extension}"
        photo_path = f"{UPLOAD_DIR}/{unique_filename}"
        with open(photo_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

    db = SessionLocal()
    student = Student(
        name=name.strip(),
        age=age,
        gender=gender,
        course=course.strip(),
        email=email.strip().lower(),
        photo=photo_path
    )
    db.add(student)
    db.commit()
    db.close()

    return RedirectResponse("/", status_code=303)


@app.get("/edit/{student_id}", response_class=HTMLResponse)
def edit_student_page(student_id: int, request: Request):
    if not get_current_user(request):
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    student = db.query(Student).filter(Student.id == student_id).first()
    db.close()

    if student is None:
        raise HTTPException(status_code=404, detail="Student Not Found")

    return templates.TemplateResponse(request=request, name="edit_student.html", context={"student": student})


@app.post("/update/{student_id}")
async def update_student(
    student_id: int,
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    course: str = Form(...),
    email: str = Form(...),
    photo: UploadFile = File(None)
):
    if not get_current_user(request):
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        db.close()
        raise HTTPException(status_code=404, detail="Student Not Found")

    if age < 15 or age > 60:
        db.close()
        return templates.TemplateResponse(
            request=request, name="edit_student.html", context={"student": student, "error": "Age must be between 15 and 60!"}
        )

    if not is_valid_email(email):
        db.close()
        return templates.TemplateResponse(
            request=request, name="edit_student.html", context={"student": student, "error": "Please enter a valid email address!"}
        )

    student.name = name.strip()
    student.age = age
    student.gender = gender
    student.course = course.strip()
    student.email = email.strip().lower()

    if photo and photo.filename:
        extension = os.path.splitext(photo.filename)[1].lower()
        if extension not in ALLOWED_EXTENSIONS:
            db.close()
            return templates.TemplateResponse(
                request=request, name="edit_student.html", context={"student": student, "error": "Only JPG, PNG, and WEBP formats allowed!"}
            )

        contents = await photo.read()
        if len(contents) > MAX_FILE_SIZE:
            db.close()
            return templates.TemplateResponse(
                request=request, name="edit_student.html", context={"student": student, "error": "Image size must be less than 2MB!"}
            )

        await photo.seek(0)
        if student.photo and os.path.exists(student.photo):
            try:
                os.remove(student.photo)
            except Exception:
                pass

        unique_filename = f"{uuid4().hex}{extension}"
        photo_path = f"{UPLOAD_DIR}/{unique_filename}"
        with open(photo_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        student.photo = photo_path

    db.commit()
    db.close()
    return RedirectResponse("/", status_code=303)


@app.get("/delete/{student_id}")
def delete_student(student_id: int, request: Request):
    if not get_current_user(request):
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    student = db.query(Student).filter(Student.id == student_id).first()

    if student:
        if student.photo and os.path.exists(student.photo):
            try:
                os.remove(student.photo)
            except Exception:
                pass
        db.delete(student)
        db.commit()

    db.close()
    return RedirectResponse("/", status_code=303)


@app.get("/export-excel")
def export_students_to_excel(request: Request):
    if not get_current_user(request):
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    students = db.query(Student).all()
    db.close()

    student_data = [{"ID": s.id, "Name": s.name, "Age": s.age, "Gender": s.gender, "Course": s.course, "Email": s.email} for s in students]

    df = pd.DataFrame(student_data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Students')
    
    output.seek(0)
    headers = {'Content-Disposition': 'attachment; filename="students_list.xlsx"'}
    return StreamingResponse(output, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@app.get("/student/{student_id}", response_class=HTMLResponse)
def view_student_profile(student_id: int, request: Request):
    if not get_current_user(request):
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    student = db.query(Student).filter(Student.id == student_id).first()
    db.close()

    if student is None:
        raise HTTPException(status_code=404, detail="Student Not Found")

    return templates.TemplateResponse(request=request, name="view_student.html", context={"student": student})

from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

# ---------------- PDF EXPORT ROUTES ----------------

@app.get("/export-pdf")
def export_students_pdf(request: Request):
    if not get_current_user(request):
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    students = db.query(Student).all()
    db.close()

    # Create PDF Buffer
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor("#1e3a8a"),
        alignment=1, # Center
        spaceAfter=15
    )

    # Title
    elements.append(Paragraph("🎓 Student Management System - Report", title_style))
    elements.append(Spacer(1, 10))

    # Table Header & Data
    data = [["ID", "Name", "Age", "Gender", "Course", "Email"]]
    for student in students:
        data.append([
            str(student.id),
            student.name,
            str(student.age),
            student.gender,
            student.course,
            student.email
        ])

    # Styling the Table
    table = Table(data, colWidths=[30, 110, 40, 60, 110, 180])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2563eb")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)

    headers = {'Content-Disposition': 'attachment; filename="students_report.pdf"'}
    return StreamingResponse(buffer, headers=headers, media_type='application/pdf')