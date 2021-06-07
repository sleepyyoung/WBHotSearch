from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from api import models
from django.core import serializers
import json
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
import pymysql
from urllib import parse
from django.views import View
from functools import wraps
import time
import re
from enter.models import UserInfo
import base64


def loginORnot(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        is_login = request.session.get("is_login")  
        request.session.clear_expired() 
        if is_login != "true":
            token = request.GET.get("token")
            page = request.GET.get("page")
            if token != "" and page != "":
                return redirect(f"/login/?url={request.path_info}?token={token}&page={page}")
            elif token != "" and page == "":
                return redirect(f"/login/?url={request.path_info}?token={token}")
            else:
                return redirect(f"/login/?url={request.path_info}")

        ret = func(request, *args, **kwargs)
        return ret

    return inner


class HomePage(View):
    def get(self, request):
        try:
            if request.session['is_login'] == "true":
                login_status = "true"
                username = request.session['user']
                userdata = json.loads(
                    serializers.serialize("json",
                                          UserInfo.objects.filter(username=username)
                                          ))[0]['fields']
                now_nickname = userdata['nickname']
                now_user = userdata['username']
        except KeyError as e:
            login_status = "false"
        return render(request, "home.html", locals())


class RealTimeHotSearchByTime(View):
    @method_decorator(loginORnot)
    def get(self, request):
        try:
            if request.session['is_login'] == "true":
                login_status = "true"
                username = request.session['user']
                userdata = json.loads(
                    serializers.serialize("json",
                                          UserInfo.objects.filter(username=username)
                                          ))[0]['fields']
                now_nickname = userdata['nickname']
                now_user = userdata['username']
        except KeyError as e:
            login_status = "false"
        return render(request, "realtimehot_search_by_time.html", locals())


class RealTimeHotSearchByContent(View):
    @method_decorator(loginORnot)
    def get(self, request):
        try:
            token_s = request.GET.get("token")
            token = parse.unquote(base64.b64decode(base64.b64decode(token_s)).decode())
        except:
            return redirect("/")

        try:
            content, method = re.findall(r"\?content=(.*?)&method=(\w+)", token)[0]
            content_url = content
            conn = pymysql.connect(
                host="127.0.0.1",
                user="root",
                password="19834044876",
                database="WBHotSearch"
            )
            cursor =conn.cursor()
            if method == "fuzzy":
                content_match = "LIKE \"%" + content + "%\""
                cursor.execute(f"""
            SELECT id,srank,A.title,heat,tag,href,B.datetime_earliest datetime_earliest,B.datetime_latest datetime_latest
            FROM api_realtimehot A,
            (SELECT title, MIN(datetime), MAX(datetime)
            FROM api_realtimehot
            WHERE title {content_match}
            GROUP BY title) AS B(title, datetime_earliest, datetime_latest)
            WHERE A.datetime = B.datetime_earliest AND A.title = B.title AND tag <> '荐';
            """)
            if method == "precise":
                content_match = "\"" + content + "\""           
                cursor.execute(f"""
        SELECT id,
               srank,
               A.title,
               heat,
               tag,
               href,
               B.datetime_earliest datetime_earliest,
               B.datetime_latest datetime_latest
        FROM api_realtimehot A,
             (SELECT title, MIN(datetime), MAX(datetime)
              FROM api_realtimehot
              WHERE match(title) against({content_match} in boolean mode)
              GROUP BY title)
                 AS B(title, datetime_earliest, datetime_latest)
        WHERE A.datetime = B.datetime_earliest and match(A.title) against({content_match} in boolean mode)
          AND A.title = B.title AND tag <> '荐';
            """)
            all = []
            for item in cursor.fetchall():
                all.append({
                    "id": item[0],
                    "srank": item[1],
                    "title": item[2],
                    "heat": item[3],
                    "tag": item[4],
                    "href": "https://s.weibo.com" + item[5],
                    "datetime_earliest": item[6].strftime("%Y-%m-%d %H:%M:%S"),
                    "datetime_latest": item[7].strftime("%Y-%m-%d %H:%M:%S")
                })
            cursor.close()
            conn.close()
            if all:
                if method == "precise":
                    echarts_data = json.loads(
                        serializers.serialize('json', models.realtimehot.objects.filter(title__exact=all[0]['title'])))
                    x_data = []
                    y_srank_data = []
                    y_heat_data = []
                    for item in echarts_data:
                        old_href = item['fields']['href']
                        item['fields']['href'] = "https://s.weibo.com" + old_href
                        x_data.append(item['fields']['datetime'])
                        y_srank_data.append(item['fields']['srank'])
                        y_heat_data.append(item['fields']['heat'] if item['fields']['heat'] else 0)
                    x_data = [_.replace("T", "   ") for _ in x_data]
                    y_heat_data = [int(_) for _ in y_heat_data]
                    if sum(y_srank_data) == 0 and sum(y_heat_data) == 0:
                        flag_top_or_not = "true"
                        return render(request, 'realtimehot_search_by_content.html', locals())
                    data_date_heat = []
                    data_date_srank = []
                    for i in range(len(x_data)):
                        data_date_heat.append([x_data[i], y_heat_data[i]])
                        data_date_srank.append([x_data[i], y_srank_data[i]])

                    title_text = content.encode("unicode_escape").decode()
                    title_subtext = "历史排行".encode("unicode_escape").decode()
                    name_srank = "排名".encode("unicode_escape").decode()
                    name_heat = "热度".encode("unicode_escape").decode()

            paginator = Paginator(all, 50)
            result_num = len(all)
            tail_page = paginator.num_pages
            tail_page_ellipsis = tail_page - 4

            try:
                current_num = request.GET.get('page', "1")
                if current_num.isnumeric():
                    pass
                else:
                    current_num = 1

                all = paginator.page(current_num)
                if tail_page > 11:
                    if current_num - 5 < 1:
                        page_range = range(1, 11)
                    elif current_num + 5 > tail_page:
                        page_range = range(tail_page - 9, tail_page + 1)
                    else:
                        page_range = range(current_num - 5, current_num + 5)
                else:
                    page_range = paginator.page_range
                return render(request, 'realtimehot_search_by_content.html', locals())
            except EmptyPage:
                error_page = request.GET.get('page')
                if error_page.isnumeric():
                    if int(error_page) < 1:
                        return redirect(request.path + "?&token=" + token_s + "&page=1")
                    elif int(error_page) > int(tail_page):
                        return redirect(request.path + "?&token=" + token_s + "&page=" + str(tail_page))
                else:
                    return redirect(request.path + "?&token=" + token_s + "&page=1")
        except TypeError:
            return redirect(request.path + "?&token=" + token_s + "&page=1")


class NotFound(View):
    def get(self, request):
        return render(request, '404.html')
