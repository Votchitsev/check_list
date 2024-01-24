import math
from django.db.models import F
from checks.models import Result, Question, EmployeePosition, EmployeePositionQuestion
from checks.servises.get_relational_questions import validate_form



class Counter:

    def __init__(self, control_event_id):

        self.result_object = Result.objects.filter(control_event_id=control_event_id)
        self.questions = Question.objects.all()
        self.manager_questions = [3, 6, 7, 8, 10, 21, 22, 23, 24, 25, 27, 37, 38, 59, 60, 62, 70]
        self.retail_manager_questions = [66, 67, 68, 69, 71]
        self.manager_and_production_questions = [4, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19, 30, 35, 46, 47, 50, 56, 61, 63, 64]

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
        
        score_of_all_questions -= 1

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

        production_result_object = [
            i for i in self.result_object 
            if i.question.id not in self.manager_questions 
            and i.question.id not in self.manager_and_production_questions
            and i.question.id not in self.retail_manager_questions
            ]

        manager_and_production_result_object = [
            i for i in self.result_object if i.question.id in self.manager_and_production_questions
            ]

        score = 0
        score_of_not_checked_questions = 0

        score_of_all_questions = sum(
            [x.significance_score for x in self.questions 
                if x.id not in self.manager_questions
                and x.id not in self.manager_and_production_questions
                and x.id not in self.retail_manager_questions]
                )
        score_of_all_questions += sum([x.significance_score for x in self.questions if x.id in
                                       self.manager_and_production_questions]) / 2
        score_of_all_questions -= 1

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
        
    def retail_manager_score(self):
        retail_manager_result_object = [i for i in self.result_object if i.question.id in self.retail_manager_questions]

        score = 0
        score_of_not_checked_questions = 0
        score_of_all_questions = sum(
            [x.significance_score for x in self.questions if x.id in self.retail_manager_questions]
                )
        
        for i in retail_manager_result_object:
            if i.grade.name == "Да":
                score += i.question.significance_score
                
            elif i.grade.name == "Н/о":
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
        
        if self.count_score() <= 80 or self.is_overdue_food() == 'Да':
            return 'Неудовлетворительно'
        elif 80 < self.count_score() < 95:
            return 'Удовлетворительно'
        elif 94 < self.count_score() < 100:
            return 'Хорошо'
        elif self.count_score() == 100:
            return 'Отлично'

    def is_overdue_food(self):
        try:
            if str(self.result_object.filter(question_id=33)[0].grade) == 'Нет':
                return 'Да'
            else:
                return 'Нет'
        except IndexError:
            return '-'

    def is_poor_quality(self):
        try:
            if str(self.result_object.filter(question_id=34)[0].grade) == 'Нет':
                return 'Да'
            else:
                return 'Нет'
        except IndexError:
            return '-'


class NewCounter:
    def __init__(self, control_event_id):
        self.control_event_id = control_event_id
        self.result_object = Result.objects.filter(control_event_id=control_event_id).select_related('question')
        self.questions = Question.objects.all()
        self.control_count_questions = len([i for i in self.questions if not i.parent_question])

    def count_score(self):
        score = 0
        score_of_not_checked_questions = 0
        score_of_all_questions = sum([x.significance_score for x in self.questions if not x.parent_question])

        for i in self.result_object:
            if i.grade.name == 'Да':
                score += i.question.significance_score
            elif i.grade.name == 'Н/о':
                score_of_not_checked_questions += i.question.significance_score

        try:
            return int(math.ceil((score / (score_of_all_questions - score_of_not_checked_questions)) * 100))
        except ZeroDivisionError:
            return 0
    
    def employee_count_score(self):
        employee_questions = EmployeePositionQuestion.objects.all()
        employees = EmployeePosition.objects.all()

        result = dict()

        for employee in employees:
            non_checked_score = 0
            score = 0

            all_employee_questions = employee_questions.filter(employee_position=employee).annotate(
                    parent_question=F('question__parent_question')
                )

            all_employee_questions_ids = [x.question.id for x in all_employee_questions]

            all_questions_score = sum([x.question.significance_score for x in all_employee_questions if not x.parent_question])

            for r in self.result_object:
                if r.question.id in all_employee_questions_ids:
                    if r.grade.name == 'Н/о':
                        non_checked_score += r.question.significance_score

                    if r.grade.name == 'Да':
                        score += r.question.significance_score

            try:
                if employee.position in result:
                    result[employee.position] += int(math.ceil((score / (all_questions_score - non_checked_score)) * 100))

                else:
                    result[employee.position] = int(math.ceil((score / (all_questions_score - non_checked_score)) * 100))
            except ZeroDivisionError:
                result[employee.position] = 0

        return result

    def completeness_check(self):
        questions = [x.question.id for x in self.result_object]
        is_valid = validate_form(questions)

        if is_valid and len(questions) == self.control_count_questions:
            return '✓'
        else:
            return '✗'

    def common_grade(self):
        if self.count_score() <= 80 or self.is_overdue_food() == 'Да':
            return 'Неудовлетворительно'
        elif 80 < self.count_score() < 95:
            return 'Удовлетворительно'
        elif 94 < self.count_score() < 100:
            return 'Хорошо'
        elif self.count_score() == 100:
            return 'Отлично'

    def is_overdue_food(self):
        try:
            overdue_food_questions = self.result_object.filter(question_id__in=[33, 71])

            for question in overdue_food_questions:

                if str(question.grade) == 'Нет':
                    return 'Да'

            return 'Нет'

        except IndexError:
            return '-'

    def is_poor_quality(self):
        try:
            if str(self.result_object.filter(question_id=34)[0].grade) == 'Нет':
                return 'Да'
            else:
                return 'Нет'
        except IndexError:
            return '-'
