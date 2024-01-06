
from university.student import Student, GraduateStudent
from university.teacher import Teacher

def main():
    student1 = Student("Alice", 20, "S1001")
    teacher1 = Teacher("Dr. Smith", 45, "E1001", "Mathematics")
    grad_student1 = GraduateStudent("Bob", 24, "S1002", "Quantum Computing")

    print(student1.introduce())
    print(teacher1.introduce())
    print(grad_student1.introduce())
    print(Student.get_student_count())

if __name__ == "__main__":
    main()
