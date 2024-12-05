from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from newspaper_agency.views import BaseView

# urlpatterns = [
#     path("", lambda request: redirect("api/register")),
#     path("admin/", admin.site.urls),
#     path('api/', include('newspaper_agency.urls')),
#     # path('', BaseView.as_view(), name='index'),
# ]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("newspaper_agency.urls", namespace="newspaper_agency")),
    # path("accounts/", include("django.contrib.auth.urls")),
    path("", BaseView.as_view(), name='index'),
    # path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)