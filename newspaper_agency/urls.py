from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    TopicListView,
    TopicCreateView,
    NewspaperListView,
    NewspaperDetailView,
    RedactorListView,
    RedactorCreateView,
    RedactorUpdateView,
    RedactorDeleteView,
    LoginView,
    RegisterView,
    CustomLogoutView,
    TopicUpdateView,
    TopicDeleteView,
)

urlpatterns = [
    path("topics/", TopicListView.as_view(), name="topic_list"),
    path("topic_form/", TopicCreateView.as_view(), name="topic_form"),
    path('topic_update/<int:pk>/', TopicUpdateView.as_view(), name='topic_update'),
    path('topics/<int:pk>/delete/', TopicDeleteView.as_view(), name='topic_delete'),
    path("newspaper_list/", NewspaperListView.as_view(), name="newspaper_list"),
    path("newspapers/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper_detail"),
    path("redactors/", RedactorListView.as_view(), name="redactor_list"),
    path("redactor_form/", RedactorCreateView.as_view(), name="redactor_form"),
    path("redactors/<int:pk>/update/", RedactorUpdateView.as_view(), name="redactor_update"),
    path("redactors/<int:pk>/delete/", RedactorDeleteView.as_view(), name="redactor_delete"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name = "newspaper_agency"
