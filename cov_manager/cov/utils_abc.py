import pymysql

def get_conn():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        db="cov_django",
        charset="utf8",
        port=3306,
    )
    # 创建游标：
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def query(sql, *args):
    '''
    :param sql:
    :param args:
    :return:返回结果，((),())形式
    '''
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()  # 获取结果,返回元组
    close_conn(conn, cursor)
    return res


def get_c1_data():
    sql = "select sum(confirm), (select suspect from cov_history order by ds desc limit 1)," \
          "sum(heal),sum(dead) from cov_details " \
          "where update_time=(select update_time from cov_details order by update_time desc limit 1)"
    res = query(sql)
    #print(res[0])
    return res[0]   #获取到的元组有多个，只需返回一个


def get_c2_data():
    # sql = "select province,sum(confirm) from details where update_time=(select update_time from details" \
    #       "order by update_time desc limit 1) group by province"
    # res = query(sql)
    # return res

    sql = "select province,sum(confirm) from cov_details " \
          "where update_time=(select update_time from cov_details " \
          "order by update_time desc limit 1) " \
          "group by province"

    res = query(sql)
    #print(res)
    return res


def get_l1_data():
    sql = "select ds,confirm,suspect,heal,dead from cov_history"
    res = query(sql)
    return res


def get_l2_data():
    sql = "select ds,confirm_add,suspect_add,heal_add,dead_add from cov_history"
    res = query(sql)
    return res


def get_r1_data():
    # union_all 两块相加
    sql = 'SELECT city,confirm FROM ' \
          '(select city,confirm from cov_details  ' \
          'where update_time=(select update_time from cov_details order by update_time desc limit 1) ' \
          'and province not in ("湖北","北京","上海","天津","重庆") ' \
          'union all ' \
          'select province as city,sum(confirm) as confirm from cov_details  ' \
          'where update_time=(select update_time from cov_details order by update_time desc limit 1) ' \
          'and province in ("北京","上海","天津","重庆") group by province) as a ' \
          'ORDER BY confirm DESC limit 100'

    res = query(sql)
    return res


def get_r2_data():
    sql = "select content from baidu_hot order by id"

    res = query(sql)
    return res


if __name__ == '__main__':
    # print(get_r1_data())
    print(get_r2_data())
    pass
