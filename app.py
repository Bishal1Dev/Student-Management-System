import json
import logging
import os
import shutil
import threading
from copy import deepcopy
from datetime import date
from typing import Any, Dict, List, Optional

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
<<<<<<< HEAD

# ==============================================================
# Logging
# ==============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Limit incoming request body size to 1 MB to prevent abuse.
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

# ==============================================================
# Configuration (via environment variables)
# ==============================================================

ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://127.0.0.1:5000,http://localhost:5000").split(",")
    if origin.strip()
]

# Optional API key auth. Set API_KEY env var to opt in.
API_KEY = os.getenv("API_KEY", "")

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))
DEBUG = os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true", "yes")

# Restrict CORS to known origins instead of wide-open "*"
CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS}})


# ==============================================================
# Persistent storage (atomic + thread-safe)
# ==============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "students.json")
BACKUP_FILE = os.path.join(BASE_DIR, "students.corrupt.json")

# Guards against concurrent read/write on the JSON file.
_file_lock = threading.Lock()


def load_students() -> List[Dict[str, Any]]:
    """Read students from JSON storage.

    Returns an empty list if the file does not exist. If the file is
    corrupt, it is moved to a backup file and the server returns a 500
    via a raised exception so no data is silently wiped on the next save.
    """
=======
CORS(app)

# ==============================================================
# Persistent storage
# ==============================================================

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "students.json"
)


def load_students():
>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
    if not os.path.exists(DATA_FILE):
        save_students([])
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
<<<<<<< HEAD
            content = f.read()

        if not content.strip():
            return []

        data = json.loads(content)
        if not isinstance(data, list):
            raise ValueError("students.json must contain a list")
        return data

    except (json.JSONDecodeError, OSError, ValueError) as exc:
        # Preserve the corrupt file instead of silently returning [].
        try:
            shutil.copy2(DATA_FILE, BACKUP_FILE)
        except OSError:
            pass
        raise RuntimeError(
            f"students.json is corrupt and was backed up to {BACKUP_FILE}. "
            f"Please inspect or restore it. Original error: {exc}"
        ) from exc


def save_students(students: List[Dict[str, Any]]) -> None:
    """Atomically write students to disk (thread-safe)."""
    with _file_lock:
        tmp = f"{DATA_FILE}.tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(students, f, indent=2)
        # Atomic replace on supported filesystems to avoid partial writes.
        os.replace(tmp, DATA_FILE)


def get_next_id(students: List[Dict[str, Any]]) -> int:
    """Return the next available student id (max id + 1)."""
=======
            content = f.read().strip()

            if not content:
                return []

            return json.loads(content)

    except (json.JSONDecodeError, OSError):
        return []


def save_students(students):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=2)


def get_next_id(students):
>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
    if not students:
        return 1

    return max(s["id"] for s in students) + 1


<<<<<<< HEAD
def find_student(students: List[Dict[str, Any]], student_id: int) -> Optional[Dict[str, Any]]:
    """Return the student with the given id, or None."""
    for student in students:
        if student["id"] == student_id:
            return student
=======
def find_student(students, student_id):
    for student in students:
        if student["id"] == student_id:
            return student

>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
    return None


# ==============================================================
# GPA
# ==============================================================

<<<<<<< HEAD
def marks_to_gpa_points(mark: float) -> float:
    """Convert a numeric mark (0-100) into GPA points."""
    if mark >= 90:
        return 4.0
    if mark >= 80:
        return 3.5
    if mark >= 70:
        return 3.0
    if mark >= 60:
        return 2.5
    return 0.0


def calculate_gpa(grades: Dict[str, float]) -> float:
    """Average the GPA points across all recorded subjects."""
    if not grades:
        return 0.0
    total = sum(marks_to_gpa_points(mark) for mark in grades.values())
    return round(total / len(grades), 2)


def calculate_attendance_percent(attendance: Dict[str, int]) -> float:
    """Return attendance percentage (present / total * 100)."""
    present = attendance.get("present", 0)
    absent = attendance.get("absent", 0)
=======
def marks_to_gpa_points(mark):

    if mark >= 90:
        return 4.0

    elif mark >= 80:
        return 3.5

    elif mark >= 70:
        return 3.0

    elif mark >= 60:
        return 2.5

    else:
        return 0.0



def calculate_gpa(grades):

    if not grades:
        return 0.0

    total = sum(
        marks_to_gpa_points(mark)
        for mark in grades.values()
    )

    return round(total / len(grades), 2)



def calculate_attendance_percent(attendance):

    present = attendance.get("present",0)
    absent = attendance.get("absent",0)

>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
    total = present + absent

    if total == 0:
        return 0.0

    return round((present / total) * 100,2)



<<<<<<< HEAD
def student_with_computed_fields(student: Dict[str, Any]) -> Dict[str, Any]:
    """Return a deep copy of the student with computed gpa/attendance_percent added."""
    data = deepcopy(student)

    data["gpa"] = calculate_gpa(student.get("grades", {}))
    data["attendance_percent"] = calculate_attendance_percent(
        student.get("attendance", {"present": 0, "absent": 0})
    )
    return data


# ==============================================================
# Validation helpers
# ==============================================================

def parse_int(value: Any, message: str) -> int:
    """Coerce a value to int or raise ValueError with a friendly message."""
    try:
        return int(value)
    except (ValueError, TypeError):
        raise ValueError(message) from None


def parse_float(value: Any, message: str) -> float:
    """Coerce a value to float or raise ValueError with a friendly message."""
    try:
        return float(value)
    except (ValueError, TypeError):
        raise ValueError(message) from None


def validate_name(value: Any) -> str:
    """Validate and return a non-empty name."""
    name = str(value or "").strip()
    if not name:
        raise ValueError("Name is required")
    return name


def validate_course(value: Any) -> str:
    """Validate and return a non-empty course."""
    course = str(value or "").strip()
    if not course:
        raise ValueError("Course is required")
    return course


def validate_email(value: Any) -> str:
    """Validate and return a non-empty, plausible email."""
    email = str(value or "").strip()
    if not email:
        raise ValueError("Email is required")
    if email.count("@") != 1 or "." not in email:
        raise ValueError("Invalid email format")
    local, _, domain = email.partition("@")
    if not local or not domain or "." not in domain:
        raise ValueError("Invalid email format")
    return email


def validate_age(value: Any) -> int:
    """Validate and return an age between 1 and 100."""
    age = parse_int(value, "Age must be a number")
    if age < 1 or age > 100:
        raise ValueError("Age must be between 1 and 100")
    return age


def validate_marks(value: Any) -> float:
    """Validate and return marks between 0 and 100."""
    marks = parse_float(value, "Marks must be a number")
    if marks < 0 or marks > 100:
        raise ValueError("Marks must be between 0 and 100")
    return marks


def ensure_unique_email(students: List[Dict[str, Any]],
                        email: str,
                        exclude_id: Optional[int] = None) -> None:
    """Raise ValueError if another student already uses this email."""
    for s in students:
        if s.get("email", "").lower() == email.lower() and s["id"] != exclude_id:
            raise ValueError("Email already exists for another student")


# ==============================================================
# Error helpers
# ==============================================================

def validation_error(message: str) -> Any:
    return jsonify({"error": message}), 400


def not_found_error(message: str = "Student not found") -> Any:
    return jsonify({"error": message}), 404
=======
def student_with_computed_fields(student):

    data = dict(student)

    data["gpa"] = calculate_gpa(
        student.get("grades", {})
    )

    data["attendance_percent"] = calculate_attendance_percent(
        student.get(
            "attendance",
            {
                "present":0,
                "absent":0
            }
        )
    )

    return data



# ==============================================================
# Error helpers
# ==============================================================

def validation_error(message):

    return jsonify({
        "error":message
    }),400



def not_found_error(message="Student not found"):

    return jsonify({
        "error":message
    }),404

>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6


def auth_error() -> Any:
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(RuntimeError)
def handle_runtime_error(exc: RuntimeError) -> Any:
    """Return corrupt storage errors as a 500 with a clear message."""
    logger.error("Runtime error: %s", exc)
    return jsonify({"error": str(exc)}), 500


@app.errorhandler(413)
def handle_too_large(exc: Any) -> Any:
    """Return a friendly message when the request body exceeds the limit."""
    return jsonify({"error": "Request body too large"}), 413


# ==============================================================
<<<<<<< HEAD
# Auth guard (optional)
# ==============================================================

def require_api_key() -> Optional[Any]:
    """Return an error response if API auth is enabled and no valid key is sent."""
    if not API_KEY:
        return None
    provided = request.headers.get("X-API-Key", "")
    if provided != API_KEY:
        return auth_error()
    return None


@app.before_request
def check_auth() -> Optional[Any]:
    """Enforce API key on all routes except the home page."""
    if request.path == "/" or request.method == "OPTIONS":
        return None
    return require_api_key()


# ==============================================================
=======
>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
# HOME
# ==============================================================

@app.route("/")
<<<<<<< HEAD
def home() -> Any:
    return send_file("index.html")


# ==============================================================
# STUDENTS
# ==============================================================

@app.route("/students", methods=["GET"])
def get_students() -> Any:
    students = load_students()

    # Optional search: ?q=name_or_course
    query = (request.args.get("q") or "").strip().lower()
    if query:
        students = [
            s for s in students
            if query in str(s.get("name", "")).lower()
            or query in str(s.get("course", "")).lower()
        ]

    # Optional sorting: ?sort=name|gpa|attendance&order=asc|desc
    sort_key = request.args.get("sort", "").strip().lower()
    order = request.args.get("order", "asc").strip().lower()

    computed = [student_with_computed_fields(s) for s in students]

    if sort_key in ("name", "gpa", "attendance"):
        reverse = order == "desc"

        if sort_key == "name":
            computed.sort(key=lambda s: s.get("name", "").lower(), reverse=reverse)
        elif sort_key == "gpa":
            computed.sort(key=lambda s: s.get("gpa", 0), reverse=reverse)
        else:  # attendance
            computed.sort(key=lambda s: s.get("attendance_percent", 0), reverse=reverse)

    # Optional pagination: ?page=1&per_page=10
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    if page is not None and str(page).strip() != "":
        try:
            page = int(page)
            per_page = int(per_page) if per_page else 10
        except (ValueError, TypeError):
            return validation_error("page and per_page must be numbers")

        if page < 1 or per_page < 1:
            return validation_error("page and per_page must be positive")

        total = len(computed)
        start = (page - 1) * per_page
        end = start + per_page
        items = computed[start:end]

        return jsonify({
            "total": total,
            "page": page,
            "per_page": per_page,
            "students": items,
        })

    return jsonify(computed)


@app.route("/students", methods=["POST"])
def add_student() -> Any:
    data = request.get_json(silent=True)
    if not data:
        return validation_error("No data received")

    try:
        name = validate_name(data.get("name"))
        course = validate_course(data.get("course"))
        email = validate_email(data.get("email"))
        age = validate_age(data.get("age"))
    except ValueError as exc:
        return validation_error(str(exc))

    students = load_students()

    try:
        ensure_unique_email(students, email)
    except ValueError as exc:
        return validation_error(str(exc))
=======
def home():

    return send_file("index.html")



# ==============================================================
# STUDENTS
# ==============================================================


@app.route("/students", methods=["GET"])
def get_students():

    students = load_students()

    return jsonify([
        student_with_computed_fields(s)
        for s in students
    ])





@app.route("/students", methods=["POST"])
def add_student():

    data = request.get_json(silent=True)


    if not data:
        return validation_error(
            "No data received"
        )


    name = (
        data.get("name") or ""
    ).strip()


    course = (
        data.get("course") or ""
    ).strip()


    email = (
        data.get("email") or ""
    ).strip()


    age = data.get("age")



    # -------------------------
    # Validation
    # -------------------------

    if not name:
        return validation_error(
            "Name is required"
        )


    if not course:
        return validation_error(
            "Course is required"
        )


    if not email:
        return validation_error(
            "Email is required"
        )


    if "@" not in email or "." not in email:

        return validation_error(
            "Invalid email format"
        )



    if age is None or str(age).strip()=="":
        return validation_error(
            "Age is required"
        )



    try:

        age = int(age)


    except:

        return validation_error(
            "Age must be a number"
        )



    if age < 1 or age > 100:

        return validation_error(
            "Age must be between 1 and 100"
        )



    students = load_students()

>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6

    new_student = {

        "id":get_next_id(students),

        "name":name,

        "age":age,

        "email":email,

        "course":course,

        "grades":{},

        "attendance":
        {
            "present":0,
            "absent":0
        }

    }


    students.append(new_student)


    save_students(students)


    return jsonify({

        "message":
        "Student added successfully",

        "student":
        student_with_computed_fields(
            new_student
        )

    }),201
# ==============================================================
# UPDATE STUDENT
# ==============================================================


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id: int) -> Any:
    students = load_students()
    student = find_student(students, student_id)
    if student is None:
        return not_found_error()
    return jsonify(student_with_computed_fields(student))


# ==============================================================
# UPDATE STUDENT
# ==============================================================

@app.route("/students/<int:student_id>", methods=["PUT"])
<<<<<<< HEAD
def update_student(student_id: int) -> Any:
=======
def update_student(student_id):

>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
    data = request.get_json(silent=True)


    if not data:
        return validation_error(
            "No data received"
        )


    students = load_students()
<<<<<<< HEAD
    student = find_student(students, student_id)
=======


    student = find_student(
        students,
        student_id
    )


>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
    if student is None:

        return not_found_error()

<<<<<<< HEAD
    try:
        if "name" in data:
            student["name"] = validate_name(data["name"])
        if "course" in data:
            student["course"] = validate_course(data["course"])
        if "email" in data:
            email = validate_email(data["email"])
            ensure_unique_email(students, email, exclude_id=student_id)
            student["email"] = email
        if "age" in data:
            student["age"] = validate_age(data["age"])
    except ValueError as exc:
        return validation_error(str(exc))
=======


    # -------------------------
    # Name validation
    # -------------------------

    if "name" in data:

        name = str(
            data["name"]
        ).strip()


        if not name:

            return validation_error(
                "Name cannot be empty"
            )


        student["name"] = name




    # -------------------------
    # Course validation
    # -------------------------

    if "course" in data:

        course = str(
            data["course"]
        ).strip()


        if not course:

            return validation_error(
                "Course cannot be empty"
            )


        student["course"] = course




    # -------------------------
    # Email validation
    # -------------------------

    if "email" in data:

        email = str(
            data["email"]
        ).strip()


        if not email:

            return validation_error(
                "Email is required"
            )


        if "@" not in email or "." not in email:

            return validation_error(
                "Invalid email format"
            )


        student["email"] = email




    # -------------------------
    # Age validation
    # -------------------------

    if "age" in data:

        try:

            age = int(
                data["age"]
            )


        except:

            return validation_error(
                "Age must be a number"
            )



        if age < 1 or age > 100:

            return validation_error(
                "Age must be between 1 and 100"
            )


        student["age"] = age


>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6

    save_students(students)



    return jsonify({

        "message":
        "Student updated successfully",

        "student":
        student_with_computed_fields(
            student
        )

    })


<<<<<<< HEAD
=======



>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
# ==============================================================
# DELETE STUDENT
# ==============================================================

<<<<<<< HEAD
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id: int) -> Any:
    students = load_students()
    student = find_student(students, student_id)
=======

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):

    students = load_students()


    student = find_student(
        students,
        student_id
    )


>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
    if student is None:

        return not_found_error()



    students = [
        s for s in students
        if s["id"] != student_id
    ]


    save_students(students)


    return jsonify({

        "message":
        "Student deleted successfully"

    })


<<<<<<< HEAD
# ==============================================================
# GRADES
# ==============================================================

@app.route("/grades", methods=["POST"])
def add_grade() -> Any:
=======



# ==============================================================
# GRADES
# ==============================================================


@app.route("/grades", methods=["POST"])
def add_grade():

>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
    data = request.get_json(silent=True)


    if not data:

        return validation_error(
            "No data received"
        )


    try:
<<<<<<< HEAD
        student_id = parse_int(data.get("student_id"), "student_id must be a number")
        subject = str(data.get("subject") or "").strip()
        if not subject:
            raise ValueError("Subject is required")
        marks = validate_marks(data.get("marks"))
    except ValueError as exc:
        return validation_error(str(exc))

    students = load_students()
    student = find_student(students, student_id)
=======

        student_id = int(
            data.get("student_id")
        )


    except:

        return validation_error(
            "student_id must be a number"
        )



    subject = (
        data.get("subject") or ""
    ).strip()



    if not subject:

        return validation_error(
            "Subject is required"
        )



    try:

        marks = float(
            data.get("marks")
        )


    except:

        return validation_error(
            "Marks must be a number"
        )



    if marks < 0 or marks > 100:

        return validation_error(
            "Marks must be between 0 and 100"
        )



    students = load_students()


    student = find_student(
        students,
        student_id
    )


>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
    if student is None:

        return not_found_error()



    student["grades"][subject] = marks


    save_students(students)



    return jsonify({

        "message":
        "Grade added successfully",

        "student":
        student_with_computed_fields(
            student
        )

    })


<<<<<<< HEAD
@app.route("/grades", methods=["DELETE"])
def delete_grade() -> Any:
    """Delete a single subject grade for a student."""
=======



# ==============================================================
# ATTENDANCE
# ==============================================================


@app.route("/attendance", methods=["POST"])
def mark_attendance():

>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
    data = request.get_json(silent=True)


    if not data:

        return validation_error(
            "No data received"
        )



    try:
<<<<<<< HEAD
        student_id = parse_int(data.get("student_id"), "student_id must be a number")
        subject = str(data.get("subject") or "").strip()
        if not subject:
            raise ValueError("Subject is required")
    except ValueError as exc:
        return validation_error(str(exc))

    students = load_students()
    student = find_student(students, student_id)
=======

        student_id = int(
            data.get("student_id")
        )


    except:

        return validation_error(
            "student_id must be a number"
        )



    status = data.get("status")



    if status not in [
        "present",
        "absent"
    ]:

        return validation_error(
            "status must be present or absent"
        )



    students = load_students()


    student = find_student(
        students,
        student_id
    )



>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
    if student is None:

        return not_found_error()

<<<<<<< HEAD
    if subject not in student.get("grades", {}):
        return not_found_error(f"Subject '{subject}' not found for this student")

    del student["grades"][subject]
    save_students(students)

    return jsonify({
        "message": "Grade deleted successfully",
        "student": student_with_computed_fields(student),
    })


# ==============================================================
# ATTENDANCE
# ==============================================================

@app.route("/attendance", methods=["POST"])
def mark_attendance() -> Any:
    data = request.get_json(silent=True)
    if not data:
        return validation_error("No data received")

    try:
        student_id = parse_int(data.get("student_id"), "student_id must be a number")
    except ValueError as exc:
        return validation_error(str(exc))

    status = data.get("status")
    if status not in ("present", "absent"):
        return validation_error("status must be present or absent")

    students = load_students()
    student = find_student(students, student_id)
    if student is None:
        return not_found_error()

    # Track per-day attendance to prevent double-marking the same day.
    attendance = student.setdefault("attendance", {"present": 0, "absent": 0})
    records = attendance.setdefault("records", {})

    today = date.today().isoformat()
    if today in records:
        return validation_error("Attendance for today is already marked")

    records[today] = status
    attendance[status] = attendance.get(status, 0) + 1
=======


    student["attendance"][status] += 1


>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
    save_students(students)



    return jsonify({

        "message":
        "Attendance updated successfully",

        "student":
        student_with_computed_fields(
            student
        )

    })


<<<<<<< HEAD
# ==============================================================
# STATISTICS
# ==============================================================

@app.route("/statistics", methods=["GET"])
def statistics() -> Any:
=======



# ==============================================================
# STATISTICS
# ==============================================================


@app.route("/statistics", methods=["GET"])
def statistics():

>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
    students = load_students()



    if not students:

        return jsonify({

            "total_students":0,

            "average_gpa":0,

            "highest_gpa":0,

            "lowest_gpa":0,

            "average_attendance":0

        })

<<<<<<< HEAD
    gpas = [calculate_gpa(s.get("grades", {})) for s in students]
    attendance = [calculate_attendance_percent(s.get("attendance", {})) for s in students]
=======



    gpas = [

        calculate_gpa(
            s.get("grades",{})
        )

        for s in students

    ]
>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6



    attendance = [

        calculate_attendance_percent(
            s.get(
                "attendance",
                {}
            )
        )

        for s in students

    ]



    return jsonify({
<<<<<<< HEAD
        "total_students": len(students),
        "average_gpa": round(sum(gpas) / len(gpas), 2),
        "highest_gpa": max(gpas),
        "lowest_gpa": min(gpas),
        "average_attendance": round(sum(attendance) / len(attendance), 2),
    })


# ==============================================================
# REPORTS
# ==============================================================

@app.route("/report/<int:student_id>", methods=["GET"])
def report(student_id: int) -> Any:
    students = load_students()
    student = find_student(students, student_id)
=======

        "total_students":
        len(students),


        "average_gpa":
        round(
            sum(gpas)/len(gpas),
            2
        ),


        "highest_gpa":
        max(gpas),


        "lowest_gpa":
        min(gpas),


        "average_attendance":
        round(
            sum(attendance)/len(attendance),
            2
        )

    })





# ==============================================================
# REPORTS
# ==============================================================


@app.route("/report/<int:student_id>", methods=["GET"])
def report(student_id):

    students = load_students()


    student = find_student(
        students,
        student_id
    )


>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
    if student is None:

        return not_found_error()
<<<<<<< HEAD
    return jsonify(student_with_computed_fields(student))


@app.route("/reports", methods=["GET"])
def all_reports() -> Any:
=======



    return jsonify(
        student_with_computed_fields(
            student
        )
    )




@app.route("/reports", methods=["GET"])
def all_reports():

>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
    students = load_students()


    return jsonify([

        student_with_computed_fields(s)

        for s in students

    ])





# ==============================================================
<<<<<<< HEAD
# ANALYTICS / DISTRIBUTION
# ==============================================================

@app.route("/distribution", methods=["GET"])
def grade_distribution() -> Any:
    """Return the number of students per GPA band for analytics."""
    students = load_students()
    bands = {
        "A (3.5-4.0)": 0,
        "B (3.0-3.4)": 0,
        "C (2.5-2.9)": 0,
        "D (2.0-2.4)": 0,
        "F (<2.0)": 0,
    }

    for s in students:
        gpa = calculate_gpa(s.get("grades", {}))
        if gpa >= 3.5:
            bands["A (3.5-4.0)"] += 1
        elif gpa >= 3.0:
            bands["B (3.0-3.4)"] += 1
        elif gpa >= 2.5:
            bands["C (2.5-2.9)"] += 1
        elif gpa >= 2.0:
            bands["D (2.0-2.4)"] += 1
        else:
            bands["F (<2.0)"] += 1

    return jsonify({
        "total": len(students),
        "bands": bands,
    })


# ==============================================================
=======
>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
# START SERVER
# ==============================================================


if __name__ == "__main__":
<<<<<<< HEAD
=======


>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
    if not os.path.exists(DATA_FILE):

        save_students([])

<<<<<<< HEAD
    app.run(host=HOST, port=PORT, debug=DEBUG)
=======


    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
>>>>>>> a6e90f73f78e7831bdab0c5e83ee4cdb720efef6
