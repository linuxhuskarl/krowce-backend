from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Session)
admin.site.register(Team)

admin.site.register(User)
admin.site.register(Sentence)
admin.site.register(Item)
admin.site.register(Score)
