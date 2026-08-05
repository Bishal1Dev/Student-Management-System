# Student Management System

A web-based Student Management System built using **HTML, CSS, JavaScript, and Python Flask**.

This project allows users to manage student records, track grades, calculate GPA, monitor attendance, and generate student reports through a simple web interface.

---

# Features

## Student Management

- Add new students
- View all students
- Update student information
- Delete student records
- Automatically generate unique student IDs


## Grade Management

- Add subject grades
- Update student marks
- Delete individual subject grades
- Automatically calculate GPA
- Support multiple subjects


## Attendance Management

- Mark student attendance
- Track present and absent days
- Prevent double-marking attendance on the same day
- Automatically calculate attendance percentage


## Reports & Statistics

- Generate individual student reports
- Generate complete class reports
- Display:
  - Total students
  - Average GPA
  - Highest GPA
  - Lowest GPA
  - Average attendance
  - Grade distribution across GPA bands

## Search, Sort & Pagination

- Search students by name or course (`GET /students?q=`)
- Sort by name, GPA, or attendance (`?sort=&order=`)
- Paginate results (`?page=&per_page=`)

## Data Safety & Security

- Atomic, thread-safe writes to `students.json`
- Corrupt files are backed up instead of silently wiped
- Duplicate email detection on add/update
- Per-day attendance tracking (prevents double-marking same day)
- Delete individual subject grades
- Optional API key auth (set `API_KEY` env var)
- Restrict CORS origins (via `ALLOWED_ORIGINS` env var)
- Request body size limit


---

# Technologies Used

## Frontend

### HTML
Used to create the structure of the web application.

### CSS
Used for styling and improving the user interface.

### JavaScript
Used for:
- Frontend interaction
- Sending API requests
- Updating webpage data dynamically


## Backend

### Python Flask

Used for:
- Creating the web server
- Handling API requests
- Processing student data
- Performing GPA and attendance calculations


## Database

### JSON Storage

Student information is stored in:

```
students.json
```

JSON was used because it is lightweight and simple for small-scale applications.

---

# Project Structure

```
Python-Project/

│
├── .venv/
│   └── Python virtual environment
│
├── app.py
│   └── Flask backend application
│
├── index.html
│   └── Frontend user interface
│
├── requirements.txt
│   └── Python dependencies
│
└── students.json
    └── Student database
```

---

# System Architecture

```
             USER
              |
              |
        index.html
     HTML + CSS + JavaScript
              |
              |
        Flask API Server
             app.py
              |
              |
       Python Processing
              |
              |
        students.json
```

---

# Installation Guide

## 1. Clone the Repository

```bash
git clone https://github.com/Bishal1Dev/Student-Management-System.git
```

Navigate into the project folder:

```bash
cd Student-Management-System
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

---

## 3. Activate Virtual Environment

### Windows

```powershell
.venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start the Flask server:

```bash
python app.py
```

The server will start at:

```
http://127.0.0.1:5000
```

Open the link in your browser.

---

# Configuration (Environment Variables)

The server behavior can be customized with environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Interface to bind the server to |
| `PORT` | `5000` | Port to run the server on |
| `FLASK_DEBUG` | `0` | Set to `1` to enable debug mode |
| `ALLOWED_ORIGINS` | `http://127.0.0.1:5000,http://localhost:5000` | Comma-separated list of allowed CORS origins |
| `API_KEY` | *(empty)* | If set, all API requests must include the `X-API-Key` header |

Example (PowerShell):

```powershell
$env:PORT = "8080"
$env:FLASK_DEBUG = "1"
$env:API_KEY = "my-secret-key"
python app.py
```

Example (bash):

```bash
PORT=8080 FLASK_DEBUG=1 API_KEY=my-secret-key python app.py
```

When `API_KEY` is set, send it with every request:

```
X-API-Key: my-secret-key
```

---

# API Endpoints

## Student Management

### Get All Students

```
GET /students
```

Returns all student records.

Optional query parameters:
- `?q=<text>` — search by name or course
- `?sort=name|gpa|attendance&order=asc|desc` — sort results


### Get Single Student

```
GET /students/<student_id>
```

Returns one student record.


### Add Student

```
POST /students
```

Creates a new student.


### Update Student

```
PUT /students/<student_id>
```

Updates student information.


### Delete Student

```
DELETE /students/<student_id>
```

Deletes a student.


---

## Grade Management

### Add Grade

```
POST /grades
```

Adds or updates student marks.


### Delete Grade

```
DELETE /grades
```

Deletes a single subject grade for a student.

Request body:

```json
{
  "student_id": 1,
  "subject": "Python"
}
```


---

## Attendance Management

### Mark Attendance

```
POST /attendance
```

Updates attendance records.


---

## Reports

### Individual Report

```
GET /report/<student_id>
```

Returns complete student information.


### Complete Report

```
GET /reports
```

Returns reports for all students.


---

# GPA Calculation

The system converts marks into GPA points:

| Marks | GPA |
|------|-----|
| 90 - 100 | 4.0 |
| 80 - 89 | 3.5 |
| 70 - 79 | 3.0 |
| 60 - 69 | 2.5 |
| Below 60 | 0.0 |

The final GPA is calculated by averaging all subject GPA points.

---

# Attendance Calculation

Attendance percentage is calculated using:

```
Attendance Percentage =
(Present Days / Total Days) × 100
```

Example:

```
Present: 90
Absent: 10

Attendance = 90%
```

---

# Data Validation

The system includes validation for:

- Empty student information
- Invalid marks
- Invalid student IDs
- Incorrect API requests

This prevents incorrect data from being stored.

---

# Future Improvements

Possible improvements:

- MySQL/PostgreSQL database integration
- User authentication system
- Admin dashboard
- PDF report generation
- Cloud deployment
- Role-based access control
- Mobile application support

---

# Learning Outcomes

Through this project, the following concepts were implemented:

- Flask web development
- REST API creation
- Frontend-backend communication
- JSON data handling
- CRUD operations
- Data validation
- GPA calculation logic
- Attendance management


---

# Author

**Bishal Lamichhane**

Student Management System Project
