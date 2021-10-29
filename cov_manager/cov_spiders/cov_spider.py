import urllib.request as rq
import json
import time
import pymysql
import traceback

url_last = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
url_today = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"


def get_url(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3877.400 QQBrowser/10.8.4506.400"}
    req = rq.Request(url, headers=headers)
    res = rq.urlopen(req)
    html = res.read().decode("utf-8")
    return html


def get_tencent_data(url_last, url_today):
    html_last = get_url(url_last)
    data_last = json.loads(html_last)
    data_last = json.loads(data_last["data"])

    html_today = get_url(url_today)
    data_today = json.loads(html_today)
    data_today = json.loads(data_today["data"])
    # print(data_last.keys())

    history_data = {}
    for i in data_last["chinaDayList"]:
        ds = "2021." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i['dead']
        history_data[ds] = {"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead}

    # for i in data_last["chinaDayAddList"]:
    #     ds_data = "2021" + i["date"]
    #     tup_data = time.strptime(ds_data, "%Y,%m,%d")
    #     ds_data = time.strftime("%Y-%m-%d", tup_data)
    #     confirm_data = i["confirm"]
    #     suspect_data = i["suspect"]
    #     heal_data = i["heal"]
    #     dead_data = i['"dead']
    #     history_data[ds_data].update({"confirm": confirm_data, "suspect": suspect_data, "heal": heal_data, "dead": dead_data})

    for i in data_last["chinaDayAddList"]:
        date_add = "2021." + i["date"]
        tup_add = time.strptime(date_add, "%Y.%m.%d")
        date_add = time.strftime("%Y-%m-%d", tup_add)  # 改变时间格式,不然插入数据库会报错，数据库是datetime类型

        confirm_add = i["confirm"]
        suspect_add = i["suspect"]
        dead_add = i["dead"]
        heal_add = i["heal"]
        # g更新，update函数可以添加新的键值对
        history_data[date_add].update(
            {"confirm_add": confirm_add, "suspect_add": suspect_add, "dead_add": dead_add, "heal_add": heal_add})

    details = []
    updata_time = data_today["lastUpdateTime"]
    data_country = data_today["areaTree"]
    data_province = data_country[0]["children"]
    for pro_infos in data_province:
        province = pro_infos["name"]
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]
            confirm = city_infos["total"]["confirm"]
            confirm_add = city_infos["today"]["confirm"]
            heal = city_infos["total"]["heal"]
            dead = city_infos["total"]["dead"]
            details.append([updata_time, province, city, confirm, confirm_add, heal, dead])
    return history_data, details


def get_conn():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        db="cov_django",
        charset="utf8",
        port=3306,
    )
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def update_details(url_last, url_today):
    cursor = None
    conn = None
    try:
        detail_data = get_tencent_data(url_last, url_today)[1]
        conn, cursor = get_conn()
        sql = "insert into cov_details(update_time,province,city,confirm,confirm_add,heal,dead) value(%s,%s,%s,%s,%s,%s,%s)"
        # sql_query = "insert %s = (select update_time from datails order by id desc limit 1)"
        sql_query = 'select %s=(select update_time from cov_details order by id desc limit 1)'
        # cursor.execute(sql_query,detail_data[0][0])
        cursor.execute(sql_query, detail_data[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新数据")
            for item in detail_data:
                cursor.execute(sql, item)
            conn.commit()
            print(f"{time.asctime()}更新最新数据完毕")
        else:
            print(f"{time.asctime()}已是最新数据")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def insert_history(url_last, url_today):
    cursor = None
    conn = None
    try:
        dic = get_tencent_data(url_last, url_today)[0]

        print(f"{time.asctime()}开始插入历史数据")
        conn, cursor = get_conn()
        sql = "insert into cov_history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for key, value in dic.items():
            # item 格式 {'2020-01-13': {'confirm': 41, 'suspect': 0, 'heal': 0, 'dead': 1}
            cursor.execute(sql, [key, value.get("confirm"), value.get("confirm_add"), value.get("suspect"),
                                 value.get("suspect_add"), value.get("heal"), value.get("heal_add"),
                                 value.get("dead"), value.get("dead_add")])
        conn.commit()  # 提交事务 update delete insert操作
        print(f"{time.asctime()}插入历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def update_history(url_last, url_today):
    cursor = None
    conn = None
    try:
        dic = get_tencent_data(url_last, url_today)[0]
        print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = get_conn()
        sql = "insert into cov_history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from cov_history where ds=%s"
        for key, value in dic.items():
            # item 格式 {'2020-01-13': {'confirm': 41, 'suspect': 0, 'heal': 0, 'dead': 1}
            if not cursor.execute(sql_query, key):
                cursor.execute(sql, [key, value.get("confirm"), value.get("confirm_add"), value.get("suspect"),
                                     value.get("suspect_add"), value.get("heal"), value.get("heal_add"),
                                     value.get("dead"), value.get("dead_add")])
        conn.commit()
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


if __name__ == '__main__':
    # get_tencent_data(url_last)
    update_details(url_last, url_today)
    update_history(url_last, url_today)
