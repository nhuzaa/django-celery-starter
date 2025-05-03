from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'devices', views.DeviceViewSet)
router.register(r'protocols', views.TestProtocolViewSet)
router.register(r'results', views.TestResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 