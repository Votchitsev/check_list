from checks.models import ControlEvent, Object


def has_not_control():
    return [i for i in Object.objects.all() if len(ControlEvent.objects.filter(object=i)) == 0]


def primary_control():   
    need_control_objects = ControlEvent.objects.filter(score__range=[80, 100]).order_by('date')
    need_control_objects = set(i.object for i in need_control_objects)
    return (has_not_control() + list(need_control_objects))[:15]


def repeat_control():
    repeat_control = {}
    for object in Object.objects.all():
        try:
            last_control = ControlEvent.objects.filter(id=object.id, score__range=[0, 79]).order_by('-date')[0]
            repeat_control[last_control.object] = str(last_control.date)
        except IndexError:
            continue
    return [i[0] for i in sorted(repeat_control.items(), key=lambda item: item[1])][:5]


def make_plan():
    return set(primary_control() + repeat_control())
