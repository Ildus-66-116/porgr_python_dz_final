import csv
import logging
import sys
from functools import wraps

FORMAT = ('{levelname:<4} - {asctime}. В модуле "{name}" '
          'в строке {lineno:03d} функция "{funcName}()" записала сообщение: {msg}')


class SubjectDescriptor:

    def dec_logger(func):
        def inner(*args, **kwargs):
            logger = logging.getLogger(__name__)
            logging.basicConfig(filename='task_2.log', filemode='w', encoding='utf-8', level=logging.INFO,
                                style='{', format=FORMAT)
            result = func(*args, **kwargs)
            logger_text = f'{func.__name__}:{result}, args:{args}, {kwargs}'
            logger.info(logger_text)
            return result

        return inner

    @dec_logger
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    @dec_logger
    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)

    @dec_logger
    def __set__(self, instance, value):
        if not isinstance(value, str) or not value[0].isupper():
            logging.error(ValueError("ФИО должно состоять только из букв и начинаться с заглавной буквы"))
            raise ValueError("ФИО должно состоять только из букв и начинаться с заглавной буквы")
        setattr(instance, self.private_name, value)


class Student:
    def dec_logger(func):
        def inner(*args, **kwargs):
            logger = logging.getLogger(__name__)
            logging.basicConfig(filename='task_2.log', filemode='w', encoding='utf-8', level=logging.INFO,
                                style='{', format=FORMAT)
            result = func(*args, *kwargs)
            logger_text = f'{func.__name__}:{result}, args:{args}, {kwargs}'
            logger.info(logger_text)
            return result

        return inner

    name = SubjectDescriptor()
    _subjects_csv = []
    subjects = {}
    @dec_logger
    def __init__(self, name, subjects_file):
        self.name = name
        self.load_subjects(subjects_file)

    @dec_logger
    def load_subjects(self, subjects_file):
        with open(subjects_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for line in reader:
                for subject_name in line:
                    self._subjects_csv.append(subject_name)

    @dec_logger
    def add_grade(self, subject_name, grade):
        if not isinstance(grade, int) or not 2 <= grade <= 5:
            raise ValueError("Оценка должна быть целым числом от 2 до 5")
        if subject_name in self._subjects_csv:
            self.subjects.setdefault(subject_name, {'grades': []})
            self.subjects[subject_name].setdefault('grades', [])
            self.subjects[subject_name]['grades'].append(grade)
        else:
            raise ValueError(f"Предмет {subject_name} не найден")

    @dec_logger
    def add_test_score(self, subject_name, test_score):
        if subject_name not in self._subjects_csv:
            raise ValueError(f"Предмет {subject_name} не найден")
        if not isinstance(test_score, int) or not 0 <= test_score <= 100:
            raise ValueError("Результат теста должен быть целым числом от 0 до 100")
        if subject_name in self._subjects_csv:
            self.subjects.setdefault(subject_name, {'test_scores': []})
            self.subjects[subject_name].setdefault('test_scores', [])
            self.subjects[subject_name]['test_scores'].append(test_score)

    @dec_logger
    def get_average_test_score(self, subject_name):
        if subject_name not in self._subjects_csv:
            logging.error(ValueError(f"Предмет {subject_name} не найден"))
            raise ValueError(f"Предмет {subject_name} не найден")
        total_scores = 0
        number_scores = 0
        for key, value in self.subjects.items():
            if key == subject_name:
                if (sum(value['test_scores'])) != 0:
                    number_scores += 1
                total_scores += (sum(value['test_scores']))
            return total_scores / number_scores if total_scores > 0 else None

    @dec_logger
    def get_average_grade(self):
        total_grades = 0
        total_subjects = 0
        for i in self.subjects.values():
            if (sum(i['grades'])) != 0:
                total_subjects += 1
            total_grades += (sum(i['grades']))
        return total_grades / total_subjects if total_subjects > 0 else None

    @dec_logger
    def __getattr__(self, subject_name):
        if subject_name in self._subjects_csv:
            return self.subjects[subject_name]
        else:
            raise ValueError(f"Предмет {subject_name} не найден")

    def __str__(self):
        subjects_list = ', '.join(self.subjects.keys())
        return f"Студент: {self.name}\nПредметы: {str(subjects_list)}"


if __name__ == '__main__':
    if len(sys.argv) > 1:
        student = Student(sys.argv[1], "subjects.csv")
        print(student)
    else:
        student_1 = Student("Сидоров Сидор", "subjects.csv")
        average_history_score = student_1.get_average_test_score("Литература")
        student_1.add_grade("Литература", 5)
        print(student_1)

        student_2 = Student("Иван Иванов", "subjects.csv")
        student_2.add_grade("Математика", 4)
        student_2.add_test_score("Математика", 85)
        student_2.add_grade("История", 5)
        student_2.add_test_score("История", 92)
        print(student_2)

        average_grade = student_2.get_average_grade()
        print(f"Средний балл: {average_grade}")
