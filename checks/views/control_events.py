from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponse


from checks.models import ControlEvent, CorrectionReport, Grade, Question, Result
from checks.servises.count_score_of_control_event import Counter
from checks.servises.get_files import CheckListReport
from checks.forms import ControlEventForm


class ControlEventListView(ListView):
    '''
    Класс ControlEventListView отвечает за отображение страницы на которой перечисляются все проверки.
    '''
    paginate_by = 27
    model = ControlEvent
    template_name = 'checks/control_event.html'
    ordering = ['-date']


@login_required
def delete_control_event_view(request):
    '''
    Функция delete_control_event_view осуществляет действия по удалению проверки
    '''
    control_event_for_delete = request.GET['control_event']
    ControlEvent.objects.filter(id=control_event_for_delete).delete()
    return redirect(reverse('control-event-list'))


class ControlEventFormView(View):
    '''
    Класс отвечает за логику функционирования формы
    по созданию проверки.
    '''
    form_class = ControlEventForm
    template_name = 'checks/control_event_create.html'

    def get(self, request):
        form = self.form_class()
        context = {'control_event_form': form}
        return render(request=request, context=context, template_name=self.template_name)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            date = form.cleaned_data['date']
            obj = form.cleaned_data['object']
            control_event = ControlEvent.objects.create(
                date=date, object=obj, 
                revizor=f"{request.user.first_name} {request.user.last_name}",
                score=0)
            correction_report = CorrectionReport(control_event=control_event, has_given=False, has_completed=False)
            correction_report.save()
            return redirect(reverse('control-event-list'))
        else:
            context = {'control_event_form': form}
            return render(request, context=context, template_name=self.template_name)


class ControlEventView(View):
    '''
    Класс отвечает за отображение страницы с результатами конкретной проверки)
    '''
    template_name = 'checks/control_event_result.html'

    def get(self, request, control_event_id):
        control_event = ControlEvent.objects.filter(id=control_event_id)[0]
        counter = Counter(control_event_id)

        if control_event.revizor != None:
            revizor = control_event.revizor
        else:
            revizor = 'Не известно'
        
        context = {
            'result': Result.objects.filter(control_event=control_event_id).order_by('question__text'),
            'questions': Question.objects.all(),
            'control_event_id': control_event_id,
            'object': control_event.object,
            'date': control_event.date,
            'score': control_event.score,
            'manager_responsibility': counter.manager_count_score(),
            'production_responsibility': counter.production_count_score(),
            'retail_manager_responsibility': counter.retail_manager_score(),
            'status': counter.completeness_check(),
            'revizor': revizor,
        }
        
        return render(request=request, context=context, template_name=self.template_name)


@login_required
def check_list_form(request, control_event_id):
    '''
    Функция принимает аргумент id проверки и отрисовывает чек-лист с вопросами для внесения
    результатов проверки
    '''
    if request.method == 'GET':
        questions_not_exists = Question.objects.exclude(question__control_event_id=control_event_id).order_by('text')
        
        context = {
            'questions': questions_not_exists,
            'control_event_id': control_event_id
        }

        return render(request, context=context, template_name='checks/check_list.html')

    if request.method == 'POST':

        for i in request.POST.dict():
            if i == 'csrfmiddlewaretoken':
                continue
            result = Result(
                control_event = ControlEvent.objects.get(id=control_event_id),
                question = Question.objects.get(id=i),
                grade = Grade.objects.get(name=request.POST.__getitem__(i)),
                )
            result.save()
            control_event = ControlEvent.objects.get(id=control_event_id) 
            control_event.score = Counter(control_event_id).count_score()
            control_event.save()
        return redirect(reverse('control-event', kwargs={'control_event_id': control_event_id}))


@login_required
def delete_check_list_view(request):
    '''
    Функция отвечает за удаление отдельной позиции чек-листа
    '''
    Result(id=request.GET['control_event_position_id']).delete()
    control_event = ControlEvent.objects.get(id=request.GET['control_event_id'])
    control_event.score = Counter(request.GET['control_event_id']).count_score()
    control_event.save()
    return redirect(reverse('control-event', kwargs={
        'control_event_id': request.GET['control_event_id']
    }))


def download_check_list_file(request, control_event_id):
    '''
    Функция принимает аргумент - id проверки и вызывает функцию CheckListReport,
    которая осуществляет выгрузку файла чек-листа в формат excel
    '''
    report = CheckListReport(control_event_id)
    response = HttpResponse(report.download_check_list_file(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f"attachment;filename={report.create_filename()}"
    return response
    