# @Version: python3.10
# @Time: 2024/1/6 10:44
# @Author: PlutoCtx
# @Email: 15905898514@163.com
# @File: fetch_column_urls.py
# @Software: PyCharm
# @User: chent

import requests
import json
import csv

def getGZHJson(appid, secret):
    path = " https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential"
    url = path + "&appid=" + appid + "&secret=" + secret
    result = requests.get(url)
    token = json.loads(result.text)
    access_token = token['access_token']
    data = {
        "type": "news",
        "offset": 0,
        "count": 1,
    }
    headers = {
        'content-type': "application/json",
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=' + access_token
    result = requests.post(url=url, data=json.dumps(data), headers=headers)
    result.encoding = result.apparent_encoding
    result = json.loads(result.text)
    count = int(result['total_count'])
    gzh_dict = {"news_item": []}
    for i in range(0, count):
        data['offset'] = i
        result = requests.post(url=url, data=json.dumps(data), headers=headers)
        result.encoding = result.apparent_encoding
        result = json.loads(result.text)
        for item in result['item'][0]['content']['news_item']:
            temp_dict = {}
            temp_dict['title'] = item["title"]
            temp_dict['digest'] = item["digest"]
            temp_dict['url'] = item["url"]
            temp_dict['thumb_url'] = item["thumb_url"]
            print(temp_dict)
            gzh_dict['news_item'].append(temp_dict)
    return json.dumps(gzh_dict)



if __name__ == '__main__':
    getGZHJson('开发者ID', '开发者密码')
