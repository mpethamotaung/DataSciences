from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.submit, name='submit'),
    path('success', views.success, name='success'),
    # Add other paths as needed
]