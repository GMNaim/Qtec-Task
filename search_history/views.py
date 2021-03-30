from collections import Counter

from django.shortcuts import render

from .models import UserSearchHistory


def home(request):
    search_history = UserSearchHistory.objects.all()
    keywords = [search_item.searched_keyword.lower() for search_item in
                search_history]
    keywords_with_count = dict(Counter(keywords))
    countries = [search_item.country.lower() for search_item in search_history]
    countries_with_count = dict(Counter(countries))
    users = set([search_item.user for search_item in
                 search_history])

    context = {'search_history': search_history,
               'keywords': keywords_with_count,
               'countries': countries_with_count,
               'users': users}
    return render(request, 'search_history/base.html', context)
