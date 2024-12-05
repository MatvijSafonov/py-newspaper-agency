from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Topic, Redactor, Newspaper
from .forms import RedactorForm



class BaseView(TemplateView):
    template_name = 'newspaper_agency/index.html'


class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = RedactorForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)


class LoginView(BaseLoginView):
    template_name = "registration/login.html"

class CustomLogoutView(LogoutView):
    template_name = "registration/logout.html"
    next_page = reverse_lazy("newspaper_agency:logout")

class TopicListView(View):
    def get(self, request):
        topics = Topic.objects.all()
        data = [{"id": topic.id, "name": topic.name} for topic in topics]
        return JsonResponse(data, safe=False)


class NewspaperListView(View):
    def get(self, request):
        newspapers = Newspaper.objects.prefetch_related("topics", "publishers").all()
        data = [
            {
                "id": newspaper.id,
                "title": newspaper.title,
                "published_date": newspaper.published_date,
                "topics": [topic.name for topic in newspaper.topics.all()],
                "publishers": [
                    {
                        "id": publisher.id,
                        "name": f"{publisher.first_name} {publisher.last_name}",
                        "username": publisher.username,
                    }
                    for publisher in newspaper.publishers.all()
                ],
            }
            for newspaper in newspapers
        ]
        return JsonResponse(data, safe=False)


class NewspaperDetailView(View):
    def get(self, request, pk):
        newspaper = get_object_or_404(Newspaper.objects.prefetch_related("topics", "publishers"), pk=pk)
        data = {
            "id": newspaper.id,
            "title": newspaper.title,
            "content": newspaper.content,
            "published_date": newspaper.published_date,
            "topics": [topic.name for topic in newspaper.topics.all()],
            "publishers": [
                {
                    "id": publisher.id,
                    "name": f"{publisher.first_name} {publisher.last_name}",
                    "username": publisher.username,
                }
                for publisher in newspaper.publishers.all()
            ],
        }
        return JsonResponse(data)


class RedactorListView(View):
    def get(self, request):
        redactors = Redactor.objects.all()
        data = [
            {
                "id": redactor.id,
                "username": redactor.username,
                "first_name": redactor.first_name,
                "last_name": redactor.last_name,
                "years_of_experience": redactor.years_of_experience,
            }
            for redactor in redactors
        ]
        return JsonResponse(data, safe=False)
