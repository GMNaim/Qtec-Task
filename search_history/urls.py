from django.urls import path

from .views import home, filer_searches

app_name = 'search_history'

urlpatterns = [
    path('', home, name='home'),
    path('filter-searches', filer_searches, name='filter-search-history'),
]
