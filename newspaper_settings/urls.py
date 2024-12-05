from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from newspaper_agency.views import BaseView

urlpatterns = [
    path("", lambda request: redirect("api/register")),
    path("admin/", admin.site.urls),
    path('api/', include('newspaper_agency.urls')),
    path('home/', BaseView.as_view(), name='base'),
]