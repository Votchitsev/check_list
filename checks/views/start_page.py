from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import redirect, render

from checks.models import ExecutiveDirector
from checks.servises.plan import make_plan


def logout_view(request):
    logout(request)
    return redirect(reverse('start_page'))

def start_view(request):
    context = {
        'executive_directors': ExecutiveDirector.objects.filter(is_worked=True),
        'plan': make_plan(),
    }
    return render(request, context=context, template_name='checks/index.html')
