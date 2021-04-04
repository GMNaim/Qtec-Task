import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .models import UserSearchHistory


def home(request):
    """Show all search and filter items"""

    all_searches = UserSearchHistory.objects.all().order_by('-id')

    searches = UserSearchHistory.objects.all()
    keywords = searches.order_by('searched_keyword').distinct(
        'searched_keyword'
    )

    countries = searches.order_by('country').distinct('country')

    users = searches.order_by('user__username').distinct('user__username')

    # Total search count according fixed time range
    today = None
    yesterday = None
    last_week = None
    last_month = None
    if all_searches.count():
        time_range_count = all_searches[0].get_total_search_in_time()
        today = time_range_count['today']
        yesterday = time_range_count['yesterday']
        last_week = time_range_count['lastWeek']
        last_month = time_range_count['lastMonth']

    context = {'search_history': all_searches,
               'keywords': keywords,
               'countries': countries,
               'users': users,
               'today': today,
               'yesterday': yesterday,
               'lastWeek': last_week,
               'lastMonth': last_month
               }

    return render(request, 'search_history/base.html', context)


def filer_searches(request):
    """ Filter all search based on user selection. """

    keywords = request.GET.getlist('keyword[]')
    countries = request.GET.getlist('country[]')
    users = request.GET.getlist('user[]')
    time_range = request.GET.getlist('time_range[]')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    all_searches = UserSearchHistory.objects.all().order_by('-id')

    if from_date and to_date:
        # Formatting given date
        start_date = datetime.datetime.strptime(
            from_date,
            '%Y-%m-%d'
        ) + datetime.timedelta(days=1)
        end_date = datetime.datetime.strptime(
            to_date,
            '%Y-%m-%d'
        ) + datetime.timedelta(days=2)
        # Filtering with custom date
        all_searches = all_searches.filter(
            search_time__gte=start_date,
            search_time__lte=end_date).order_by('-search_time')

    # Filtering with Fixed time range
    if len(time_range) > 0:
        for i in time_range:
            if i == '30':  # 30 means last 30 days
                all_searches = all_searches.filter(
                    search_time__gte=datetime.datetime.today() -
                                     datetime.timedelta(days=30)
                ).order_by('-search_time')
            if i == '7':  # 7 means last 7 days
                all_searches = all_searches.filter(
                    search_time__gte=datetime.datetime.today() -
                                     datetime.timedelta(days=7)
                ).order_by('-search_time')
            if i == '1':  # 1 means last 1 days
                all_searches = all_searches.filter(
                    search_time__day=(datetime.datetime.today() -
                                      datetime.timedelta(days=1)).day
                ).order_by('-search_time')
            if i == '0':  # 0 means today
                all_searches = all_searches.filter(
                    search_time__day=datetime.datetime.today().day
                ).order_by('-search_time')

    # Filter with keyword
    if len(keywords) > 0:
        all_searches = all_searches.filter(keyword_slug__in=keywords)

    # Filter with country
    if len(countries) > 0:
        all_searches = all_searches.filter(country_slug__in=countries)

    # Filter with user
    if len(users) > 0:
        all_searches = all_searches.filter(user_slug__in=users)

    # rendering template with data for json response
    rendered_template = render_to_string(
        'search_history/ajax/filter_searches.html',
        {'all_searches': all_searches}
    )
    return JsonResponse({'data': rendered_template})
