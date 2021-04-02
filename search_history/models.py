import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class UserSearchHistory(models.Model):
    """Keep detail record of user searches """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_slug = models.SlugField(null=True, blank=True)
    searched_keyword = models.TextField()
    keyword_slug = models.SlugField(null=True, blank=True)
    search_time = models.DateTimeField(auto_now_add=True)
    search_result = models.JSONField()
    user_ip_address = models.CharField(max_length=50)
    user_browser = models.CharField(max_length=500)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    country_slug = models.SlugField(null=True, blank=True)
    visited_sites = models.TextField()

    def save(self, *args, **kwargs):
        self.keyword_slug = slugify(self.searched_keyword, allow_unicode=True)
        self.country_slug = slugify(self.country, allow_unicode=True)
        self.user_slug = slugify(self.user, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_keyword_count(self):
        return UserSearchHistory.objects.filter(
            searched_keyword__icontains=self.searched_keyword).count()

    def get_country_count(self):
        return UserSearchHistory.objects.filter(
            country__icontains=self.country).count()

    def get_user_count(self):
        return UserSearchHistory.objects.filter(
            user__username__exact=self.user.username).count()

    def get_total_search_in_time(self):
        time_range_count = {'today': 0, 'yesterday': 0, 'lastWeek': 0,
                            'lastMonth': 0}
        all_search = UserSearchHistory.objects.all()
        time_range_count['today'] = all_search.filter(
            search_time__day=datetime.datetime.today().day).count()

        time_range_count['yesterday'] = all_search.filter(
            search_time__day=(datetime.datetime.today() - datetime.timedelta(
                                  days=1)).day).count()

        time_range_count['lastWeek'] = all_search.filter(
            search_time__gte=datetime.datetime.today() -
                             datetime.timedelta(days=7)).count()

        time_range_count['lastMonth'] = all_search.filter(
            search_time__gte=datetime.datetime.today() -
                             datetime.timedelta(days=30)).count()
        return time_range_count

    def __str__(self):
        return self.searched_keyword


"""
Example of search_result value
 [
   {
       "result_title": "Search Result Title Here",
       "result_link": "link",
       "domain": "abc.com"
   },
   {
       "search_title": "Search Title 2 Here",
       "result_link": "link",
       "domain": "abc3.com"
   }
]
"""
