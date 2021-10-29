from django.shortcuts import render
from django.http import HttpResponse
from .utils_abc import get_c1_data, get_c2_data, get_r1_data, get_r2_data, get_l1_data, get_l2_data
import json
import time
from jieba.analyse import extract_tags


# Create your views here.

def index(requsts):
    context = {'a': 'test'}
    return render(requsts, 'index.html', context)


def hello(requsts):
    return HttpResponse("Hello kobe!")


def main(requsts):
    return render(requsts, 'main.html')


'''
ajax交互流程：从main.html执行controlller.js，调用函数，匹配url，再调用url对应的函数，返回数据展示数据
'''


def time_get(requsts):
    time_str = time.strftime("%Y{}%m{}%d{}%X")
    return HttpResponse(time_str.format("年", "月", "日"))  # 格式化函数将年月日带入上面的{}


def get_c1(request):
    data = get_c1_data()
    return HttpResponse(
        json.dumps({"confirm": str(data[0]), "suspect": str(data[1]), "heal": str(data[2]), "dead": str(data[3])}))


def get_c2(request):
    res = []
    for tup in get_c2_data():
        print(tup)
        res.append({"name": tup[0], "value": int(tup[1])})
    return HttpResponse(json.dumps({"data": res}))


def get_r1(request):
    data = get_r1_data()
    city, confirm = [], []
    for a, b in data:
        if a != "地区待确认" and a != "境外输入":
            city.append(a)
            confirm.append(int(b))

    return HttpResponse(json.dumps({"city": city[0:5], "confirm": confirm[0:5]}))  # 只获取前五条


def get_r2(requests):
    data = get_r2_data()
    d = []
    for i in data:
        k = i[0]
        ks = extract_tags(k)
        for j in ks:
            d.append({"name":j, "value":11})    #echats用到的数据是字典，必须得加上value值
    return HttpResponse(json.dumps(({'kws': d})))


def get_l1(request):  # 必须加参数
    data = get_l1_data()
    day, confirm, suspect, heal, dead = [], [], [], [], []
    for a, b, c, d, e in data:
        day.append(a.strftime("%m-%d"))
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    # 从倒数一百提取到底

    return HttpResponse(
        json.dumps({"day": day[-100:], "confirm": confirm[-100:], "suspect": suspect[-100:], "heal": heal[-100:],
                    "dead": dead[-100:]}))


def get_l2(request):
    data = get_l2_data()
    day, confirm_add, suspect_add, heal_add, dead_add = [], [], [], [], []
    for a, b, c, d, e in data:
        day.append(a.strftime("%m-%d"))
        confirm_add.append(b)
        suspect_add.append(c)
        heal_add.append(d)
        dead_add.append(e)

    return HttpResponse(
        json.dumps({"day": day[-100:], "confirm_add": confirm_add[-100:], "suspect_add": suspect_add[-100:],
                    "heal_add": heal_add[-100:], "dead_add": dead_add[-100:]}))
