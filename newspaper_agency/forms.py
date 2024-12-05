from django import forms
from .models import Topic, Redactor, Newspaper


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["name"]


class RedactorForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ["username", "first_name", "last_name", "email", "password", "years_of_experience"]
        widgets = {
            "password": forms.PasswordInput(),
        }


class NewspaperForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = ["title", "content", "published_date", "topics", "publishers"]
        widgets = {
            "published_date": forms.DateInput(attrs={"type": "date"}),
        }
