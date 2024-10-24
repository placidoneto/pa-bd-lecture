from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend import views

router = DefaultRouter()
router.register(r'clientes', views.ClienteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('amazon_api/', include(router.urls)),
]