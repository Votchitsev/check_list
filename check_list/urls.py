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
from django.urls import path

from checks.views import start_view, get_objects_view, LocationFormView, LocationListView, delete_location

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start_view),
    path('objects/', get_objects_view),
    path('locations/', LocationListView.as_view()),
    path('add_location/', LocationFormView.as_view()),
    path('locations/delete/', delete_location),
]
