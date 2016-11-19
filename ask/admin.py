from django.contrib import admin
from ask.models import Question, Answer, Tag, UserAccount

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(UserAccount)
# Register your models here.
