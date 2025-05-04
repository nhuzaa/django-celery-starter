from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('devicelist', views.DeviceViewSet, basename='devicelist')
router.register('protocols', views.TestProtocolViewSet, basename='protocols')
router.register('results', views.TestResultViewSet, basename='results')

urlpatterns = [
    path('', include(router.urls)),
] 