from django.urls import path
from . import views

# Define the application namespace
app_name = 'blog'

# Define two different URL patterns
urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    # detailed post view
    path('<int:year>/<int:month>/<int:day>/<slug:post>',
         views.post_detail,
         name='post_detail'),
    # Django path converters: https://docs.djangoproject.com/en/5.0/topics/http/urls/#path-converters
    # re_path can be used to define complex URL patterns with regex
]