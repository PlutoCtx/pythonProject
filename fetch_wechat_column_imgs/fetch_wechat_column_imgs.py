# @Version: python3.10
# @Time: 2024/1/5 23:47
# @Author: PlutoCtx
# @Email: 15905898514@163.com
# @File: fetch_wechat_column_imgs.py
# @Software: PyCharm
# @User: chent

import requests
from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import numpy as np
import time
from tqdm import trange

# 获取网页信息
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30, stream=True)
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
def download(ad_list, location):
    # 注意更改文件目录
    root = "D:\\公众号爬取\\" + location + "\\"
    for i in range(len(ad_list)):
        path = root + str(i) + "." + 'png'
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = requests.get(ad_list[i][0])
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()


def read_csv_urls(path='data.csv'):
    df = pd.read_csv(path, encoding="gbk")
    # df_array = np.array(df)
    # df_list = df_array.tolist()
    #
    # for l in df_list:
    #     print(l)
    url_list = df['NavigatedToUrl']
    # for url in urls:
    #     print(url)
    return url_list

def read_excel_urls(path='./data/02data.xlsx'):
    df = pd.read_excel(path)
    url_list = df['NavigatedToUrl']
    return url_list



if __name__ == '__main__':

    urls = read_excel_urls()

    for i in trange(1349, len(urls)):
        html = getHTMLText(urls[i])
        list = get_img_URL(html)
        download(list, '【' + str('%05d' %(i + 1031)) + '】')
        # print("**********************" + str('%05d' %i))
        time.sleep(0.1)
