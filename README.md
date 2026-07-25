# 🎓 Student Management System

A professional Student Management System built with **FastAPI**, **SQLAlchemy**, **SQLite**, **HTML**, **CSS**, **Jinja2**, and **Python**. The application allows users to securely manage student records with authentication, photo uploads, search, reports, and data export features.

---

# 📖 Project Overview

The Student Management System is a web-based application that helps users efficiently manage student records. It provides secure login, CRUD operations, student profile management, image uploads, search functionality, statistics dashboard, and PDF/Excel export.

---

# ✨ Features

- 🔐 Secure Login & Logout
- 👤 Change Username
- 🔑 Change Password
- ➕ Add Student
- ✏️ Edit Student
- ❌ Delete Student
- 👁 View Student Profile
- 📷 Upload Student Photo
- 🔍 Search Students
- 📊 Dashboard Statistics
- 📈 Course-wise Chart using Chart.js
- 📄 Export Student List to PDF
- 📊 Export Student List to Excel
- ✅ Email Validation
- ✅ Image Validation
- 🔒 Password Hashing using Bcrypt
- 📁 Session-based Authentication

---

# 🛠 Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- HTML5
- CSS3
- Jinja2
- Chart.js
- Pandas
- OpenPyXL
- ReportLab
- Passlib (bcrypt)
- Python-Multipart
- Uvicorn

---

# 📂 Project Structure

```
student_management_system/
│
├── main.py
├── database.py
├── models.py
├── requirements.txt
├── README.md
│
├── static/
│   ├── style.css
│   └── uploads/
│
├── templates/
│   ├── login.html
│   ├── index.html
│   ├── add_student.html
│   ├── edit_student.html
│   ├── view_student.html
│   ├── change_username.html
│   └── change_password.html
│
└── students.db
```

---

# ⚙ Installation

## Clone the Repository

```bash
git clone https://github.com/your-username/student-management-system.git
```

Move to the project folder

```bash
cd student-management-system
```

Install required packages

```bash
pip install -r requirements.txt
```

---

# ▶ Run the Application

```bash
uvicorn main:app --reload
```

Open your browser:

```
http://127.0.0.1:8000
```

---

# 🔑 Default Login Credentials

| Username | Password |
|----------|----------|
| Farmeen | hani021 |

> You can change the username and password after logging in.

---

# 👨‍🎓 Student Information

Each student record contains:

- Name
- Age
- Gender
- Course
- Email
- Photo

---

# 📊 Dashboard

The dashboard displays:

- Total Students
- Male Students
- Female Students
- Course-wise Student Statistics
- Search by Student Name

---

# 📷 Photo Upload

Supported image formats:

- JPG
- JPEG
- PNG
- WEBP

Maximum image size:

- 2 MB

---

# 📄 PDF Export

Generate a professional PDF report containing:

- Student ID
- Name
- Age
- Gender
- Course
- Email

---

# 📊 Excel Export

Export all student records into an Excel spreadsheet (.xlsx).

---

# 🌐 Available Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | / | Dashboard |
| GET | /login | Login Page |
| POST | /login | User Login |
| GET | /logout | Logout |
| GET | /add | Add Student Page |
| POST | /add | Save Student |
| GET | /edit/{id} | Edit Student |
| POST | /update/{id} | Update Student |
| GET | /delete/{id} | Delete Student |
| GET | /student/{id} | View Student Profile |
| GET | /change-username | Change Username |
| POST | /change-username | Update Username |
| GET | /change-password | Change Password |
| POST | /change-password | Update Password |
| GET | /export-pdf | Export PDF |
| GET | /export-excel | Export Excel |

---

# 🔒 Security Features

- Passwords stored using Bcrypt hashing
- Session-based authentication
- Protected routes
- Email format validation
- Image type validation
- Image size validation

---

# 📦 Required Python Packages

```text
fastapi
uvicorn
sqlalchemy
jinja2
python-multipart
passlib[bcrypt]
pandas
openpyxl
reportlab
python-dotenv
```

Install all packages using:

```bash
pip install -r requirements.txt
```

---

# 🚀 Future Improvements

- Multiple User Roles (Admin & Staff)
- Student Attendance Module
- Student Fee Management
- Student ID Card Generation
- Email Notifications
- Dark Mode
- Pagination
- Student Performance Reports
- Backup & Restore Database

---

# 👨‍💻 Author

**Waseem Qureshi**

Student Management System using FastAPI, SQLAlchemy, SQLite, HTML, CSS, and Python.

---

# 📄 License

This project is developed for educational and learning purposes.

# 📂 Project Structure

```
student_management_system/
│
├── main.py                  # Main FastAPI application
├── database.py              # Database connection
├── models.py                # SQLAlchemy models
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
├── students.db              # SQLite database
│
├── static/
│   ├── style.css            # Main stylesheet
│   └── uploads/             # Uploaded student photos
│
├── templates/
│   ├── index.html           # Dashboard
│   ├── login.html           # Login page
│   ├── add_student.html     # Add student form
│   ├── edit_student.html    # Edit student form
│   ├── view_student.html    # Student profile
│   ├── change_username.html # Change username page
│   └── change_password.html # Change password page
│
├── __pycache__/             # Python cache files (auto-generated)
│
└── screenshots/             # Optional project screenshots
    ├── dashboard.png
    ├── login.png
    ├── add_student.png
    └── profile.png
```

### 📁 Folder Description

| File / Folder | Purpose |
|---------------|---------|
| **main.py** | Main FastAPI application containing all routes |
| **database.py** | Creates and manages the SQLite database connection |
| **models.py** | Defines the `Student` and `User` database models |
| **students.db** | SQLite database file storing all records |
| **templates/** | HTML pages rendered using Jinja2 |
| **static/** | Stores CSS files and uploaded student images |
| **uploads/** | Contains uploaded student profile photos |
| **requirements.txt** | List of required Python packages |
| **README.md** | Project documentation |
| **__pycache__/** | Automatically generated Python cache files |
| **screenshots/** | Screenshots for GitHub documentation (optional) |
