import datetime

from captcha.fields import CaptchaField
from django.db import models

from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True, null=True, verbose_name="电话号码")
    nickname = models.CharField(max_length=11, unique=False, null=True, verbose_name="昵称")
    QQ_number = models.CharField(max_length=11, unique=True, null=True, verbose_name="QQ号码")

    class Meta:
        verbose_name = "用户" 
        verbose_name_plural = verbose_name


# 注册验证码
class RegisterCaptcha(models.Model):
    captcha = models.CharField(max_length=6, verbose_name="验证码")
    email = models.EmailField(verbose_name="邮箱")
    deadline = models.DateTimeField(verbose_name="过期时间", default=datetime.datetime.strptime(
        (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"),
        "%Y-%m-%d %H:%M:%S")) 

    class Meta:
        verbose_name = "注册验证码"
        verbose_name_plural = verbose_name


class ForgotPasswordCaptcha(models.Model):
    captcha = models.CharField(max_length=6, verbose_name="验证码")
    email = models.EmailField(verbose_name="邮箱")
    deadline = models.DateTimeField(verbose_name="过期时间", default=datetime.datetime.strptime(
        (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"),
        "%Y-%m-%d %H:%M:%S"))

    class Meta:
        verbose_name = "忘记密码验证码"
        verbose_name_plural = verbose_name
