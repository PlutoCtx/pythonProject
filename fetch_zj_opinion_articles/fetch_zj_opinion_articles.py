# @Version: python3.10
# @Time: 2023/10/22 16:53
# @Author: PlutoCtx
# @Email: 15905898514@163.com
# @File: fetch_zj_opinion_articles.py
# @Software: PyCharm
# @User: chent

import requests
from bs4 import BeautifulSoup


def fetch_online_codes(url):
    """
    to get online html codes, including the information we need
    :param url: string, online page's url
    :return:    string, online page's html codes
    """

    # 发送请求，获取网页源码
    response = requests.get(url)

    # 指定编码格式，防止中文乱码
    # 指定网页编码为UTF-8
    response.encoding = 'utf-8'

    # 将网页源码全部存到html中，类型为字符串类型
    html = response.text

    return html


def get_article_items(soup, classname):
    return soup.find_all(class_=classname)


def handle_article_info(cur_content, article_info):
    """
    to format the article info
    :param cur_content:     current content
    :param article_info:    article information
    :return:    formatted and added content
    """
    info = "> " + str(article_info.pop().text)
    info = info.replace("作者", " 作者").replace("编辑", " 编辑").replace("\n", " ")
    cur_content += info
    cur_content += "\n"

    return cur_content


def fetch_opinion_articles(url):
    """
    to get ZheJiang Opinion's articles
    :param url: string, online page's url
    :return:    article's single parts, including its title,
                info(source, author, editor, publish time),
                contents, remarks and hot talks

    """

    html_content = fetch_online_codes(url)

    # 新建 BeautifulSoup 对象，对html内容进行解析
    soup = BeautifulSoup(html_content, features='html.parser')

    # 获取文章名
    article_title = get_article_items(soup, "artTitle")

    # 获取文章信息，来源、作者、编辑、发布时间
    article_info = get_article_items(soup, "info")

    # 获取文章具体内容
    article_contents = get_article_items(soup, "artCon")

    # 整文拼接
    all_content = ""
    try:
        """
        因为我本人习惯于使用 typora 进行记录，所以现在在编写代码是把一些Markdown语法的格式也写进去，主要在字符串的拼接这一部分，
        所以有些地方对于不了解Markdown语法的人可能会显得有点不知所云
        """
        # 文章标题拼接
        title = "## " + article_title.pop().text + "\n"
        all_content += title

        # 文章信息拼接
        all_content = handle_article_info(all_content, article_info)

        # 文章内容拼接
        content = str(article_contents.pop().text)
        content = content.replace("\u3000\u3000", "\r\n\n")

        all_content += content

        with open('opinion.txt', 'a') as f:
            f.write(all_content)
        print(all_content)

    except:
        print("error!!!")


if __name__ == '__main__':
    # 潮评某文章网页链接url
    # 打开文件
    f = open("urls.txt")

    # 调用文件的 readline()方法
    line = f.readline()  # 每次读取一行内容

    i = 0
    while line:
        line = f.readline().strip()
        fetch_opinion_articles(line)
        print(i + 1)
        i += 1

    f.close()
