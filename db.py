import pymysql
import config


def checklogin(user, pwd):
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = 'SELECT passwd FROM user WHERE uname="' + user + '"'
    cursor.execute(sql)
    a = cursor.fetchone()
    if a is None:
        print("用户不存在！")
        return 2
    else:
        if a[0] != pwd:
            print("密码错误！")
            return 1
        else:
            print("成功登录！")
            return 0


def register(user, pwd):
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = 'INSERT INTO user SET uname="' + user + '", passwd="' + pwd + '";'
    cursor.execute(sql)
    sql2 = 'INSERT INTO score SET uname="' + user + '", achieved_time=NOW(), highest_score=0;' 
    cursor.execute(sql2)
    db.commit()


def getHighestScore(user):
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = 'SELECT highest_score FROM score WHERE uname="' + user + '";'
    cursor.execute(sql)
    score = cursor.fetchone()[0]
    return score


def updateHighestScore(user, score):
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = 'UPDATE score SET highest_score=' + str(score) + ', achieved_time=NOW() WHERE uname="' + user + '";'
    cursor.execute(sql)
    db.commit()


def getHighestScTime(user):
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = 'SELECT achieved_time FROM score WHERE uname="' + user + '";'
    cursor.execute(sql)
    return cursor.fetchone()[0]


def dbGetLeaderBoardData():
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = 'SELECT id, uname, highest_score, achieved_time FROM score ORDER BY highest_score DESC'
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


def dbGetLeaderBoardMyData(uname):
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = 'SELECT id, uname, highest_score, achieved_time FROM score WHERE uname="' + uname + '";'
    cursor.execute(sql)
    data = cursor.fetchone()
    return data
