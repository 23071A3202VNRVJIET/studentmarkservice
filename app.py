# Import necessary tools from external Python libraries
from fastapi import FastAPI, HTTPException  # FastAPI is the web framework; HTTPException helps send error responses
from pydantic import BaseModel, Field       # BaseModel defines data structures; Field adds custom validation rules

# Create the main application instance. Think of 'app' as the main entry point to our web server.
app = FastAPI(title="Student Marks service")

# In-memory database (a dictionary). 
# Key: student_id (int), Value: dictionary of student details.
# NOTE: Data stored here will reset whenever the server restarts.
students = {}


# Define the data blueprint (schema) for a Student using Pydantic.
# Pydantic automatically validates incoming request data against these rules before hitting our endpoints.
class Student(BaseModel):
    # 'id' must be an integer greater than 0
    id: int = Field(gt=0)
    
    # 'name' must be a string with at least 1 character (cannot be empty)
    name: str = Field(min_length=1)
    
    # 'maths' must be a floating-point number (decimal) between 0 and 100 inclusive
    maths: float = Field(ge=0, le=100)
    
    # 'physics' must be a floating-point number between 0 and 100 inclusive
    physics: float = Field(ge=0, le=100)
    
    # 'chemistry' must be a floating-point number between 0 and 100 inclusive
    chemistry: float = Field(ge=0, le=100)


# -----------------------------------------------------------------------------
# 1. Home Endpoint
# -----------------------------------------------------------------------------
@app.get("/")
def home():
    """
    HTTP GET request to the root URL ('/').
    Serves as a health check to confirm the service is live.
    """
    return {"message": "Student CRUD Microservice is running"}


# -----------------------------------------------------------------------------
# 2. Create Student Endpoint
# -----------------------------------------------------------------------------
@app.post("/students", status_code=201)
def create_student(student: Student):
    """
    HTTP POST request to create a new student record.
    Status Code 201 Created indicates successful resource creation.
    """
    # Check if a student with the same ID already exists in our dictionary
    if student.id in students:
        # HTTP 409 Conflict: Returned when a resource already exists
        raise HTTPException(
            status_code=409,
            detail="Student ID already exists"
        )

    # Convert the Pydantic model instance to a standard Python dictionary and store it
    students[student.id] = student.model_dump()

    return {
        "message": "Student created successfully",
        "student": students[student.id]
    }


# -----------------------------------------------------------------------------
# 3. Retrieve All Students Endpoint
# -----------------------------------------------------------------------------
@app.get("/students")
def get_students():
    """
    HTTP GET request to retrieve all stored student records.
    Returns a JSON list containing dictionary records of all students.
    """
    return list(students.values())


# -----------------------------------------------------------------------------
# 4. Retrieve Single Student Endpoint
# -----------------------------------------------------------------------------
@app.get("/students/{student_id}")
def get_student(student_id: int):
    """
    HTTP GET request with a path parameter to retrieve a specific student by ID.
    """
    # Check if the requested ID exists in our storage
    if student_id not in students:
        # HTTP 404 Not Found: Returned when requested resource is missing
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return students[student_id]


# -----------------------------------------------------------------------------
# 5. Update Student Endpoint
# -----------------------------------------------------------------------------
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    """
    HTTP PUT request to completely replace an existing student record.
    """
    # Verify the student exists before updating
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Ensure consistency between URL path parameter and JSON body payload
    if student.id != student_id:
        # HTTP 400 Bad Request: Indicates invalid client request payload
        raise HTTPException(
            status_code=400,
            detail="Student ID in URL must match the ID in the request body"
        )

    # Overwrite existing record with updated dataset
    students[student_id] = student.model_dump()

    return {
        "message": "Student updated successfully",
        "student": students[student_id]
    }


# -----------------------------------------------------------------------------
# 6. Delete Student Endpoint
# -----------------------------------------------------------------------------
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    """
    HTTP DELETE request to remove a specific student record by ID.
    """
    # Verify the student exists before attempting deletion
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Remove the student from the dictionary
    del students[student_id]

    return {"message": "Student deleted successfully"}