from checks.models import Object, Location, ControlEvent
from pprint import pprint


def getRating():

    result = []

    for location in Location.objects.all():
        events_count = ControlEvent.objects.filter(object__location=location).count()
        
        score_list = [control_event.score for control_event in ControlEvent.objects.filter(object__location=location)]
        
        avg_score = round(sum(score_list) / len(score_list), 2)

        result.append({
            'location': location,
            'events_count': events_count,
            'avg_score': avg_score,
        })

    return sorted(result, key=lambda location: -location['avg_score'])
