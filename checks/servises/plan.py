from checks.models import ControlEvent, Object


def has_not_control():
    return [i for i in Object.objects.filter(isExists=True) if len(ControlEvent.objects.filter(object=i)) == 0]


def primary_control():   
    last_control = {}

    for object in Object.objects.filter(isExists=True):
        control_events = ControlEvent.objects.filter(object=object).order_by('-date')
        if len(control_events) > 0:
            last_control[object] = control_events[0].date

    return [i[0] for i in sorted(last_control.items(), key=lambda item: item[1])][:15]


def repeat_control():
    last_control = {}

    for object in Object.objects.filter(isExists=True):
        control_events = ControlEvent.objects.filter(object=object).order_by('-date')
        if len(control_events) > 0:
            if control_events[0].score < 80:
                last_control[object] = control_events[0].date

    return [i[0] for i in sorted(last_control.items(), key=lambda item: item[1])][:5]


def make_plan():
    return set(has_not_control() + primary_control() + repeat_control())
