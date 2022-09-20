from checks.models import Object, Location, ControlEvent


def getRating(start_date, finish_date):
    result = []
    place = 0

    for location in Location.objects.all():
        events_count = ControlEvent.objects.filter(object__location=location, date__range=[start_date, finish_date]).count()
        
        score_list = [control_event.score for control_event in ControlEvent.objects.filter(object__location=location, date__range=[start_date, finish_date])]
         
        if len(score_list) != 0:
            avg_score = round(sum(score_list) / len(score_list), 2)

            result.append({
            'location': location,
            'events_count': events_count,
            'avg_score': avg_score,
        })
  
    sortedList = sorted(result, key=lambda location: -location['avg_score'])

    for location in sortedList:
        place += 1
        location['place'] = place

    return sortedList
