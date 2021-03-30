from django.shortcuts import render


def home(request):
    return render(request, 'search_history/base.html')