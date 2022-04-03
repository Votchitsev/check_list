import io

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
import xlsxwriter

from checks.forms import CreateLocationForm, CreateObjectForm, ControlEventForm, CheckListForm
from checks.models import Object, Location, ControlEvent, Question, Grade, Result
from checks.servises.count_score_of_control_event import count_score
from checks.servises.indicators_on_the_main_page import StartPageInfo
from checks.servises.get_files import CheckListReport
from checks.servises.object_page import ObjectInformation


# START PAGE

def logout_view(request):
    logout(request)
    return redirect(reverse('start_page'))


def start_view(request):
    info = StartPageInfo(queryset=ControlEvent.objects.all())
    context = {
        'title': 'Главная',
        'count_of_control_events': info.count_of_control_events(),
        'negative_results': info.count_of_negative_scores(),
        'avg_result': info.avg_result(),
        'results': info.most_positive_and_negative_results()
    }
    return render(request, context=context, template_name='checks/index.html')


# LOCATION_VIEWS


class LocationListView(ListView):
    model = Location
    template_name = 'checks/location.html'
    context_object_name = 'locations'

    def get_context_data(self, **kwargs):
        context = super(LocationListView, self).get_context_data(**kwargs)
        context['title'] = 'Муниципалитеты'
        return context


@login_required
def delete_location(request):
    Location.objects.filter(id=request.GET['location_id']).delete()
    location_list = Location.objects.all()
    context = {'locations': location_list}
    return render(request, context=context, template_name='checks/location.html')


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
        'information': information
    }
    return render(request, context=context, template_name='checks/object_page.html')


def get_objects_view(request):
    objects_list = Object.objects.all()
    context = {'objects': objects_list,
               'title': 'Объекты'}
    return render(request, context=context, template_name="checks/object.html")


@login_required
def delete_object_view(request):
    Object.objects.filter(id=request.GET['obj_id']).delete()
    return redirect(reverse('object-list'))


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
        control_events_list = self.get_queryset()
        context = {'control_events': control_events_list}
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
        form = self.form_class(initial={'control_event': control_event})
        result = Result.objects.filter(control_event=control_event_id)
        score = count_score(control_event_id=control_event_id)
        context = {
            'check_list_form': form,
            'result': result,
            'control_event_id': control_event_id,
            'object': control_event.object,
            'date': control_event.date,
            'score': score,
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
