#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
import base64
import requests
import json
import time
import os

__author__ = 'johnny'
__email__ = 'zhaozy93@outlook.com'


#根据每首歌对应的id，去调用接口轮询每首歌的热门评论
#结束后生成一个以 | 为分隔符的csv文件

headers = {
    'Cookie': 'appver=1.5.0.75771;',
    'Referer': 'http://music.163.com/'
}

first_param = "{rid:\"\", offset:\"0\", total:\"true\", limit:\"20\", csrf_token:\"\"}"
second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"


def get_params():
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


def get_json(url, params, encSecKey):
    data = {
        "params": params,
        "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    return response.content


if __name__ == "__main__":
    params = get_params();
    encSecKey = get_encSecKey();

    with open('playlist.json') as json_file:
        data = json.load(json_file)
    for item in data:
        url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + item +'?csrf_token=your token'
        json_text = get_json(url, params, encSecKey)
        json_dict = json.loads(json_text)
        fileObject = open('musiccommenttotal.csv', 'a+')
        fileObject.write(str(item).encode('utf-8') + '|' + data[item].encode('utf-8') + '|' + str(json_dict['total']).encode('utf-8') + '\r\n')
        fileObject.close()
        fileObject = open('musiccomment.csv', 'a+')
        print data[item].encode('utf-8') + '  has  '.encode('utf-8') + str(json_dict['total']).encode('utf-8') + '  comments,  and is pirnting'.encode('utf-8')
        for comment in json_dict['hotComments']:
            if comment['likedCount'] > 4000:
                commentstr = comment['content'].replace(os.linesep, ' ')
                fileObject.write(str(item).encode('utf-8') + '|' + data[item].encode('utf-8') + '|' + commentstr.encode('utf-8') + '|' + str(comment['likedCount']).encode('utf-8') + '\r\n')
        fileObject.close()
        time.sleep(3)
