from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from .models import Topic, Redactor, Newspaper
from .forms import RedactorForm, TopicForm


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
        context = {
            "topics": topics,
            "total_topics": topics.count()
        }
        return render(request, 'newspaper_agency/topic_list.html', context)


class TopicCreateView(View):
    def get(self, request):
        return render(request, 'newspaper_agency/topic_form.html')

    def post(self, request):
        name = request.POST.get('name')
        if name:
            topic, created = Topic.objects.get_or_create(name=name)
            if not created:
                return render(request, 'newspaper_agency/topic_form.html',
                              {'error': 'A topic with this name already exists.'})
            return redirect('newspaper_agency:topic_list')

        return render(request, 'newspaper_agency/topic_form.html', {'error': 'Please provide a topic name.'})


class TopicUpdateView(UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'newspaper_agency/topic_update.html'
    context_object_name = 'topic'

    def get_success_url(self):
        return reverse('newspaper_agency:topic_list')


class TopicDeleteView(DeleteView):
    model = Topic
    template_name = 'newspaper_agency/topic_delete.html'
    success_url = reverse_lazy('newspaper_agency:topic_list')


class NewspaperListView(View):
    def get(self, request):
        newspapers = Newspaper.objects.prefetch_related("topics", "publishers").all()
        context = {
            "newspapers": newspapers
        }
        return render(request, 'newspaper_agency/newspaper_list.html', context)


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
        total_redactors = redactors.count()
        context = {
            "redactors": redactors,
            "total_redactors": total_redactors
        }
        return render(request, 'newspaper_agency/redactor_list.html', context)


class RedactorCreateView(View):
    def get(self, request):
        form = RedactorForm()
        return render(request, 'newspaper_agency/redactor_form.html', {'form': form})

    def post(self, request):
        form = RedactorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('newspaper_agency:redactor_list')
        return render(request, 'newspaper_agency/redactor_form.html', {'form': form})


class RedactorUpdateView(UpdateView):
    model = Redactor
    fields = ['username', 'first_name', 'last_name', 'years_of_experience']
    template_name = 'newspaper_agency/redactor_update.html'
    success_url = reverse_lazy('newspaper_agency:redactor_list')


class RedactorDeleteView(DeleteView):
    model = Redactor
    template_name = 'newspaper_agency/redactor_delete.html'
    success_url = reverse_lazy('newspaper_agency:redactor_list')
