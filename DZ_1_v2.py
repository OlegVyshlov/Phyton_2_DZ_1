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


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        average_grade = self.calculate_average_grade()
        return f"{super().__str__()}\nСредняя оценка за лекции: {average_grade:.1f}"

    def calculate_average_grade(self):
        total_grade = sum(sum(grades) / len(grades) for grades in self.grades.values()) / len(self.grades) \
            if self.grades else 0
        return total_grade

    def __lt__(self, other):
        return self.calculate_average_grade() < other.calculate_average_grade()

    def __gt__(self, other):
        return self.calculate_average_grade() > other.calculate_average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"{super().__str__()}\nУ лекторов:"


class Student(Person):
    def __init__(self, name, surname, gender):
        super().__init__(name, surname)
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        average_grade = self.calculate_average_grade()
        courses_in_progress = ", ".join(self.courses_in_progress)
        finished_courses = ", ".join(self.finished_courses)
        return f"{super().__str__()}\n" \
               f"Средняя оценка за домашние задания: {average_grade:.1f}\n" \
               f"Курсы в процессе изучения: {courses_in_progress}\n" \
               f"Завершенные курсы: {finished_courses}"

    def calculate_average_grade(self):
        total_grades = sum(sum(grades) / len(grades) for grades in self.grades.values()) / len(self.grades) \
            if self.grades else 0
        return total_grades

def avg_hw_grade(students, course):
    grades = []
    for student in students:
        if course in student.grades:
            grades.extend(student.grades[course])
    average_grade = sum(grades) / len(grades) if grades else 0
    return average_grade

def avg_lecture_grade(lecturers, course):
    grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            grades.extend(lecturer.grades[course])
    average_grade = sum(grades) / len(grades) if grades else 0
    return average_grade

student1 = Student('Иван', 'Иванов', 'мужчина')
student1.courses_in_progress += ['Python']
student1.finished_courses += ['Введение в программирование']

student2 = Student('Ирина', 'Петрова', 'женщина')
student2.courses_in_progress += ['Python', 'Git']
student2.finished_courses += ['Введение в программирование', 'Основы JavaScript']

lecturer1 = Lecturer('Сергей', 'Степанов')
lecturer1.courses_attached += ['Python']

lecturer2 = Lecturer('Кирилл', 'Викторов')
lecturer2.courses_attached += ['Git']

reviewer1 = Reviewer('Семён', 'Кузьмин')
reviewer1.courses_attached += ['Python']

reviewer2 = Reviewer('Cаша', 'Белый')
reviewer2.courses_attached += ['Git']

reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student1, 'Python', 8)
reviewer2.rate_hw(student1, 'Git', 7)
reviewer2.rate_hw(student2, 'Python', 10)
reviewer2.rate_hw(student2, 'Git', 9)

student1.rate_lecture(lecturer1, 'Python', 9)
student1.rate_lecture(lecturer2, 'Git', 8)
student2.rate_lecture(lecturer1, 'Python', 10)
student2.rate_lecture(lecturer2, 'Git', 7)

print(reviewer1)
print(reviewer2)
print(lecturer1)
print(lecturer2)
print(student1)
print(student2)

print(avg_hw_grade([student1, student2], 'Python'))
print(avg_hw_grade([student1, student2], 'Git'))
print(avg_lecture_grade([lecturer1, lecturer2], 'Python'))
print(avg_lecture_grade([lecturer1, lecturer2], 'Git'))
