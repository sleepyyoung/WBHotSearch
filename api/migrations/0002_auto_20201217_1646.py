# Generated by Django 3.1.2 on 2020-12-17 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='realtimehot',
            options={'verbose_name': '热搜榜', 'verbose_name_plural': '热搜榜'},
        ),
        migrations.AlterField(
            model_name='realtimehot',
            name='datetime',
            field=models.DateTimeField(verbose_name='时间'),
        ),
        migrations.AlterField(
            model_name='realtimehot',
            name='heat',
            field=models.CharField(max_length=100, verbose_name='热度'),
        ),
        migrations.AlterField(
            model_name='realtimehot',
            name='href',
            field=models.CharField(max_length=500, verbose_name='链接'),
        ),
        migrations.AlterField(
            model_name='realtimehot',
            name='srank',
            field=models.IntegerField(verbose_name='排名'),
        ),
        migrations.AlterField(
            model_name='realtimehot',
            name='tag',
            field=models.CharField(max_length=100, verbose_name='标签'),
        ),
        migrations.AlterField(
            model_name='realtimehot',
            name='title',
            field=models.CharField(max_length=100, verbose_name='标题'),
        ),
    ]
