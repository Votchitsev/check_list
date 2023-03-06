'''
Скрипт обновляет записи об общих оценках за проверки в базе данных. 
Запуск производить в консоли режима отладки.
'''

from checks.models import ControlEvent
from checks.servises.count_score_of_control_event import Counter


for event in ControlEvent.objects.all():
    try:
        old_score = event.score

        counter = Counter(event.id)
        event.score = counter.count_score()

        event.save()

        print(old_score, '-> ', event.score)

    except:
        print('error')
        break
