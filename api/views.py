import time
from pyecharts.charts import WordCloud, Map, Geo
from django.db.models import Sum
from lxml import etree
import requests
from django.views import View
from Crypto.Cipher import AES
import base64
from django.utils.decorators import method_decorator
import datetime
from home.views import loginORnot
from api import models
from django.core import serializers
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from pyecharts import options as opts
from pyecharts.globals import ChartType


class RealTimeHotGetResultForHome(APIView):
    def get(self, request):
        response = requests.get(url="https://s.weibo.com/top/summary?cate=realtimehot",
                                headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
                                })
        response = etree.HTML(response.text)
        lists = []
        for res in response.xpath("//tbody/tr"):
            item = {}
            srank = res.xpath("td[1]/text()") if res.xpath("td[1]/text()") else 0
            title = res.xpath("td[2]/a/text()")[0]
            heat = res.xpath("td[2]/span/text()")[0] if res.xpath("td[2]/span/text()") else ''
            tag = res.xpath("td[3]/i/text()")[0] if res.xpath("td[3]/i/text()") else ''
            href = res.xpath("td[2]/a/@href")[0] if res.xpath(
                "td[2]/a/@href")[0] != "javascript:void(0);" else res.xpath(
                "td[2]/a/@href_to")[0]
            item['srank'] = srank
            item['title'] = title
            item['heat'] = heat
            item['tag'] = tag
            item['href'] = "https://s.weibo.com/" + href
            item['datetime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if tag == '荐':
                del item['title']
                del item['heat']
                del item['href']
            else:
                pass
            lists.append(item)
        return JsonResponse(json.dumps(lists, ensure_ascii=False))


class SocialEventGetResultForHome(APIView):
    def get(self, request):
        response = requests.get(url="https://s.weibo.com/top/summary?cate=socialevent",
                                headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
                                })
        response = etree.HTML(response.text)
        lists = []
        for res in response.xpath("//tbody/tr"):
            item = {}
            title = res.xpath("td[2]/a/text()")[0]
            href = res.xpath("td[2]/a/@href")[0] if res.xpath(
                "td[2]/a/@href")[0] != "javascript:void(0);" else res.xpath(
                "td[2]/a/@href_to")[0]
            item['title'] = title
            item['href'] = "https://s.weibo.com/" + href
            item['datetime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            lists.append(item)
        return JsonResponse(json.dumps(lists, ensure_ascii=False))


def aesDecrypt(key, data):
    """
    AES的ECB模式解密方法
    :param key: 密钥
    :param data: 加密后的数据（密文）
    :return:明文
    前端加密，后端解密
    """
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    key = key.encode('utf8')
    data = base64.b64decode(data)
    cipher = AES.new(key, AES.MODE_ECB)

    text_decrypted = unpad(cipher.decrypt(data))
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted


class RealTimeHotSearchByTime(APIView):
    @method_decorator(loginORnot)
    def post(self, request):
        dummy_year = request.POST.get("year")
        dummy_month = request.POST.get("month")
        dummy_day = request.POST.get("day")
        dummy_hour = request.POST.get("hour")
        dummy_minute = request.POST.get("minute")
        really_time = aesDecrypt('sleepy_youngF**K', request.POST.get("random"))
        year = really_time[:4]
        month = really_time[4:6]
        day = really_time[6:8]
        hour = really_time[8:10]
        minute = really_time[10:]
        if year == dummy_year and month == dummy_month and day == dummy_day and hour == dummy_hour and minute == dummy_minute:
            pass
        else:  # 对面会返回 500
            year = dummy_year
            month = dummy_month
            day = dummy_day
            hour = dummy_hour
            minute = dummy_minute

        all = json.loads(serializers.serialize("json", models.realtimehot.objects.filter(
            datetime__hour=hour,
            datetime__day=day,
            datetime__minute=minute,
            datetime__month=month,
            datetime__year=year
        )))
        lists = []
        for item in json.loads((json.dumps(all, ensure_ascii=False))):
            lists.append(dict({
                "srank": item["fields"]["srank"],
                "title": item["fields"]["title"],
                "heat": item["fields"]["heat"],
                "tag": item["fields"]["tag"],
                "href": "https://s.weibo.com" + item["fields"]["href"],
                "datetime": str(item["fields"]["datetime"]).replace("T", " "),
            }))
        return JsonResponse(json.dumps(lists, ensure_ascii=False))


# ---------------------------------------------------------------------------------------------
def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error


class RealTimeHotWordCloud(APIView):
    def get(self, request, *args, **kwargs):
        now = datetime.datetime(int(time.strftime("%Y", time.localtime(time.time()))),
                                int(time.strftime("%m", time.localtime(time.time()))),
                                int(time.strftime("%d", time.localtime(time.time()))))
        all = models.realtimehot.objects.filter(datetime__gte=now).values("title").annotate(heats=Sum("heat"))
        lists = []
        for item in all:
            if item['title'] != '':
                lists.append((item['title'], item['heats']))
        wc = (
            WordCloud(
                init_opts=opts.InitOpts()
            )
                .add(series_name="", data_pair=lists,
                     width="auto", height="100%",
                     is_draw_out_of_bound=True
                     )
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
                ),
                tooltip_opts=opts.TooltipOpts(is_show=True),
            )
                .dump_options_with_quotes()
        )
        return JsonResponse(json.loads(wc))


class LastWeekProvinces(APIView):
    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        week = now - datetime.timedelta(days=7)
        week_ago = datetime.datetime(week.year, week.month, week.day, week.hour, week.minute)
        lists = []
        for i in list(models.realtimehot.objects.filter(datetime__gte=week_ago, datetime__lte=now).distinct().values(
                "title")):
            lists.append(i["title"])
        provinces_dict = {'黑龙江': 0, '上海': 0, '内蒙古': 0, '吉林': 0, '辽宁': 0, '河北': 0, '天津': 0, '山西': 0,
                          '陕西': 0, '甘肃': 0, '宁夏': 0, '青海': 0, '新疆': 0, '西藏': 0, '四川': 0, '重庆': 0,
                          '山东': 0, '河南': 0, '江苏': 0, '安徽': 0, '湖北': 0, '浙江': 0, '福建': 0, '江西': 0, '湖南': 0,
                          '贵州': 0, '广西': 0, '海南': 0, '广东': 0, '北京': 0, '云南': 0, '香港': 0, '澳门': 0, '台湾': 0}
        provinces_list = list(provinces_dict.keys())
        for i in lists:
            for j in provinces_list:
                if j in i:
                    provinces_dict[j] += 1

        china_provinces = (
            Map(init_opts=opts.InitOpts())
                .add("", [list(z) for z in zip(provinces_list, list(provinces_dict.values()))], "china",
                     is_map_symbol_show=False,
                     zoom=1.2)
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                tooltip_opts=opts.TooltipOpts(
                    trigger="item", formatter="{b} : {c}次"
                ),
                visualmap_opts=opts.VisualMapOpts(
                    min_=0,
                    max_=10,
                    # range_text=["High", "Low"],
                    is_calculable=True,
                    range_color=["white", "lightskyblue", "yellow", "orangered"],
                ),
            )
                .dump_options_with_quotes()
        )

        return JsonResponse(json.loads(china_provinces))


class LastWeekCities(APIView):
    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        week = now - datetime.timedelta(days=7)
        week_ago = datetime.datetime(week.year, week.month, week.day, week.hour, week.minute)
        lists = []
        for i in list(models.realtimehot.objects.filter(datetime__gte=week_ago, datetime__lte=now).distinct().values(
                "title")):
            lists.append(i["title"])
        cities_list = [
            '津市', '北京', '天津', '石家庄', '辛集', '藁城', '晋州', '新乐', '鹿泉', '唐山', '遵化', '迁安', '秦皇岛', '邯郸', '武安', '邢台',
            '南宫', '沙河', '保定', '涿州', '定州', '安国', '高碑店', '张家口', '承德', '沧州', '泊头', '任丘', '黄骅', '河间', '廊坊', '霸州',
            '三河', '衡水', '冀州', '深州', '太原', '古交', '大同', '阳泉', '长治', '潞城', '晋城', '高平', '朔州', '晋中', '介休', '运城',
            '河津', '忻州', '原平', '临汾', '侯马', '霍州', '吕梁', '孝义', '汾阳', '呼和浩特', '包头', '乌海', '赤峰', '通辽', '霍林郭勒',
            '鄂尔多斯', '呼伦贝尔', '满洲里', '牙克石', '扎兰屯', '额尔古纳', '根河', '巴彦淖尔', '乌兰察布', '丰镇', '乌兰浩特', '阿尔山', '二连浩特',
            '锡林浩特', '沈阳', '新民', '大连', '瓦房店', '普兰店', '庄河', '鞍山', '海城', '抚顺', '本溪', '丹东', '东港', '凤城', '锦州',
            '凌海', '营口', '盖州', '大石桥', '阜新', '辽阳', '灯塔', '盘锦', '铁岭', '调兵山', '开原', '朝阳', '北票', '凌源', '葫芦岛',
            '兴城', '长春', '九台', '榆树', '德惠', '吉林', '蛟河', '桦甸', '舒兰', '磐石', '四平', '公主岭', '双辽', '辽源', '通化', '梅河口',
            '集安', '白山', '临江', '松原', '白城', '洮南', '大安', '延吉', '图们', '敦化', '珲春', '龙井', '和龙', '哈尔滨', '双城', '尚志',
            '五常', '齐齐哈尔', '讷河', '鸡西', '虎林', '密山', '鹤岗', '双鸭山', '大庆', '伊春', '铁力', '佳木斯', '同江', '富锦', '七台河',
            '牡丹江', '绥芬河', '海林', '宁安', '穆棱', '黑河', '北安', '五大连池', '绥化', '安达', '肇东', '海伦', '上海', '南京', '无锡',
            '江阴', '宜兴', '徐州', '新沂', '邳州', '常州', '溧阳', '金坛', '苏州', '常熟', '张家港', '昆山', '吴江', '太仓', '南通', '启东',
            '如皋', '通州', '海门', '连云港', '淮安', '盐城', '东台', '大丰', '扬州', '仪征', '高邮', '江都', '镇江', '丹阳', '扬中', '句容',
            '泰州', '兴化', '靖江', '泰兴', '姜堰', '宿迁', '杭州', '建德', '富阳', '临安', '宁波', '余姚', '慈溪', '奉化', '温州', '瑞安',
            '乐清', '嘉兴', '海宁', '平湖', '桐乡', '湖州', '绍兴', '诸暨', '上虞', '嵊州', '金华', '兰溪', '义乌', '东阳', '永康', '衢州',
            '江山', '舟山', '台州', '温岭', '临海', '丽水', '龙泉', '合肥', '芜湖', '蚌埠', '淮南', '马鞍山', '淮北', '铜陵', '安庆', '桐城',
            '黄山', '滁州', '天长', '明光', '阜阳', '宿州', '巢湖', '六安', '亳州', '池州', '宣城', '宁国', '福州', '福清', '长乐', '厦门',
            '莆田', '三明', '永安', '泉州', '石狮', '晋江', '南安', '漳州', '龙海', '南平', '邵武', '武夷山', '建瓯', '建阳', '龙岩', '漳平',
            '宁德', '福安', '福鼎', '南昌', '景德镇', '乐平', '萍乡', '九江', '瑞昌', '新余', '鹰潭', '贵溪', '赣州', '瑞金', '南康', '吉安',
            '井冈山', '宜春', '丰城', '樟树', '高安', '抚州', '上饶', '德兴', '济南', '章丘', '青岛', '胶州', '即墨', '平度', '胶南', '莱西',
            '淄博', '枣庄', '滕州', '东营', '烟台', '龙口', '莱阳', '莱州', '蓬莱', '招远', '栖霞', '海阳', '潍坊', '青州', '诸城', '寿光',
            '安丘', '高密', '昌邑', '济宁', '曲阜', '兖州', '邹城', '泰安', '新泰', '肥城', '威海', '文登', '荣成', '乳山', '日照', '莱芜',
            '临沂', '德州', '乐陵', '禹城', '聊城', '临清', '滨州', '郑州', '巩义', '荥阳', '新密', '新郑', '登封', '开封', '洛阳', '偃师',
            '平顶山', '舞钢', '汝州', '安阳', '林州', '鹤壁', '新乡', '卫辉', '辉县', '焦作', '济源', '沁阳', '孟州', '濮阳', '许昌', '禹州',
            '长葛', '漯河', '三门峡', '义马', '灵宝', '南阳', '邓州', '商丘', '永城', '信阳', '周口', '项城', '驻马店', '武汉', '黄石', '大冶',
            '十堰', '丹江口', '宜昌', '宜都', '当阳', '枝江', '襄樊', '老河口', '枣阳', '宜城', '鄂州', '荆门', '钟祥', '孝感', '应城', '安陆',
            '汉川', '荆州', '石首', '洪湖', '松滋', '黄冈', '麻城', '武穴', '咸宁', '赤壁', '随州', '广水', '恩施', '利川', '仙桃', '潜江',
            '天门', '长沙', '浏阳', '株洲', '醴陵', '湘潭', '湘乡', '韶山', '衡阳', '耒阳', '常宁', '邵阳', '武冈', '岳阳', '汨罗', '临湘',
            '常德', '津市', '张家界', '益阳', '沅江', '郴州', '资兴', '永州', '怀化', '洪江', '娄底', '冷水江', '涟源', '吉首', '广州', '增城',
            '从化', '韶关', '乐昌', '南雄', '深圳', '珠海', '汕头', '佛山', '江门', '台山', '开平', '鹤山', '恩平', '湛江', '廉江', '雷州',
            '吴川', '茂名', '高州', '化州', '信宜', '肇庆', '高要', '四会', '惠州', '梅州', '兴宁', '汕尾', '陆丰', '河源', '阳江', '阳春',
            '清远', '英德', '连州', '东莞', '中山', '潮州', '揭阳', '普宁', '云浮', '罗定', '南宁', '柳州', '桂林', '梧州', '岑溪', '北海',
            '防城港', '东兴', '钦州', '贵港', '桂平', '玉林', '北流', '百色', '贺州', '河池', '宜州', '来宾', '合山', '崇左', '凭祥', '海口',
            '三亚', '五指山', '琼海', '儋州', '文昌', '万宁', '东方', '重庆', '成都', '都江堰', '彭州', '邛崃', '崇州', '自贡', '攀枝花',
            '泸州', '德阳', '广汉', '什邡', '绵竹', '绵阳', '江油', '广元', '遂宁', '内江', '乐山', '峨眉山', '南充', '阆中', '眉山', '宜宾',
            '广安', '华蓥', '达州', '万源', '雅安', '巴中', '资阳', '简阳', '西昌', '贵阳', '清镇', '六盘水', '遵义', '赤水', '仁怀', '安顺',
            '铜仁', '兴义', '毕节', '凯里', '都匀', '福泉', '昆明', '安宁', '曲靖', '宣威', '玉溪', '保山', '昭通', '丽江', '临沧', '楚雄',
            '个旧', '开远', '景洪', '大理', '瑞丽', '潞西', '拉萨', '日喀则', '西安', '铜川', '宝鸡', '咸阳', '兴平', '渭南', '韩城', '华阴',
            '延安', '汉中', '榆林', '安康', '商洛', '兰州', '嘉峪关', '金昌', '白银', '天水', '武威', '张掖', '平凉', '酒泉', '玉门', '敦煌',
            '庆阳', '定西', '陇南', '临夏', '合作', '西宁', '格尔木', '德令哈', '银川', '灵武', '石嘴山', '吴忠', '青铜峡', '固原', '中卫',
            '乌鲁木齐', '克拉玛依', '吐鲁番', '哈密', '昌吉', '阜康', '米泉', '博乐', '库尔勒', '阿克苏', '阿图什', '喀什', '和田', '伊宁', '奎屯',
            '塔城', '乌苏', '阿勒泰', '石河子', '阿拉尔', '图木舒克', '五家渠', '台北', '高雄', '基隆', '台中', '台南', '新竹', '嘉义', '香港',
            '澳门']
        cities_dict = {}
        for i in lists:
            for j in cities_list:
                if j in i:
                    frequency = cities_dict.get(j, 0)
                    cities_dict[j] = frequency + 1
        china_cities = (
            Geo(init_opts=opts.InitOpts())
                .add_schema(maptype="china", zoom=1.2)
                .add("",
                     [list(z) for z in zip(list(cities_dict.keys()), list(cities_dict.values()))],
                     type_=ChartType.EFFECT_SCATTER, effect_opts=opts.EffectOpts(is_show=True,
                                                                                 symbol_size=30, scale=4, period=5)
                     )

                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(
                    min_=0,
                    max_=10,
                    # range_text=["High", "Low"],
                    is_calculable=True,
                    range_color=["lightskyblue", "orangered"],
                ),

                tooltip_opts=opts.TooltipOpts(
                    is_show=True,
                    trigger="item",
                    formatter="{b} : {c}次"
                ),
            )
                .dump_options_with_quotes()
        )

        return JsonResponse(json.loads(china_cities))
