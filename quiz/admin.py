from django.contrib import admin
from django.contrib.auth.models import User
from quiz.models import Language
from quiz.models import Set
from quiz.models import Card

admin.site.unregister(User)
admin.site.register(User)
admin.site.register(Language)
admin.site.register(Set)
admin.site.register(Card)