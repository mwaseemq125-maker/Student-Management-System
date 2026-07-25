# 🎓 Student Management System

A full-stack **Student Management System** built using **FastAPI**, **SQLAlchemy**, and **Jinja2 Templates**. It includes authentication, CRUD operations, profile picture uploads with validation, real-time analytics charts, and data export features (Excel & PDF).

---

## 🚀 Features

* **Admin Authentication:** Secure login/logout system using password hashing (`passlib` + `bcrypt`) and cookies.
* **Account Management:** Admins can change their username and password securely.
* **Student CRUD Operations:**
  * Add new students with validation (Age limits, Email regex, Photo size/format).
  * View detailed individual student profiles.
  * Edit and update student information (along with profile picture replacement).
  * Delete student records (automatically cleans up uploaded image files).
* **Search Functionality:** Real-time search filter to find students by name.
* **Dashboard Analytics:** Visual statistics and charts showing total counts, gender distribution, and course-wise breakdown using Chart.js.
* **Data Export:**
  * Export student data to **Excel (`.xlsx`)** using `pandas` and `openpyxl`.
  * Export professional PDF reports using `reportlab`.

---

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, SQLAlchemy
* **Database:** SQLite (managed via SQLAlchemy ORM)
* **Frontend:** HTML5, Tailwind CSS / Jinja2 Templates, Chart.js
* **File Handling & Processing:** Pandas, Openpyxl, ReportLab, Passlib

---

## 📂 Project Structure

```text
student-management-system/
│
├── static/
│   ├── uploads/         # Stores uploaded student profile pictures
│   └── css/             # Stylesheets (if any)
│
├── templates/           # HTML templates (Jinja2)
│   ├── index.html
│   ├── login.html
│   ├── add_student.html
│   ├── edit_student.html
│   └── ...
│
├── database.py          # Database session configuration
├── models.py            # SQLAlchemy models (User & Student)
├── main.py              # FastAPI application routes and logic
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
