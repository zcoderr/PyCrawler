from __future__ import print_function
import json
import requests
import pymysql
import contextlib
import operator
import datetime
import time
import schedule
from ifanr import Ifanr

localhost = '127.0.0.1'
tencenthost = '140.143.197.154'


@contextlib.contextmanager
def mysql(host=Constants.mysql_localhost, port=3306, user=Constants.mysql_user, passwd=Constants.mysql_passwd,
          db=Constants.mysql_db_name, charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def getSSPai():
    res = requests.get(
        "https://sspai.com/api/v1/articles?offset=0&limit=20&type=recommend_to_home&sort=recommend_to_home_at&include_total=false")

    list = json.loads(res.text)
    for post in list["list"]:
        title = post["title"]
        summary = post["promote_intro"]
        img = "https://cdn.sspai.com/" + post["banner"]
        article_link = "https://sspai.com/" + "post/" + str(post["id"])
        platform = "sspai"
        author = post["author"]["nickname"]
        author_avatar = "https://cdn.sspai.com/" + post["author"]["avatar"]
        posttime = datetime.datetime.fromtimestamp(post["released_at"])
        postid = post["id"]
        insertToDB(title, summary, img, article_link, platform, "null", "null", author, author_avatar, posttime,
                   postid)

        print("文章id:" + str(postid))
        print("title:" + title)
        print("summary:" + summary)
        print("img:" + img)
        print("article_link:" + article_link)
        print("posttime:" + str(posttime))
        print("author:" + author)
        print("avatar:" + author_avatar)
        print("----------")


def insertToDB(title, summary, img, article_link, platform, channel, channel_link, author, author_avatar, posttime,
               postid):
    if (filter(postid)):
        with mysql() as cursor:
            cursor.executemany(
                "insert into post(title,summary,img,article_link,platform,channel,channel_link,author,author_avatar,posttime,postid)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                [(title, summary, img, article_link, platform, channel, channel_link, author, author_avatar, posttime,
                  postid)])


def filter(postid):
    with mysql() as cursor:
        cursor.execute("select postid from post where platform = 'sspai'")
        ids = cursor.fetchall()

    for id in ids:
        if (int(postid) == id['postid']):
            return False
    return True


def timeformat(str):
    now = time.time()

    if (operator.eq(str, "刚刚")):
        timest = now
    elif (operator.eq(str[-3], "分")):
        minutes = str.split("分")[0]
        timest = now - int(minutes) * 60
    elif (operator.eq(str[-2], "时")):
        hours = str.split("小")[0]
        timest = now - int(hours) * 60 * 60
    elif (operator.eq(str[-2], "天")):
        days = str.split("天")[0]
        timest = now - int(days) * 60 * 60 * 24
    elif (operator.eq(str[0], "昨天")):
        timest = now - 60 * 60 * 24
    elif (operator.eq(str[0], "前天")):
        timest = now - 60 * 60 * 24 * 2
    else:
        timest = 0

    return datetime.datetime.fromtimestamp(timest)


def timing():
    schedule.every(6).seconds.do(getSSPai)
    while True:
        schedule.run_pending()
        time.sleep(1)


class SSPai:
    def doJob(self):
        timing()


if __name__ == '__main__':
    SSPai().doJob()
