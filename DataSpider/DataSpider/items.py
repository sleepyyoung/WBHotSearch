# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from api.models import realtimehot


class RealTimeHotItem(DjangoItem):
    django_model = realtimehot


# class SocialEventItem(DjangoItem):
#     django_model = socialevent


