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


# 根据豆瓣电影的id获取一张该电影高清海报的url
def getDoubanImg(movieId):
    res = urllib.request.urlopen("https://movie.douban.com/subject/" + movieId + "/photos?type=R")

    soup = BeautifulSoup(res, "html.parser", from_encoding="utf-8")

    allImg = soup.find("ul", "poster-col3 clearfix")
    imgList = allImg.findAll("li")

    # 第一张海报
    firstImgId = imgList[0].attrs['data-id']
    print("https://img1.doubanio.com/view/photo/l/public/p" + firstImgId + ".jpg")

    # 所有海报
    for img in imgList:
        imgId = img.attrs['data-id']
        print("https://img1.doubanio.com/view/photo/l/public/p" + imgId + ".jpg")


if __name__ == '__main__':
    getDoubanImg("1305690")
