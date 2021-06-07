"""home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from home import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', views.HomePage.as_view(), name="homepage"),  

    path('realtimehot/search_by_content/', views.RealTimeHotSearchByContent.as_view(),
         name="realtimehot_search_by_content"),

    path('realtimehot/search_by_time/',
         views.RealTimeHotSearchByTime.as_view(),
         name="realtimehot_search_by_time"),

    path('404/', views.NotFound.as_view()),
]
