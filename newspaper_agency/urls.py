from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    TopicListView,
    NewspaperListView,
    NewspaperDetailView,
    RedactorListView,
    LoginView,
    RegisterView,
    BaseView,
    CustomLogoutView,
)

urlpatterns = [
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("newspaper_list/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspapers/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name = "newspaper_agency"
