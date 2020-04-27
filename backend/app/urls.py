from django.urls import path
from app import views

urlpatterns = [
    path('getLabelingInfo/<int:projectId>/<int:imageId>/',views.Images_Detail),
]
