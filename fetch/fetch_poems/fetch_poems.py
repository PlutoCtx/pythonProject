# @Version: python3.10
# @Time: 2024/1/17 17:22
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: fetch_poems.py
# @Software: PyCharm
# @User: chent

import requests
from lxml import etree
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    # 'referer': 'https://dytt8.net/html/gndy/dyzz/list_23_2.html'
}
BASE_DOMIN = 'https://www.gushiwen.cn/default_1.aspx'


def parse_page(url):
    response = requests.get(url, headers=headers)
    text = response.text
    titles = re.findall(r'<b>(.*?)</b>', text, flags=re.DOTALL)  # flags=re.DOTALL 来对这些 tab, new line 不敏感.
    authors = re.findall(r'<p class="source">.*?<a.*?>(.*?)</a>', text, flags=re.DOTALL)
    dynasty = re.findall(r'<p class="source">.*?<a.*?<a.*?>(.*?)</a>', text, flags=re.DOTALL)
    poems_ret = re.findall(r'<div class="contson".*?>(.*?)</div>', text, flags=re.DOTALL)
    poems = []
    for poem in poems_ret:
        temp = re.sub("<.*?>", "", poem)
        poems.append(temp.strip())
    results = []
    for value in zip(titles, dynasty, authors, poems):
        title, time, author, poem = value
        result = {
            "标题": title,
            "朝代": time,
            "作者": author,
            "原文": poem
        }

        results.append(result)
    print(results)


def spider():
    # url_base = 'https://so.gushiwen.cn/shiwens/default.aspx?page={}&tstr=&astr=%E6%9D%8E%E7%99%BD'
    url_base = 'https://www.gushiwen.cn/default_{}.aspx'
    for i in range(1, 2):
        print('正在爬取第{}页：'.format(i))
        url = url_base.format(i)
        print(" " * 20 + "优美古诗文" + " " * 20)

        print("*" * 50)
        parse_page(url)
        print("*" * 50)


if __name__ == '__main__':
    spider()