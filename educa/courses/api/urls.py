from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'courses'
router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)
router.register('subjects', views.SubjectViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
