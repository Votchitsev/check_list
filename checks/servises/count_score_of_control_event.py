from checks.models import Result


def count_score(control_event_id):
    result_object = Result.objects.filter(control_event=control_event_id)

    score = 0
    score_of_checked_questions = 0

    for i in result_object:
        if i.grade.name == 'Yes':
            score += i.question.significance_score
            score_of_checked_questions += i.question.significance_score
        elif i.grade.name == 'No':
            score_of_checked_questions += i.question.significance_score

    try:
        return int((score / score_of_checked_questions) * 100)
    except ZeroDivisionError:
        return 0

