# Student Management System
# Full Project Code Explanation

---

# 1. Project Introduction

The Student Management System is a web-based application developed to manage student information digitally.

The purpose of this project is to replace manual student record management with an automated system.

The system provides functionality for:

- Adding students
- Updating student information
- Deleting student records
- Managing grades
- Calculating GPA automatically
- Tracking attendance
- Generating reports
- Viewing class statistics


The project follows a client-server architecture where the frontend communicates with the backend through API requests.

---

# 2. Project Technologies

## Frontend

The frontend is developed using:

## HTML

HTML is responsible for creating the structure of the application.

It contains:

- Forms
- Input fields
- Buttons
- Tables
- Dashboard layout


## CSS

CSS is responsible for the design and appearance of the application.

It controls:

- Colors
- Layout
- Spacing
- User interface styling


## JavaScript

JavaScript provides functionality and interaction.

It is responsible for:

- Sending requests to backend
- Receiving responses
- Updating webpage content dynamically
- Handling user actions


---

# Backend

## Python Flask

Python is used for backend development.

Flask is a lightweight Python web framework used to:

- Create the server
- Create API routes
- Handle requests
- Process data
- Perform calculations
- Communicate with storage


---

# Database

## JSON Storage

Instead of using a traditional database like MySQL, this project uses JSON file storage.

The file:

```
students.json
```

stores all student information.

Advantages:

- Simple implementation
- Lightweight
- Easy to read
- Persistent storage


---

# 3. Project Structure


```
Student-Management-System

│
├── app.py
│
├── index.html
│
├── requirements.txt
│
├── students.json
│
└── .venv

```


---

# app.py

This is the main backend file.

It contains:

- Flask configuration
- API routes
- Data handling functions
- GPA calculation
- Attendance calculation
- Report generation


---

# index.html

This is the frontend interface.

It provides:

- Student forms
- Dashboard
- Tables
- Buttons
- User interaction


---

# requirements.txt

This file contains required Python libraries.


Example:

```
Flask
Flask-CORS
```


These packages are installed using:

```
pip install -r requirements.txt
```


---

# students.json

This file stores student information.


Initially:

```json
[]
```


After adding students:

```json
[
 {
  "id":1,
  "name":"Bishal",
  "age":20,
  "course":"Cyber Security"
 }
]
```


---

# 4. Application Architecture


The complete workflow:


```
             User

              |

              |

        index.html

     HTML + CSS + JavaScript

              |

              |

        HTTP Request

              |

              |

        Flask Backend

             app.py

              |

              |

       Python Processing

              |

              |

        students.json

```


---

# 5. Flask Application Setup


Code:

```python
app = Flask(__name__)

CORS(app)
```


Explanation:

First, Flask application is created.

The Flask object manages the web server.

CORS is enabled because the frontend and backend communicate with each other.

Without CORS, browser security restrictions may block frontend requests.


---

# 6. Data File Configuration


Code:

```python
DATA_FILE = os.path.join(
os.path.dirname(os.path.abspath(__file__)),
"students.json"
)
```


Explanation:

This creates the path to the JSON storage file.

The program automatically finds the location of students.json.


This makes the application portable because it can run on different systems.


---

# 7. Loading Student Data


Function:

```python
load_students()
```


Purpose:

Reads student information from JSON storage.


Process:


1. Check if students.json exists

2. If not:
   - Create an empty file

3. Open file

4. Read JSON data

5. Convert JSON into Python list

6. Return student data


Example:

JSON:

```json
[
{
"name":"Alex"
}
]
```


Python:

```python
[
{
"name":"Alex"
}
]
```


---

# 8. Saving Student Data


Function:

```python
save_students()
```


Purpose:

Writes updated student information back into JSON.


Whenever data changes:

- Add student
- Update student
- Delete student
- Add grades
- Update attendance


The save function updates the file.


---

# 9. Generating Student ID


Function:

```python
get_next_id()
```


Purpose:

Creates unique IDs.


Example:


Existing:

```
1
2
3
```


New student:


```
4
```


It uses the highest existing ID and adds 1.


This prevents duplicate IDs.


---

# 10. Finding Students


Function:

```python
find_student()
```


Purpose:

Searches student records using ID.


Example:


Input:

```
student_id = 5
```


The function searches the list and returns the matching student.


---

# 11. Student API System


The backend uses REST API endpoints.


---

# GET Students


Endpoint:

```
GET /students
```


Purpose:

Returns all students.


Process:


Frontend requests data.

↓

Flask receives request.

↓

Reads students.json.

↓

Returns student list.


---

# Add Student


Endpoint:


```
POST /students
```


Purpose:

Creates a new student.


Example request:


```json
{
"name":"John",
"age":20,
"course":"Cyber Security"
}
```


Backend process:


1. Receive data

2. Validate information

3. Generate ID

4. Create student object

5. Save into JSON

6. Return response


---

# Update Student


Endpoint:

```
PUT /students/<id>
```


Purpose:

Updates existing information.


Editable information:


- Name
- Age
- Email
- Course


---

# Delete Student


Endpoint:


```
DELETE /students/<id>
```


Purpose:


Removes student from storage.


Process:


1. Find student

2. Remove from list

3. Save updated data


---

# 12. GPA Calculation System


The project automatically calculates GPA.


Function:

```
marks_to_gpa_points()
```


It converts marks into GPA.


Rules:


| Marks | GPA |
|-|-|
|90-100|4.0|
|80-89|3.5|
|70-79|3.0|
|60-69|2.5|
|Below 60|0.0|


---

Function:

```
calculate_gpa()
```


It calculates the average GPA.


Example:


Subjects:


Python = 90

Networking = 80


Calculation:


Python:

4.0


Networking:

3.5


Final GPA:


```
(4.0 + 3.5) / 2

=3.75
```


---

# 13. Attendance System


Function:

```
calculate_attendance_percent()
```


Purpose:

Calculates attendance percentage.


Formula:


```
Attendance =
Present /
(Present + Absent)
×100
```


Example:


Present:

90


Absent:

10


Result:


```
90%
```


---

# 14. Grade Management


Endpoint:


```
POST /grades
```


Purpose:

Adds subject marks.


Example:


Request:


```json
{
"student_id":1,
"subject":"Python",
"marks":95
}
```


Backend:


1. Finds student

2. Adds subject marks

3. Saves data

4. Calculates updated GPA


---

# 15. Attendance API


Endpoint:


```
POST /attendance
```


Example:


```json
{
"student_id":1,
"status":"present"
}
```


Backend increases:


```python
attendance["present"] += 1
```


or


```python
attendance["absent"] += 1
```


---

# 16. Statistics System


Endpoint:


```
GET /statistics
```


Purpose:


Provides overall class information.


Returns:


- Total students
- Average GPA
- Highest GPA
- Lowest GPA
- Average attendance


Used for dashboard display.


---

# 17. Report Generation


Individual report:


```
GET /report/<id>
```


Returns:


- Student information
- Grades
- GPA
- Attendance


Complete report:


```
GET /reports
```


Returns all students' reports.


---

# 18. Frontend and Backend Communication


The communication process:


```
User Action

↓

JavaScript Function

↓

Fetch API Request

↓

Flask Route

↓

Python Function

↓

JSON Update

↓

Response

↓

Update Website

```


Example:


When clicking "Add Student":


1. User fills form

2. JavaScript collects data

3. Sends POST request

4. Flask receives information

5. Python stores data

6. Frontend refreshes table


---

# 19. Error Handling


The system validates input.


Examples:


Empty name:

Rejected


Invalid marks:

Rejected


Wrong student ID:

Returns error


This prevents incorrect data storage.


---

# 20. Running The Application


Activate environment:


```
.venv\Scripts\activate
```


Install dependencies:


```
pip install -r requirements.txt
```


Run server:


```
python app.py
```


Open browser:


```
http://127.0.0.1:5000
```


---

# 21. Conclusion


The Student Management System demonstrates:


- Frontend development
- Backend development
- REST API communication
- Data storage
- CRUD operations
- Automated calculations
- Report generation


The project can be expanded in future by adding:


- SQL database
- Authentication
- Cloud deployment
- User roles
- Mobile application
