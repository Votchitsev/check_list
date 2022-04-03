from datetime import date
from dataclasses import dataclass

from checks.models import Object
from checks.models import ControlEvent, Result
from checks.servises.count_score_of_control_event import count_score


@dataclass
class ControlEventData:
    date: date
    score: int
    control_event_id: int


class ObjectInformation:
    def __init__(self, object_id):
        self.object_id = object_id

    def count_control_events(self):
        return ControlEvent.objects.filter(object=self.object_id).count()

    def count_control_events_in_the_year(self):
        return ControlEvent.objects.filter(object=self.object_id, date__contains=date.today().year).count()

    def count_negative_control_events(self):
        control_event_queryset = ControlEvent.objects.filter(object=self.object_id)

        count = 0

        for i in control_event_queryset:
            if count_score(i.id) < 80 or Result.objects.filter(control_event=i.id, question_id=33)[0].grade.id == 5:
                count += 1

        return count

    def average_score(self):
        queryset = ControlEvent.objects.filter(object=self.object_id)

        scores_count = 0
        control_events_count = 0

        for i in queryset:
            scores_count += count_score(i.id)
            control_events_count += 1

        return int(scores_count/control_events_count)

    def average_score_in_the_year(self):
        queryset = ControlEvent.objects.filter(object=self.object_id, date__contains=date.today().year)

        scores_count = 0
        control_events_count = 0

        for i in queryset:
            scores_count += count_score(i.id)
            control_events_count += 1

        return int(scores_count / control_events_count)

    def control_events_list(self):
        queryset = ControlEvent.objects.filter(object=self.object_id)

        result = [ControlEventData(date=i.date, score=count_score(i.id), control_event_id=i.id) for i in queryset]

        return reversed(result)
