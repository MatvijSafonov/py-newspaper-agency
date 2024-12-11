from django.contrib import admin

from .models import Redactor, Newspaper, Topic

admin.site.register(Redactor)
admin.site.register(Newspaper)
admin.site.register(Topic)
