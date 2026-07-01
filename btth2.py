from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]

class Student(BaseModel):
    code: str
    name: str
    email: str
    age: int

@app.post("/students")
def add_student(student: Student):
    new_student = {
        "id": len(students) + 1,
        "code": student.code,
        "name": student.name,
        "email": student.email,
        "age": student.age
    }

    students.append(new_student)
    return new_student

@app.get("/students")
def get_students(keyword: str = "", min_age: int = 0, max_age: int = 100):
    result = []

    for student in students:
        if (
            keyword.lower() in student["name"].lower()
            or keyword.lower() in student["code"].lower()
            or keyword.lower() in student["email"].lower()
        ) and min_age <= student["age"] <= max_age:
            result.append(student)

    return result

@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    return {"message": "Không tìm thấy học viên"}

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    for student in students:
        if student["id"] == student_id:
            student["code"] = updated_student.code
            student["name"] = updated_student.name
            student["email"] = updated_student.email
            student["age"] = updated_student.age
            return student

    return {"message": "Không tìm thấy học viên"}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return {"message": "Đã xóa học viên"}

    return {"message": "Không tìm thấy học viên"}