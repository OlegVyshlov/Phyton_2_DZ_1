class Person:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Mentor(Person):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []

    def __str__(self):
        return super().__str__() + "\n"


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        average_grade = sum(sum(grades) / len(grades) for grades in self.grades.values()) / len(self.grades) \
            if self.grades else 0
        return super().__str__() + f"\nСредняя оценка за лекции: {average_grade:.1f}"


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


class Student(Person):
    def __init__(self, name, surname, gender):
        super().__init__(name, surname)
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        average_grade = sum(sum(grades) / len(grades) for grades in self.grades.values()) / len(self.grades) \
            if self.grades else 0
        finished_courses = ", ".join(self.finished_courses)
        courses_in_progress = ", ".join(self.courses_in_progress)
        return super().__str__() + f"\nСредняя оценка за домашние задания: {average_grade:.1f}\n" \
                                   f"Курсы в процессе изучения: {courses_in_progress}\n" \
                                   f"Завершенные курсы: {finished_courses}"


def average_grade_by_course(students, course):
    total_grade = 0
    count = 0
    for student in students:
        if course in student.grades:
            total_grade += sum(student.grades[course]) / len(student.grades[course])
            count += 1
    if count > 0:
        return total_grade / count
    return 0


def average_grade_by_lecturer(lecturers, course):
    total_grade = 0
    count = 0
    for lecturer in lecturers:
        if course in lecturer.grades:
            total_grade += sum(lecturer.grades[course]) / len(lecturer.grades[course])
            count += 1
    if count > 0:
        return total_grade / count
    return 0


# Создание экземпляров классов
student1 = Student('Ruoy', 'Eman', 'your_gender')
student2 = Student('John', 'Doe', 'your_gender')
lecturer1 = Lecturer('Some', 'Buddy')
lecturer2 = Lecturer('Jane', 'Smith')
reviewer1 = Reviewer('Robert', 'Johnson')
reviewer2 = Reviewer('Alice', 'Williams')

# Присвоение курсов
student1.courses_in_progress.append('Python')
student2.courses_in_progress.append('Python')
lecturer1.courses_attached.append('Python')
lecturer2.courses_attached.append('Python')
reviewer1.courses_attached.append('Python')
reviewer2.courses_attached.append('Python')

# Выставление оценок
reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student2, 'Python', 8)
reviewer2.rate_hw(student1, 'Python', 9)
reviewer2.rate_hw(student2, 'Python', 7)

# Печать информации
print(student1)
print(student2)
print(lecturer1)
print(lecturer2)
print(reviewer1)
print(reviewer2)

# Сравнение студентов и лекторов
print(f"Средняя оценка за домашние задания по курсу 'Python': "
      f"{average_grade_by_course([student1, student2], 'Python'):.1f}")
print(f"Средняя оценка за лекции по курсу 'Python': "
      f"{average_grade_by_lecturer([lecturer1, lecturer2], 'Python'):.1f}")