import random

from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView
from django.core.paginator import Paginator
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse

from .forms import RedactorForm, TopicForm
from .models import Topic, Redactor, Newspaper


class BaseView(TemplateView):
    template_name = "newspaper_agency/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_topics'] = Topic.objects.count()
        context['num_redactors'] = Redactor.objects.count()
        context['num_newspapers'] = Newspaper.objects.count()

        num_visits = self.request.session.get('num_visits', 0) + 1
        self.request.session['num_visits'] = num_visits
        context['num_visits'] = num_visits

        newspaper_list = Newspaper.objects.all()

        if len(newspaper_list) > 3:
            context['random_newspapers'] = random.sample(list(newspaper_list), 3)
        else:
            context['random_newspapers'] = newspaper_list

        return context


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
    next_page = reverse_lazy("newspaper_agency:index")


class CustomLogoutView(LogoutView):
    http_method_names = ["get", "post", "options"]
    template_name = "registration/logout.html"


class TopicListView(View):
    def get(self, request):
        topics = Topic.objects.all()
        paginator = Paginator(topics, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "topics": page_obj,
            "total_topics": topics.count()
        }
        return render(request, "newspaper_agency/topic_list.html", context)


class TopicCreateView(View):
    def get(self, request):
        return render(request, "newspaper_agency/topic_form.html")

    def post(self, request):
        name = request.POST.get("name")
        if name:
            topic, created = Topic.objects.get_or_create(name=name)
            if not created:
                return render(request, "newspaper_agency/topic_form.html",
                              {"error": "A topic with this name already exists."})
            return redirect("newspaper_agency:topic_list")

        return render(request, "newspaper_agency/topic_form.html", {"error": "Please provide a topic name."})


class TopicUpdateView(UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = "newspaper_agency/topic_update.html"
    context_object_name = "topic"

    def get_success_url(self):
        return reverse("newspaper_agency:topic_list")


class TopicDeleteView(DeleteView):
    model = Topic
    template_name = "newspaper_agency/topic_delete.html"
    success_url = reverse_lazy("newspaper_agency:topic_list")


class NewspaperListView(View):
    def get(self, request):
        newspapers = Newspaper.objects.prefetch_related("topics", "publishers").all()
        paginator = Paginator(newspapers, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "newspapers": page_obj
        }
        return render(request, "newspaper_agency/newspaper_list.html", context)


class NewspaperDetailView(View):
    def get(self, request, pk):
        newspaper = get_object_or_404(Newspaper, pk=pk)
        context = {
            "newspaper": newspaper
        }
        return render(request, "newspaper_agency/newspaper_detail.html", context)


class NewspaperFormView(View):
    def get(self, request):
        topics = Topic.objects.all()
        publishers = Redactor.objects.all()
        return render(request, "newspaper_agency/newspaper_form.html", {
            "topics": topics,
            "publishers": publishers,
        })

    def post(self, request):
        title = request.POST.get("title")
        content = request.POST.get("content")
        published_date = request.POST.get("published_date")
        topic_ids = request.POST.getlist("topics")
        publisher_id = request.POST.get("publishers")

        try:
            publisher = Redactor.objects.get(id=publisher_id)
        except Redactor.DoesNotExist:
            return render(request, "newspaper_agency/newspaper_form.html", {
                "topics": Topic.objects.all(),
                "publishers": Redactor.objects.all(),
                "error": "Invalid publisher selected.",
            })

        newspaper = Newspaper.objects.create(
            title=title,
            content=content,
            published_date=published_date,
        )

        newspaper.publishers.add(publisher)
        newspaper.topics.set(topic_ids)

        return redirect("newspaper_agency:newspaper_list")


class RedactorListView(View):
    def get(self, request):
        redactors = Redactor.objects.all()
        paginator = Paginator(redactors, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "redactors": page_obj,
            "total_redactors": redactors.count()
        }
        return render(request, "newspaper_agency/redactor_list.html", context)


class RedactorCreateView(View):
    def get(self, request):
        form = RedactorForm()
        return render(request, "newspaper_agency/redactor_form.html", {"form": form})

    def post(self, request):
        form = RedactorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("newspaper_agency:redactor_list")
        return render(request, "newspaper_agency/redactor_form.html", {"form": form})


class RedactorUpdateView(UpdateView):
    model = Redactor
    fields = ["username", "first_name", "last_name", "years_of_experience"]
    template_name = "newspaper_agency/redactor_update.html"
    success_url = reverse_lazy("newspaper_agency:redactor_list")


class RedactorDeleteView(DeleteView):
    model = Redactor
    template_name = "newspaper_agency/redactor_delete.html"
    success_url = reverse_lazy("newspaper_agency:redactor_list")
