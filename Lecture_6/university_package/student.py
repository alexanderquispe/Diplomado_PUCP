
from .person import Person

class Student(Person):
    student_count = 0

    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id
        Student.student_count += 1

    def introduce(self):
        return f"{super().introduce()} I am a student with ID: {self.student_id}."

    @classmethod
    def get_student_count(cls):
        return f"There are {cls.student_count} students."

class GraduateStudent(Student):
    def __init__(self, name, age, student_id, research_topic):
        super().__init__(name, age, student_id)
        self.research_topic = research_topic

    def introduce(self):
        return f"{super().introduce()} My research topic is {self.research_topic}."
