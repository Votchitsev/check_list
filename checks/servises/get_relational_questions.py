from checks.models import Question


def get_relational_questions():
    questions = []

    for question in Question.objects.all():
        if question.parent_question:
            questions.append([question.id, question.parent_question.id])
    
    return questions


def validate_form(question_ids: list):
    handled_question_ids = [int(question) for question in question_ids if question != 'csrfmiddlewaretoken']
    relational_questions = get_relational_questions()

    for questions in relational_questions:
        match_questions_count = 0

        for question in questions:
            if question in handled_question_ids:
                match_questions_count += 1
        
        if match_questions_count > 1:
            return False
        
    
    return True
