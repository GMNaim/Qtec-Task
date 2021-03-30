from django.urls import path

from .views import home

app_name = 'search_history'

urlpatterns = [
    path('', home, name='home'),
]
