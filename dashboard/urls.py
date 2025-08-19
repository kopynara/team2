from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),             # /dashboard/
    path('upload/', views.upload, name='upload'),  # /dashboard/upload/
    path('visualize/', views.visualize, name='visualize'),  # /dashboard/visualize/
]