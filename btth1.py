from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

class Course(BaseModel):
    code: str
    name: str
    duration: int
    fee: int

@app.post("/courses")
def add_course(course: Course):
    new_course = {
        "id": len(courses) + 1,
        "code": course.code,
        "name": course.name,
        "duration": course.duration,
        "fee": course.fee
    }
    courses.append(new_course)
    return new_course

@app.get("/courses")
def get_courses(keyword: str = None, min_fee: int = None, max_fee: int = None):

    result = []

    for course in courses:

        if keyword:
            if keyword.lower() not in course["name"].lower() and keyword.lower() not in course["code"].lower():
                continue

        if min_fee is not None:
            if course["fee"] < min_fee:
                continue

        if max_fee is not None:
            if course["fee"] > max_fee:
                continue

        result.append(course)

    return result

@app.get("/courses/{course_id}")
def get_course(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            return course

    return {"message": "Không tìm thấy"}

@app.put("/courses/{course_id}")
def update_course(course_id: int, updated_course: Course):
    for course in courses:
        if course["id"] == course_id:
            course["code"] = updated_course.code
            course["name"] = updated_course.name
            course["duration"] = updated_course.duration
            course["fee"] = updated_course.fee
            return course

    return {"message": "Không tìm thấy"}

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            courses.remove(course)
            return {"message": "Xóa thành công"}

    return {"message": "Không tìm thấy"}