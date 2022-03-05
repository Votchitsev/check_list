from checks.models import Object
from checks.models import ControlEvent
from datetime import date


class ObjectInformation:
    def __init__(self, object_id):
        self.object_id = object_id

    def count_control_events(self):
        return ControlEvent.objects.filter(object=self.object_id).count()

    def count_control_events_in_the_year(self):
        return ControlEvent.objects.filter(object=self.object_id, date__contains=date.today().year).count()

    def count_negative_control_events(self):
        pass

    def average_score(self):
        pass

    def average_score_in_the_year(self):
        pass
