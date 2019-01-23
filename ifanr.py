# -*- coding:utf-8 -*-
from __future__ import print_function
import urllib
from bs4 import BeautifulSoup
import pymysql
import contextlib
import operator
import schedule
import time
import datetime

localhost = '127.0.0.1'
tencenthost = '140.143.197.154'


@contextlib.contextmanager
def mysql(host=localhost, port=3306, user='root', passwd='root', db='flowreader', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def getIfanr():
    res = urllib.request.urlopen("http://www.ifanr.com")

    soup = BeautifulSoup(res, "html.parser", from_encoding="utf-8")

    for _ in soup.findAll("div", "article-item--list"):
        post = _
        author_info = post.find("div", "author-info")
        channel = post.find("a", "article-label").text
        title = post.find("h3").text
        summary = post.find("div", "article-summary").text
        article_link = post.find("a", "article-link").attrs['href']
        channel_link = post.find("a", "article-label").attrs['href']
        img = post.find("div", "article-image").attrs['style']
        author = author_info.find("span", "author-name").text
        author_avatar = author_info.find("img").attrs['src']
        posttime = timeformat(post.find("time").text)
        platform = "ifanr"
        postid = article_link.split('/')[len(article_link.split('/')) - 1]
        img = img.split("'")[1].split("!")[0]

        if (operator.eq(channel, "小程序")):
            continue

        insertToDB(title, summary, img, article_link, platform, channel, channel_link, author, author_avatar, posttime,
                   postid)

        print("channel:" + channel)
        print("title:" + title)
        print("summary:" + summary)
        print("article-link:" + article_link)
        print("channel-link:" + channel_link)
        print("img:" + img)
        print("author:" + author)
        print("author-avatar:" + author_avatar)
        print("time:" + str(post.find("time").text))
        print("postid:" + postid)
        print("--------")


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
        cursor.execute("select postid from post where platform = 'ifanr'")
        ids = cursor.fetchall()

    for id in ids:
        if (int(postid) == id['postid']):
            return False
    return True


def timeformat(str):
    strs = str.split(" ")
    now = time.time()

    if (operator.eq(str, "刚刚")):
        timest = now
    elif (operator.eq(strs[1], "分钟前")):
        minutes = strs[0]
        timest = now - int(minutes) * 60
    elif (operator.eq(strs[1], "小时前")):
        hours = strs[0]
        timest = now - int(hours) * 60 * 60
    elif (operator.eq(strs[1], "天前")):
        days = strs[0]
        timest = now - int(days) * 60 * 60 * 24
    elif (operator.eq(str[0], "昨天")):
        timest = now - 60 * 60 * 24
    elif (operator.eq(str[0], "前天")):
        timest = now - 60 * 60 * 24 * 2
    else:
        timest = 0

    return datetime.datetime.fromtimestamp(timest)


def timing():
    schedule.every(6).seconds.do(getIfanr)
    while True:
        schedule.run_pending()
        time.sleep(1)


class Ifanr:
    def doJob(self):
        timing()


if __name__ == '__main__':
    Ifanr().doJob()
