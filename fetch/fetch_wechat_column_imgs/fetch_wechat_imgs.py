# @Version: python3.10
# @Time: 2024/1/6 19:07
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: fetch_wechat_imgs.py
# @Software: PyCharm
# @User: chent

import os
import re
import time
import threading

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import trange


# 获取网页信息
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


# 解析网页，获取所有图片url
def get_img_URL(html):
    soup = BeautifulSoup(html, "html.parser")
    ad_list = []
    for i in soup.find_all("img"):
        try:
            ad = re.findall(r'.*src="(.*?)?" .*', str(i))
            if ad:
                ad_list.append(ad)
        except:
            continue
    return ad_list


# 新建文件夹pic，下载并保存爬取的图片信息
def download(ad_list):

    global n
    n = 0
    # 注意更改文件目录
    root = "D:\\公众号爬取02\\location"
    for i in range(len(ad_list)):
        path = root + str(n + i) + "." + 'png'
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = requests.get(ad_list[i][0])
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
        n += 1

def read_csv_urls(path='data.csv'):
    df = pd.read_csv(path, encoding="gbk")

    url_list = df['NavigatedToUrl']
    return url_list

def read_excel_urls(path='./data/02data.xlsx'):
    df = pd.read_excel(path)
    url_list = df['NavigatedToUrl']
    return url_list

def include_all_single_process(url):
    html = getHTMLText(url)
    list = get_img_URL(html)
    download(list)


if __name__ == '__main__':
    threads = []
    urls = read_excel_urls()

    for i in trange(len(urls)):
        thread = threading.Thread(target=include_all_single_process(urls[i]))
        time.sleep(0.1)

    for thread in threads:
        thread.join()

    print("All downloads completed.")
