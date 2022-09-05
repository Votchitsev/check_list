from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse

from checks.models import Location, Object
from checks.servises.object_page import ObjectInformation
from checks.forms import CreateObjectForm


def object_page_view(request, object_id):
    obj = Object.objects.filter(id=object_id)[0]
    information = ObjectInformation(object_id)
    context = {
        'object': obj,
        'information': information,
        'title': obj.name,
    }
    return render(request, context=context, template_name='checks/object_page.html')


def get_objects_view(request, object_id=None):

    context = {
        'objects': Object.objects.filter(isExists = True),
        'locations': Location.objects.all(),
        }

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
