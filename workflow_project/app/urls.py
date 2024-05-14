from django.urls import path
from .views import user_input, success

urlpatterns = [
    path('', user_input, name='user_input'),
    path('success/', success, name='success'),
]
