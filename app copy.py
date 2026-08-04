
import json
import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow the frontend JavaScript to call these APIs

# ==============================================================
# Persistent storage setup
# ==============================================================
# All student data lives in this single JSON file, next to app.py.
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.json")


def load_students():
    """Load the student list from students.json.
    If the file doesn't exist yet (first run), create it with an
    empty list and return that.
    """
    if not os.path.exists(DATA_FILE):
        save_students([])
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, OSError):
        # If the file is corrupted for any reason, start fresh
        # rather than crashing the whole server.
        return []


def save_students(students):
    """Write the current student list to students.json."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=2)


def get_next_id(students):
    """Generate a new unique id.
    Using max(existing ids) + 1 instead of len(students) + 1
    means ids stay unique even after students are deleted.
    """
    if not students:
        return 1
    return max(s["id"] for s in students) + 1


def find_student(students, student_id):
    """Return the student dict with the given id, or None."""
    for s in students:
        if s["id"] == student_id:
            return s
    return None


# ==============================================================
# GPA calculation
# ==============================================================
def marks_to_gpa_points(mark):
    """Convert a single subject's marks (0-100) into GPA points."""
    if mark >= 90:
        return 4.0
    elif mark >= 80:
        return 3.5
    elif mark >= 70:
        return 3.0
    elif mark >= 60:
        return 2.5
    else:
        return 0.0  # Fail


def calculate_gpa(grades):
    """Average GPA points across all subjects for a student."""
    if not grades:
        return 0.0

    total = sum(marks_to_gpa_points(mark) for mark in grades.values())
    return round(total / len(grades), 2)


def calculate_attendance_percent(attendance):
    """Return attendance percentage, e.g. 85.0 for 85%."""
    present = attendance.get("present", 0)
    absent = attendance.get("absent", 0)
    total = present + absent
    if total == 0:
        return 0.0
    return round((present / total) * 100, 2)


def student_with_computed_fields(student):
    """Return a copy of the student with gpa/attendance_percent added,
    without changing what's actually stored on disk."""
    copy = dict(student)
    copy["gpa"] = calculate_gpa(student.get("grades", {}))
    copy["attendance_percent"] = calculate_attendance_percent(
        student.get("attendance", {"present": 0, "absent": 0})
    )
    return copy


# ==============================================================
# Basic input validation helpers
# ==============================================================
def validation_error(message):
    return jsonify({"error": message}), 400


def not_found_error(message="Student not found"):
    return jsonify({"error": message}), 404


# ==============================================================
# ROUTES
# ==============================================================

@app.route("/")
def home():
    """Serve the single-page dashboard."""
    return send_file("index.html")


# ---------------- STUDENTS ----------------

@app.route("/students", methods=["GET"])
def get_students():
    """Return every student, with gpa and attendance_percent included."""
    students = load_students()
    data = [student_with_computed_fields(s) for s in students]
    return jsonify(data)


@app.route("/students", methods=["POST"])
def add_student():
    """Add a new student."""
    data = request.get_json(silent=True)
    if not data:
        return validation_error("No data received")

    name = (data.get("name") or "").strip()
    course = (data.get("course") or "").strip()
    email = (data.get("email") or "").strip()
    age = data.get("age")

   if not name:
    return validation_error("Name is required")

   if not course:
    return validation_error("Course is required")

# Email validation
   if not email:
    return validation_error("Email is required")

   if "@" not in email or "." not in email:
    return validation_error("Invalid email format")


   # Age validation
   if age is None or str(age).strip() == "":
    return validation_error("Age is required")

try:
    age = int(age)
except (TypeError, ValueError):
    return validation_error("Age must be a number")


if age < 1 or age > 100:
    return validation_error("Age must be between 1 and 100")

    students = load_students()

    new_student = {
        "id": get_next_id(students),
        "name": name,
        "age": age,
        "email": email,
        "course": course,
        "grades": {},
        "attendance": {"present": 0, "absent": 0},
    }

    students.append(new_student)
    save_students(students)

    return jsonify({
        "message": "Student added successfully",
        "student": student_with_computed_fields(new_student),
    }), 201


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """Update basic info (name, age, email, course) for a student."""
    data = request.get_json(silent=True)
    if not data:
        return validation_error("No data received")

    students = load_students()
    student = find_student(students, student_id)

    if student is None:
        return not_found_error()

    # Only update the fields that were actually sent, and only
    # allow editing safe fields (not id/grades/attendance directly).
    for field in ("name", "age", "email", "course"):
        if field in data:
            student[field] = data[field]

    save_students(students)

    return jsonify({
        "message": "Student updated successfully",
        "student": student_with_computed_fields(student),
    })


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """Delete a student by id."""
    students = load_students()
    student = find_student(students, student_id)

    if student is None:
        return not_found_error()

    students = [s for s in students if s["id"] != student_id]
    save_students(students)

    return jsonify({"message": "Student deleted successfully"})


# ---------------- GRADES ----------------

@app.route("/grades", methods=["POST"])
def add_grade():
    """Add or update a grade for a student's subject."""
    data = request.get_json(silent=True)
    if not data:
        return validation_error("No data received")

    try:
        student_id = int(data.get("student_id"))
    except (TypeError, ValueError):
        return validation_error("student_id must be a number")

    subject = (data.get("subject") or "").strip()
    if not subject:
        return validation_error("Subject is required")

    try:
        marks = float(data.get("marks"))
    except (TypeError, ValueError):
        return validation_error("Marks must be a number")

    if marks < 0 or marks > 100:
        return validation_error("Marks must be between 0 and 100")

    students = load_students()
    student = find_student(students, student_id)

    if student is None:
        return not_found_error()

    student["grades"][subject] = marks
    save_students(students)

    return jsonify({
        "message": "Grade added successfully",
        "student": student_with_computed_fields(student),
    })


# ---------------- ATTENDANCE ----------------

@app.route("/attendance", methods=["POST"])
def mark_attendance():
    """Increment present or absent count for a student."""
    data = request.get_json(silent=True)
    if not data:
        return validation_error("No data received")

    try:
        student_id = int(data.get("student_id"))
    except (TypeError, ValueError):
        return validation_error("student_id must be a number")

    status = data.get("status")
    if status not in ("present", "absent"):
        return validation_error("status must be 'present' or 'absent'")

    students = load_students()
    student = find_student(students, student_id)

    if student is None:
        return not_found_error()

    student["attendance"][status] += 1
    save_students(students)

    return jsonify({
        "message": "Attendance updated successfully",
        "student": student_with_computed_fields(student),
    })


# ---------------- STATISTICS ----------------

@app.route("/statistics", methods=["GET"])
def statistics():
    """Return overall statistics across all students."""
    students = load_students()

    if not students:
        return jsonify({
            "total_students": 0,
            "average_gpa": 0,
            "highest_gpa": 0,
            "lowest_gpa": 0,
            "average_attendance": 0,
        })

    gpas = [calculate_gpa(s.get("grades", {})) for s in students]
    attendance_percents = [
        calculate_attendance_percent(s.get("attendance", {"present": 0, "absent": 0}))
        for s in students
    ]

    return jsonify({
        "total_students": len(students),
        "average_gpa": round(sum(gpas) / len(gpas), 2),
        "highest_gpa": max(gpas),
        "lowest_gpa": min(gpas),
        "average_attendance": round(sum(attendance_percents) / len(attendance_percents), 2),
    })


# ---------------- REPORT ----------------

@app.route("/report/<int:student_id>", methods=["GET"])
def report(student_id):
    """Return a full report for a single student."""
    students = load_students()
    student = find_student(students, student_id)

    if student is None:
        return not_found_error()

    return jsonify(student_with_computed_fields(student))


@app.route("/reports", methods=["GET"])
def all_reports():
    """Return a full report (grades, gpa, attendance) for every student.
    This powers the 'Total Report' view, which is the same idea as
    /report/<id> but combined for the whole class at once.
    """
    students = load_students()
    return jsonify([student_with_computed_fields(s) for s in students])


# ==============================================================
# RUN SERVER
# ==============================================================

if __name__ == "__main__":
    # Make sure students.json exists before the server starts.
    if not os.path.exists(DATA_FILE):
        save_students([])

    app.run(host="0.0.0.0", port=5000, debug=True)