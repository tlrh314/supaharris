from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(GlobularCluster)
admin.site.register(Observation)
admin.site.register(Reference)
admin.site.register(Parameter)
admin.site.register(Rank)
admin.site.register(Auxiliary)
admin.site.register(Profile)
