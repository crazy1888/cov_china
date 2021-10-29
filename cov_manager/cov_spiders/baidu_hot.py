import requests
from selenium import webdriver
import pymysql
import traceback
import time
from lxml import etree


def get_data():
    url = "https://top.baidu.com/board?tab=realtime"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3877.400 QQBrowser/10.8.4506.400"
    }

    #selenum爬取

    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # 加快爬取数据，不需要打开浏览器
    # browser = webdriver.Chrome(executable_path='D:\chromedriver\chromedriver_win32/chromedriver.exe',options=options)
    # browser.get(url)
    ## print(browser.page_source)

    # list = []
    #
    # for i in range(1, 31):
    #     c = browser.find_elements_by_xpath(
    #         '//*[@id="sanRoot"]/main/div[2]/div/div[2]/div[{}]/div[2]/a/div[1]'.format(i))
    #     list.append(c)
    #
    # list_content = []
    # for i in range(1, 31):
    #     for j in list[i - 1]:  # 将数据从0开始解析存入新列表
    #         context = j.text
    #         list_content.append(context)
    # print(list_content)
    #
    # return list_content

    #xpath解析爬取
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    # print(res.text)
    html = etree.HTML(res.text)
    items = html.xpath('//div[@class="category-wrap_iQLoo horizontal_1eKyQ"]')

    list_data =[]
    for item in items:
        list_data.append(item.xpath('.//div[@class="c-single-text-ellipsis"]/text()')[0].strip()) ##数据少直接用列表，为方便存入数据库
        #a={'title':item.xpath('.//div[@class="c-single-text-ellipsis"]/text()')[0].strip()} #数据多可以用字典，每个数据对于上设置的键，方便存储
    #print(list_data)
    return list_data

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


def updata_hot():
    cursor = None
    conn = None
    try:
        content = get_data()
        print(f"{time.asctime()}开始更新数据")  # 加f为支持引号内的python表达式，r为防转义
        conn, cursor = get_conn()
        sql = "insert into baidu_hot(dt,content) value (%s,%s)"

        ts = time.strftime("%Y-%m-%d %X")
        for i in content:
            cursor.execute(sql, (ts, i))
        conn.commit()
        print(f'{time.asctime()}数据更新完毕')
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


if __name__ == '__main__':
    get_data()
    updata_hot()
