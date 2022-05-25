"""check_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from checks.views import start_view, get_objects_view, LocationFormView, LocationListView, \
    ObjectFormView, LocationObjectsListView, ControlEventListView, ControlEventFormView, \
    delete_control_event_view, CheckListFormView, delete_check_list_view, logout_view, \
    download_check_list_file, object_page_view, download_main_report, get_correction_report, change_correction_report, \
    add_correction_report_comment, delete_correction_report_comment, download_brach_statistics, download_report_not_submited

location_patterns = [
    path('list/', LocationListView.as_view(), name='location-list'),
    path('create/', LocationFormView.as_view(), name='location-create'),
    path('<int:id>/', LocationObjectsListView.as_view(), name='location'),
]

object_patterns = [
    path('list/', get_objects_view, name='object-list'),
    path('create/', ObjectFormView.as_view(), name='object-create'),
    path('<int:object_id>', object_page_view, name='object-page'),
]

control_event_patterns = [
    path('list/', ControlEventListView.as_view(), name='control-event-list'),
    path('create/', ControlEventFormView.as_view(), name='control-event-create'),
    path('delete/', delete_control_event_view, name='control-event-delete'),
    path('<int:control_event_id>/', CheckListFormView.as_view(), name='control-event'),
    path('delete_position/', delete_check_list_view, name='delete-check-list-position'),
    path('<int:control_event_id>/download_check_list/', download_check_list_file, name='download_check_list'),
    path('<int:control_event_id>/correction_report/', get_correction_report, name='get_correction_report'),
    path('<int:control_event_id>/correction_report/change/', change_correction_report, name='change_correction_report'),
    path('<int:control_event_id>/correction_report/add/', add_correction_report_comment, name='add_correction_report_comment'),
    path('<int:control_event_id>/correction_report/delete/', delete_correction_report_comment, name='delete_correction_report_comment'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start_view, name='start_page'),
    path('location/', include(location_patterns)),
    path('object/', include(object_patterns)),
    path('control_event/', include(control_event_patterns)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_view, name='logout'),
    path('report/', download_main_report, name='download_main_report'),
    path('breach_statistics/', download_brach_statistics, name="download_brach_statistics"),
    path('report_checking/report_not_submited/', download_report_not_submited, name="download_report_not_submited"),
]
