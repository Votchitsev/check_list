from checks.models import Result, Question
import math


class Counter:

    def __init__(self, control_event_id):

        self.result_object = Result.objects.filter(control_event_id=control_event_id)
        self.questions = Question.objects.all()
        self.manager_questions = [3, 6, 7, 8, 10, 21, 22, 23, 24, 25, 27, 59, 60, 62, 66, 69]
        self.manager_and_production_questions = [4, 5, 11, 16, 17, 19, 30, 31, 35, 46, 47, 50, 56, 58, 63, 64]

    def count_score(self):

        score = 0
        score_of_not_checked_questions = 0
        score_of_all_questions = sum([x.significance_score for x in self.questions]) - 2

        for i in self.result_object:
            if i.grade.name == 'Да':
                score += i.question.significance_score
            elif i.grade.name == 'Н/о':
                score_of_not_checked_questions += i.question.significance_score

        try:
            return int(math.ceil((score / (score_of_all_questions - score_of_not_checked_questions)) * 100))
        except ZeroDivisionError:
            return 0

    def manager_count_score(self):

        manager_result_object = [i for i in self.result_object if i.question.id in self.manager_questions]
        manager_and_production_result_object = [i for i in self.result_object if i.question.id in
                                                self.manager_and_production_questions]

        score = 0
        score_of_not_checked_questions = 0

        score_of_all_questions = sum([x.significance_score for x in self.questions if x.id in
                                      self.manager_questions])
        score_of_all_questions += sum([x.significance_score for x in self.questions if x.id in
                                       self.manager_and_production_questions]) / 2

        for i in manager_result_object + manager_and_production_result_object:
            if i.grade.name == "Да":
                if i.question.id in self.manager_and_production_questions:
                    score += i.question.significance_score / 2
                else:
                    score += i.question.significance_score
            elif i.grade.name == "Н/о":
                if i.question.id in self.manager_and_production_questions:
                    score_of_not_checked_questions += (i.question.significance_score / 2)
                else:
                    score_of_not_checked_questions += i.question.significance_score

        try:
            return int(math.ceil((score / (score_of_all_questions - score_of_not_checked_questions)) * 100))
        except ZeroDivisionError:
            return 0

    def production_count_score(self):

        production_result_object = [i for i in self.result_object if i.question.id not in self.manager_questions and
                                    i.question.id not in self.manager_and_production_questions]

        manager_and_production_result_object = [i for i in self.result_object if i.question.id in
                                                self.manager_and_production_questions]

        score = 0
        score_of_not_checked_questions = 0

        score_of_all_questions = sum([x.significance_score for x in self.questions if x.id not in
                                      self.manager_questions and x.id not in self.manager_and_production_questions])
        score_of_all_questions += sum([x.significance_score for x in self.questions if x.id in
                                       self.manager_and_production_questions]) / 2
        score_of_all_questions -= 2

        for i in production_result_object + manager_and_production_result_object:
            if i.grade.name == "Да":
                if i.question.id in self.manager_and_production_questions:
                    score += i.question.significance_score / 2
                else:
                    score += i.question.significance_score
            elif i.grade.name == "Н/о":
                if i.question.id in self.manager_and_production_questions:
                    score_of_not_checked_questions += i.question.significance_score / 2
                else:
                    score_of_not_checked_questions += i.question.significance_score

        try:
            return int(math.ceil((score / (score_of_all_questions - score_of_not_checked_questions)) * 100))
        except ZeroDivisionError:
            return 0

    def completeness_check(self):

        if len(self.result_object) == len(self.questions) - 2:
            return '✓'
        else:
            return '✗'

    def common_grade(self):

        if self.count_score() < 80 or self.result_object.filter(question_id=33)[0].grade == 'Нет':
            return 'Неудовлетворительно'
        elif 79 < self.count_score() < 95:
            return 'Удовлетворительно'
        elif 94 < self.count_score() < 99:
            return 'Хорошо'
        elif self.count_score() == 100:
            return 'Отлично'

    def is_overdue_food(self):

        if str(self.result_object.filter(question_id=33)[0].grade) == 'Нет':
            return 'Да'
        else:
            return 'Нет'
