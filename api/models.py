from django.db import models


# Create your models here.
class realtimehot(models.Model):
    srank = models.IntegerField(verbose_name="排名")
    title = models.CharField(max_length=100, verbose_name="标题")
    heat = models.CharField(max_length=100, verbose_name="热度")
    tag = models.CharField(max_length=100, verbose_name="标签")
    href = models.CharField(max_length=500, verbose_name="链接")
    datetime = models.DateTimeField(verbose_name="时间")

    class Meta:
        verbose_name = "热搜榜"
        verbose_name_plural = verbose_name

