
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse

from checks.forms import CreateLocationForm, CreateObjectForm, ControlEventForm, CheckListForm
from checks.models import Object, Location, ControlEvent, Question, Grade, Result, CorrectionReport, CorrectionReportComment
from checks.servises.count_score_of_control_event import Counter
from checks.servises.get_files import CheckListReport, MainReport
from checks.servises.object_page import ObjectInformation


# START PAGE

def logout_view(request):
    logout(request)
    return redirect(reverse('start_page'))


def start_view(request):
    
    return render(request, template_name='checks/index.html')


# LOCATION_VIEWS


class LocationListView(ListView):
    model = Location
    template_name = 'checks/location.html'
    context_object_name = 'locations'

    def get_context_data(self, **kwargs):
        context = super(LocationListView, self).get_context_data(**kwargs)
        context['title'] = 'Муниципалитеты'
        return context


class LocationFormView(View):
    form_class = CreateLocationForm
    template_name = 'checks/create_location.html'

    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, context=context, template_name=self.template_name)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            Location.objects.create(name=name)
            return redirect(reverse('location-list'))
        else:
            context = {'form': form}
            return render(request, context=context, template_name=self.template_name)


class LocationObjectsListView(ListView):
    model = Object
    template_name = 'checks/object.html'
    context_object_name = 'objects'

    def get_queryset(self):
        location = get_object_or_404(Location, id=self.kwargs['id'])
        return Object.objects.filter(location=location)


#   OBJECTS_VIEWS

def object_page_view(request, object_id):
    obj = Object.objects.filter(id=object_id)[0]
    information = ObjectInformation(object_id)
    context = {
        'object': obj,
        'information': information,
        'title': obj.name,
    }
    return render(request, context=context, template_name='checks/object_page.html')


def get_objects_view(request):
    objects_list = Object.objects.all()
    context = {'objects': objects_list,
               'title': 'Объекты'}
    return render(request, context=context, template_name="checks/object.html")


class ObjectFormView(View):
    form_class = CreateObjectForm
    template_name = 'checks/create_object.html'

    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, context=context, template_name=self.template_name)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            location = form.cleaned_data['location']
            Object.objects.create(name=name, location=location)
            return redirect(reverse('object-list'))
        else:
            context = {'form': form}
            return render(request, context=context, template_name='checks/create_location')


#   CONTROL_EVENT_VIEWS

class ControlEventListView(ListView):
    model = ControlEvent
    template_name = 'checks/control_event.html'

    def get(self, *args, **kwargs):
        control_events_list = self.get_queryset().order_by('-date')
        context = {
            'control_events': control_events_list,
            'title': 'Проверки',
            }
        return render(self.request, context=context, template_name=self.template_name)


@login_required
def delete_control_event_view(request):
    control_event_for_delete = request.GET['control_event']
    ControlEvent.objects.filter(id=control_event_for_delete).delete()
    return redirect(reverse('control-event-list'))


class ControlEventFormView(View):
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
            ControlEvent.objects.create(date=date, object=obj)
            return redirect(reverse('control-event-list'))
        else:
            context = {'control_event_form': form}
            return render(request, context=context, template_name=self.template_name)


class CheckListFormView(View):
    form_class = CheckListForm
    template_name = 'checks/control_event_result.html'

    def get(self, request, control_event_id):
        control_event = ControlEvent.objects.filter(id=control_event_id)[0]
        counter = Counter(control_event_id)

        context = {
            'check_list_form': self.form_class(initial={'control_event': control_event}),
            'result': Result.objects.filter(control_event=control_event_id),
            'control_event_id': control_event_id,
            'object': control_event.object,
            'date': control_event.date,
            'score': counter.count_score(),
            'manager_responsibility': counter.manager_count_score(),
            'production_responsibility': counter.production_count_score(),
            'status': counter.completeness_check(),
            'title': 'Результат проверки',
        }
        return render(request=request, context=context, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        control_event_id = self.kwargs['control_event_id']
        control_event = ControlEvent.objects.filter(id=control_event_id)[0]
        if form.is_valid():
            new_result_object = Result(
                control_event=control_event,
                question=form.cleaned_data['question'],
                grade=form.cleaned_data['grade']
            )
            new_result_object.save()
            return redirect(reverse('control-event', kwargs={'control_event_id': control_event_id}))
        else:
            result = Result.objects.filter(control_event=control_event_id)
            context = {
                'check_list_form': form,
                'result': result,
                'control_event_id': control_event_id,
                'object': control_event.object,
                'date': control_event.date,
            }
            return render(request, context=context, template_name=self.template_name)


@login_required
def delete_check_list_view(request):
    Result(id=request.GET['control_event_position_id']).delete()
    return redirect(reverse('control-event', kwargs={
        'control_event_id': request.GET['control_event_id']
    }))


def download_check_list_file(request, control_event_id):
    report = CheckListReport(control_event_id)
    response = HttpResponse(report.download_check_list_file(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f"attachment;filename={report.create_filename()}"
    return response


def download_main_report(request):
    start_date = request.GET['start_date']
    finish_date = request.GET['finish_date']
    
    report = MainReport(start_date, finish_date)
    response = HttpResponse(report.download_file(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f"attachment;filename=report.xlsx"
    return response

#   CORRECTION_REPORT

def get_correction_report(request, control_event_id):

    control_event = ControlEvent.objects.filter(id=control_event_id)[0]
    correction_report = CorrectionReport.objects.filter(control_event=control_event_id)

    if len(correction_report) == 0:
        new_correction_report = CorrectionReport(
            control_event=control_event, 
            has_given=False, has_completed=False)
        new_correction_report.save()
        return redirect(reverse('get_correction_report', kwargs={'control_event_id': control_event_id}))

    has_given = str
    has_completed = str
    
    if correction_report[0].has_given == False: 
        has_given = 'Не представлен'
    else:
        has_given = 'Представлен'

    if correction_report[0].has_completed == False:
        has_completed = 'Не отработан'
    else:
        has_completed = 'Отработан'

    comments = CorrectionReportComment.objects.filter(correction_report_id=correction_report[0].id)
    
    context = {
        'control_event': control_event,
        'has_given': has_given,
        'has_completed': has_completed,
        'comment_list': comments,
    }

    return render(request, context=context, template_name='checks/correction_report.html')


def change_correction_report(request, control_event_id):
    
    control_event = ControlEvent.objects.filter(id=control_event_id)[0]
    correction_report = CorrectionReport.objects.filter(control_event=control_event_id)[0]

    action = request.GET['change']
    
    if action == 'has_given':

        if correction_report.has_given == False:
            correction_report.has_given = True
            correction_report.save()
            return redirect(reverse('get_correction_report', kwargs={'control_event_id': control_event_id}))
        else:
            correction_report.has_given = False
            correction_report.save()
            return redirect(reverse('get_correction_report', kwargs={'control_event_id': control_event_id}))

    if action == 'has_completed':
        
        if correction_report.has_completed == False:
            correction_report.has_completed = True
            correction_report.save()
            return redirect(reverse('get_correction_report', kwargs={'control_event_id': control_event_id}))
        else:
            correction_report.has_completed = False
            correction_report.save()
            return redirect(reverse('get_correction_report', kwargs={'control_event_id': control_event_id}))


def add_correction_report_comment(request, control_event_id):
    
    correction_report = CorrectionReport.objects.filter(control_event=control_event_id)[0]

    comment = CorrectionReportComment(correction_report=correction_report, comment=request.POST['text'])
    comment.save()

    return redirect(reverse('get_correction_report', kwargs={'control_event_id': control_event_id}))


def delete_correction_report_comment(request, control_event_id):
    
    deleting_comment = CorrectionReportComment.objects.filter(id=request.GET['id']).first() 
    deleting_comment.delete()

    return redirect(reverse('get_correction_report', kwargs={'control_event_id': control_event_id}))
    