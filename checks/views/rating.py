from django.http import HttpResponse
from checks.servises.get_files import download_rating


def download_rating_view(request):
    response = HttpResponse(
        download_rating(request.GET['start_date'], request.GET['finish_date']),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f"attachment;filename=report.xlsx"
    return response