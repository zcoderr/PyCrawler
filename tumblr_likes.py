# -*- coding:utf-8 -*-
from __future__ import print_function
import json
import requests
import lxml
import time
from bs4 import BeautifulSoup

authKey = "G63ym3eWUtgLP8IgyAF8bVeJoqtXBk8gOljXdkseQwuWVkSGum"
identifier = "zacharywzh"
baseUrl = "https://api.tumblr.com"



def getLikesList(offset):
    requestUrl = baseUrl + "/v2/blog/" + identifier + "/likes" + "?api_key=" + authKey + "&limit=10&offset=" + str(offset)
    print("当前请求:" + requestUrl)
    res = requests.get(requestUrl)

    jsonResult = json.loads(res.text)
    posts = jsonResult['response']['liked_posts']
    for post in posts:
        print('--||--')
        if (post['type'] == 'text'):
            try:
                print("作者：" + post['blog_name'])
                titleStr = post['summary'].split(" ")
                print("标题：" + titleStr[0])
                postSoup = BeautifulSoup(post['body'], "html.parser")
                dataStr = postSoup.figure['data-npf']

                dataJson = json.loads(dataStr)
                videoUrl = dataJson['media']['url']

                print("视频地址：" + videoUrl)
                print("------------------")
            except:
                print("-----------有异常-------------")

    # nextTimellis = jsonResult['response']['_links']['next']['query_params']['before']
    # print("时间戳：" + nextTimellis)
    # getLikesList(nextTimellis)
    offset+=10
    time.sleep(3)
    getLikesList(offset)


def parser(jsonStr):
    jsonResult = json.loads(jsonStr)
    posts = jsonResult['response']['liked_posts']
    for post in posts:
        if (post['type'] == 'text'):
            try:
                print("作者：" + post['blog_name'])
                titleStr = post['summary'].split(" ")
                print("标题：" + titleStr[0])
                postSoup = BeautifulSoup(post['body'], "html.parser")
                dataStr = postSoup.figure['data-npf']

                dataJson = json.loads(dataStr)
                videoUrl = dataJson['media']['url']

                print("视频地址：" + videoUrl)
                print("------------------")
            except:
                print("-----------有异常-------------")



if __name__ == '__main__':
    getLikesList(0)

