from datetime import date, datetime
from pprint import pprint

from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import redirect, render
from django.http import HttpResponse

from checks.models import ExecutiveDirector
from checks.servises.plan import make_plan
from checks.servises.rating import getRating
from checks.servises.get_files import BreachStatistics, MainReport, download_report_not_submited

def logout_view(request):
    logout(request)
    return redirect(reverse('start_page'))


def start_view(request):
    context = {
        'executive_directors': ExecutiveDirector.objects.filter(is_worked=True),
        'plan': make_plan(),
    }
    return render(request, context=context, template_name='checks/index.html')


def download_main_report(request):
    start_date = request.GET['start_date']
    finish_date = request.GET['finish_date']

    report = MainReport(start_date, finish_date)
    response = HttpResponse(report.download_file(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f"attachment;filename=report.xlsx"
    return response


def download_brach_statistics(request):
    start_date = request.GET['start_date']
    finish_date = request.GET['finish_date']

    report = BreachStatistics(start_date, finish_date)
    report.download_file()

    response = HttpResponse(report.download_file(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f"attachment;filename=report.xlsx"
    return response


def download_report_not_submited_view(request):   
    response = HttpResponse(download_report_not_submited(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f"attachment;filename=report.xlsx"
    return response


def ex_director_report_view(request):
    report = MainReport(
        request.GET['start_date'],
        request.GET['finish_date'],
        request.GET['executive_director']
    )
    response = HttpResponse(
        report.download_file(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f"attachment;filename=report.xlsx"
    return response


def rating(request):
    start_date = request.GET['start_date']
    finish_date = request.GET['finish_date']

    rating = getRating(start_date, finish_date)

    context = {
        'rating': rating,
        'start_date': datetime.strptime(start_date, "%Y-%m-%d"),
        'finish_date': datetime.strptime(finish_date, "%Y-%m-%d"),
        'for_download': {
            'start_date': start_date,
            'finish_date': finish_date,
        }
    }
    
    return render(request, context=context, template_name='checks/rating.html')
