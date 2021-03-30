from django.contrib.auth.models import User
from django.db import models


class UserSearchHistory(models.Model):
    """Keep detail record of user searches """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    searched_keyword = models.TextField()
    search_time = models.DateTimeField(auto_now=True)
    search_result = models.JSONField()
    user_ip_address = models.CharField(max_length=50)
    user_browser_details = models.CharField(max_length=500)
    user_location = models.CharField(max_length=255)
    visited_sites = models.TextField()

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
