#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup
import json

__author__ = 'johnny'
__email__ = 'zhaozy93@outlook.com'

#用于抓取歌单中每首歌的id，以便下一步抓取每首歌的相信信息

def get_html(url, use_cookie, request_type='GET', data=None, headers={}):
    request = ''
    if headers == {}:
        print '重置header'
        # 如果开启编码支持 返回来的是乱码，需要解码
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Upgrade - Insecure - Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',

        }
    if not use_cookie:
        # 设置保存cookie的文件，同级目录下的cookie.txt
        filename = 'cookie.txt'
        # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
        cookie = cookielib.MozillaCookieJar(filename)
    else:
        cookie = cookielib.MozillaCookieJar()
        # Cookie已经存在，读取cookie
        cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    handler = urllib2.HTTPCookieProcessor(cookie)
    # 通过handler来构建opener
    opener = urllib2.build_opener(handler)
    if request_type == 'GET':
        print 'GET请求'
        general_url = url
        if data:
            general_url = url + '?' + urllib.urlencode(data)
        request = urllib2.Request(general_url)
        # get请求如果直接使用request(url, data, header)会自动变为post请求
        for key, value in headers.items():
            request.add_header(key, value)
    if request_type == 'POST':
        print 'POST请求'
        data = urllib.urlencode(data)
        request = urllib2.Request(url, data, headers)
    response = opener.open(request)
    # for item in cookie:
    #     print 'Name = ' + item.name,
    #     print 'Value = ' + item.value
    if not use_cookie:
        # 保存cookie到文件
        cookie.save(ignore_discard=True, ignore_expires=True)
    return response.read()

def processNode(html):
    # 整个html进行解码，方便后面正则匹配中的汉字
    # content = html.decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    trTag = soup.select('#song-list-pre-cache .f-hide')
    pattern = re.compile(r'id\=(\d+)')
    obj = {}
    for parent in trTag:
        for item in parent.descendants:
            if item.name == 'a':
                match = pattern.search(item.get('href')).group(1)
                obj[match] = item.string
    # jsObj = json.dumps(obj)
    # fileObject = open('playlist.json', 'w')
    # fileObject.write(jsObj)
    # fileObject.close()
    with open('playlist.json') as json_file:
        data = json.load(json_file)
    for item in data:
        print item, data[item]

if __name__ == '__main__':
    header = {
        'Cookie': 'you can see your token and other userinfo and put here'
    }
    try:
        html = get_html('http://music.163.com/playlist?id=152183870', False, 'GET', None, header)
        pass
    except urllib2.HTTPError, e:
        print 'HTTPError'
        print e.code
        print e
    except urllib2.URLError, e:
        print 'URLError'
        print e.reason
    else:
        processNode(html)
