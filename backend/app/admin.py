from django.contrib import admin
from .models import  Projects, Images, FormPart, Figures, TracingOptions, Point

# Register your models here.

admin.site.register(Images)
admin.site.register(Projects)
admin.site.register(FormPart)
admin.site.register(Figures)
admin.site.register(TracingOptions)
admin.site.register(Point)
