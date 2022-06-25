from django.urls import path

from api.views import login, register, test, ProjectViewSet, SectionViewSet, ItemViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'sections', SectionViewSet, basename='sections')
router.register(r'items', ItemViewSet, basename='tasks')

urlpatterns = [
                  path('login/', login),
                  path('register/', register),
                  path('test/', test),
              ] + router.urls

