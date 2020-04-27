
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from app import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'images', views.ImageViewSet)
router.register(r'formparts', views.FormPartViewSet)
router.register(r'tracings', views.TrancingViewSet)
router.register(r'figures', views.FigureViewSet)
router.register(r'points', views.PointViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('', include('app.urls')),
]

urlpatterns  += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

