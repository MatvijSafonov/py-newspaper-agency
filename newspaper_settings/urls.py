from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from newspaper_agency.views import RegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("newspaper_agency.urls", namespace="newspaper_agency")),
    path("", RegisterView.as_view(), name="register"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)