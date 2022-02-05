from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from checks.forms import CreateLocationForm
from checks.models import Object, Location


def start_view(request):

    return render(request, template_name='checks/index.html')


def get_objects_view(request):

    objects_list = Object.objects.all()

    context = {'objects': objects_list}

    return render(request, context=context, template_name="checks/objects.html")


class LocationListView(ListView):
    model = Location
    template_name = 'checks/locations.html'

    def get(self, *args, **kwargs):
        location_list = self.get_queryset()
        context = {'locations': location_list}
        return render(self.request, context=context, template_name='checks/locations.html')


def delete_location(request):
    location_for_delete = request.GET['location_id']
    Location.objects.filter(id=location_for_delete).delete()
    location_list = Location.objects.all()
    context = {'locations': location_list}
    return render(request, context=context, template_name='checks/locations.html')


class LocationFormView(View):

    form_class = CreateLocationForm
    template_name = 'checks/add_location.html'

    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, context=context, template_name=self.template_name)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            Location.objects.create(name=name)
            return redirect('http://127.0.0.1:8000/locations/')
        else:
            context = {'form': form}
            return render(request, context=context, template_name=self.template_name)
