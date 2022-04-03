from checks.models import Result, Question
import math


def count_score(control_event_id):

    result_object = Result.objects.filter(control_event=control_event_id)
    questions = Question.objects.all()

    score = 0
    score_of_not_checked_questions = 0
    score_of_all_questions = sum([x.significance_score for x in questions]) - 2

    for i in result_object:
        if i.grade.name == 'Да':
            score += i.question.significance_score
        elif i.grade.name == 'Н/о':
            score_of_not_checked_questions += i.question.significance_score

    try:
        return int(math.ceil((score / (score_of_all_questions - score_of_not_checked_questions)) * 100))
    except ZeroDivisionError:
        return 0
