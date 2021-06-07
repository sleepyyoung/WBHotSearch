import datetime
import json
import random
from rest_framework.response import Response
from rest_framework.views import APIView

import django
from django.core import serializers
from django.db.models import Q
from django.views import View
import enter
from django.shortcuts import render, redirect

from enter import models
from enter.models import UserInfo
from django.contrib.auth import authenticate, login, logout
from enter.forms import LoginForm, RegisterForm, ForgotPasswordForm
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from enter.send_email import Mail


class Login(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, "login.html", {"login": "请登录:", "login_form": login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("user")
            password = request.POST.get("password")
            all_login_info = json.loads(serializers.serialize("json", UserInfo.objects.filter(username=username)))
            if len(all_login_info) != 0:
                try:
                    username = all_login_info[0]['fields']['username']
                except IndexError:
                    return render(request, "login.html", {"login": "用户名或密码错误,请重新输入:", "login_form": login_form})

                user = authenticate(username=username, password=password)
                if user:
                    url = request.GET.get("url")
                    ret = redirect(url if url else "/")
                    login(request, user=user)
                    request.session["user"] = username
                    request.session['is_login'] = "true"
                    request.session.set_expiry(None)
                    return ret
                else:
                    return render(request, "login.html", {"login": "用户名或密码错误,请重新输入:", "login_form": login_form})
            else:
                return render(request, "login.html", {"login": "用户名或密码错误,请重新输入:", "login_form": login_form})
        else:
            return render(request, "login.html", {"login": "请登录:", "login_form": login_form})


class Logout(View):
    def get(self, request):
        request.session.flush()
        logout(request)
        return redirect("/login/")


class SendEmail(APIView):
    def post(self, request):
        receiver = request.POST.get("receiver")
        method = request.POST.get("method")
        captcha = "".join([random.choice("0123456789") for _ in range(6)])
        if method == "register":
            try:
                Mail(receiver, captcha, method).send()
                if not models.RegisterCaptcha.objects.filter(email=receiver):
                    models.RegisterCaptcha(captcha=captcha, email=receiver, deadline=datetime.datetime.strptime(
                        (datetime.datetime.now() + datetime.timedelta(
                            minutes=5)).strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")).save()
                else:
                    models.RegisterCaptcha.objects.filter(
                        email=receiver).update(captcha=captcha,
                                               deadline=datetime.datetime.strptime(
                                                   (datetime.datetime.now() + datetime.timedelta(
                                                       minutes=5)).strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"))
            except:
                return JsonResponse({"error": 1})
            return JsonResponse({"error": 0})
        elif method == "forgot_password":
            try:
                Mail(receiver, captcha, method).send()
                if not models.ForgotPasswordCaptcha.objects.filter(email=receiver):
                    models.ForgotPasswordCaptcha(captcha=captcha, email=receiver,
                                                 deadline=datetime.datetime.strptime(
                                                     (datetime.datetime.now() + datetime.timedelta(
                                                         minutes=5)).strftime("%Y-%m-%d %H:%M:%S"),
                                                     "%Y-%m-%d %H:%M:%S")).save()
                else:
                    models.ForgotPasswordCaptcha.objects.filter(
                        email=receiver).update(captcha=captcha,
                                               deadline=datetime.datetime.strptime(
                                                   (datetime.datetime.now() + datetime.timedelta(
                                                       minutes=5)).strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"))
            except:
                return JsonResponse({"error": 1})
            return JsonResponse({"error": 0})


class Register(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get("username")
            nickname = request.POST.get("nickname")
            password = request.POST.get("first_password")
            captcha_email = request.POST.get("captcha_email")
            if not models.RegisterCaptcha.objects.filter(captcha=captcha_email):
                return render(request, "register.html", {"register_error": "验证码输入有误！", "register_form": register_form})
            else:
                if datetime.datetime.now() > datetime.datetime.strptime(json.loads(
                        serializers.serialize("json", models.RegisterCaptcha.objects.filter(captcha=captcha_email)))[0][
                                                                            "fields"]["deadline"], "%Y-%m-%dT%H:%M:%S"):
                    return render(request, "register.html",
                                  {"register_error": "验证码已过期，请重新点击发送！", "register_form": register_form})
                else:
                    pass
            user_list = UserInfo.objects.filter(username=username)
            if user_list:
                return render(request, "register.html", {"register_error": "该邮箱已注册！", "register_form": register_form})
            elif username.strip() != '' and password.strip() != '':
                user = UserInfo.objects.create_user(username=username, password=password, nickname=nickname)
                user.save()
                models.RegisterCaptcha.objects.filter(email=username).delete()
                return redirect("/login/")
        else:
            return render(request, "register.html", {"register_form": register_form})


class Modify(View):
    def get(self, request, method, username):
        if method == "nickname":
            register_form = RegisterForm()
            try:
                serializers.serialize("json",UserInfo.objects.filter(username=username)))[0]['fields']
            except IndexError as e:
                error = "该用户不存在！请勿通过修改URL的方式打开此页面。"
                back_button = "true"
                return render(request, "modify.html", locals())
            nickname = userdata['nickname']
            username = userdata['username']
            return render(request, "modify.html", locals())
        elif method == "password":
            register_form = RegisterForm()
            try:
                serializers.serialize("json",UserInfo.objects.filter(username=username)))[0]['fields']
            except IndexError as e:
                error = "该用户不存在！请勿通过修改URL的方式打开此页面。"
                back_button = "true"
                return render(request, "modify.html", locals())
            nickname = userdata['nickname']
            username = userdata['username']
            return render(request, "modify.html", locals())
        else:
            return render(request, "404.html")

    def post(self, request, method, username):
        register_form = RegisterForm(request.POST)
        if method == "nickname":
            nickname = request.POST.get("nickname")
            username = request.POST.get("username")
            user = UserInfo.objects.filter(username=username)
            try:
                user.update(nickname=nickname)
            except django.db.utils.DataError:
                return render(request, "modify.html", locals())
            return redirect("/")

        elif method == "password":
            username = request.POST.get("username")
            old_password = request.POST.get("old_password")
            user = authenticate(username=username, password=old_password)
            if not user:
                error = "旧密码输入有误，请重新输入！"
                return render(request, "modify.html", locals())
            first_password = request.POST.get("first_password")
            user.set_password(first_password)
            user.save()
            logout(request)
            return redirect("/login/")


class ForgotPassword(View):
    def get(self, request, username):
        forgot_password_form = ForgotPasswordForm()
        userdata = UserInfo.objects.filter(username=username)
        if not userdata:
            error = "该用户不存在！"
            back_button = "true"
            return render(request, "forgot_password.html", locals())
        return render(request, "forgot_password.html", locals())

    def post(self, request, username):
        forgot_password_form = ForgotPasswordForm(request.POST)
        username = request.POST.get("username")
        captcha_email = request.POST.get("captcha_email")

        if forgot_password_form.is_valid():
            if not models.ForgotPasswordCaptcha.objects.filter(captcha=captcha_email):
                return render(request, "forgot_password.html",
                              {"error": "验证码输入有误！", "username": username,
                               "forgot_password_form": forgot_password_form})
            else:
                if datetime.datetime.now() > datetime.datetime.strptime(json.loads(
                        serializers.serialize("json",
                                              models.ForgotPasswordCaptcha.objects.filter(captcha=captcha_email)))[0][
                                                                            "fields"]["deadline"], "%Y-%m-%dT%H:%M:%S"):
                    return render(request, "forgot_password.html",
                                  {"error": "验证码已过期，请重新点击发送！", "username": username,
                                   "forgot_password_form": forgot_password_form})
                else:
                    pass
            userdata = UserInfo.objects.get(username=username)
            first_password = request.POST.get("first_password")
            userdata.password = make_password(first_password)
            userdata.save()
            models.ForgotPasswordCaptcha.objects.filter(email=username).delete()
            return redirect("/login/")
        else:
            return render(request, "forgot_password.html",
                          {"forgot_password_form": forgot_password_form, "username": username})
