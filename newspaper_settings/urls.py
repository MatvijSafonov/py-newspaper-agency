from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from newspaper_agency.views import BaseView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("newspaper_agency.urls", namespace="newspaper_agency")),
    path("", BaseView.as_view(), name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)