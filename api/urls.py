from django.urls import path
from django.views.decorators.cache import cache_page
from api import views

urlpatterns = [
    path('realtimehot_wordcloud/',
         views.RealTimeHotWordCloud.as_view(),
         name="realtimehot_wordcloud"),

    path('last_week_provinces/',
         views.LastWeekProvinces.as_view(),
         name="last_week_provinces"),

    path('last_week_cities/',
         views.LastWeekCities.as_view(),
         name="last_week_cities"),

    path('realtimehot_get_result_home/',
         views.RealTimeHotGetResultForHome.as_view(),
         name="realtimehot_get_result_home"),

    path('realtimehot_search_by_time/',
         cache_page(60 * 24)(views.RealTimeHotSearchByTime.as_view()),
         name="realtimehot_search_by_time"),

    path('socialevent_get_result_home/', views.SocialEventGetResultForHome.as_view(),
         name="socialevent_get_result_home"),

]
