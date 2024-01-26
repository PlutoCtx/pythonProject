# @Version: python3.10
# @Time: 2023/8/29 11:53
# @Author: PlutoCtx
# @Email: 15905898514@163.com
# @File: fetch_zjxc_pdfs.py
# @Software: PyCharm
# @User: chent

# import requests
# import pdfkit

# 文章的网址链接
article_url = 'https://mp.weixin.qq.com/s?__biz=Mzg5Mjc3NzQzMA==&mid=2247513059&idx=1&sn=13ea326e4679d0fcfadc9de454e00ccb&chksm=c03a155af74d9c4cd90309ef076b97471a626420df55895fba3a8b647099329e6ddef4cb0d83&scene=21#wechat_redirect'  # 替换为具体的文章链接

# # 使用 requests 获取文章内容
# response = requests.get(article_url)
# article_content = response.text
#
# # 使用 pdfkit 将内容保存为 PDF 文件
# pdfkit.from_string(article_content, 'article.pdf')


# if __name__ == '__main__':
#     # import requests
#     # import pdfkit
#     #
#     # # 文章的网址链接
#     # # article_url = 'https://www.example.com/article'  # 替换为具体的文章链接
#     #
#     # # 使用 requests 获取文章内容
#     # response = requests.get(article_url)
#     # article_content = response.text
#     #
#     # # 指定保存路径和文件名
#     # save_path = '/path/to/save/directory/article.pdf'  # 替换为你想要保存的路径和文件名
#     #
#     # # 使用 pdfkit 将内容保存为 PDF 文件
#     # try:
#     #     pdfkit.from_string(article_content, save_path)
#     #     print("文件已成功保存为 PDF。")
#     # except Exception as e:
#     #     print("保存 PDF 文件时发生错误:", str(e))
#
#     import requests
#     import pdfkit
#
#     # 文章的网址链接
#     # article_url = 'https://www.example.com/article'  # 替换为具体的文章链接
#
#     # 使用 requests 获取文章内容
#     response = requests.get(article_url)
#     article_content = response.text
#
#     # 指定保存路径和文件名
#     save_path = '/path/to/save/directory/article.pdf'  # 替换为你想要保存的路径和文件名
#
#     # 使用 pdfkit 将内容保存为 PDF 文件
#     try:
#         pdfkit.from_string(article_content, save_path)
#         print("文件已成功保存为 PDF。")
#     except Exception as e:
#         print("保存 PDF 文件时发生错误:", str(e))



# # 使用 requests 获取文章内容
# response = requests.get(article_url)
# article_content = response.text
#
# # 指定保存路径和文件名
# save_path = 'total_files/article.pdf'  # 替换为你想要保存的路径和文件名
#
# # 使用 pdfkit 将内容保存为 PDF 文件
# try:
#     pdfkit.from_string(article_content, save_path)
#     print("文件已成功保存为 PDF。")
# except Exception as e:
#     print("保存 PDF 文件时发生错误:", str(e))


# import requests
# import pdfkit
#
# # 文章的网址链接
# article_url = 'https://www.example.com/article'  # 替换为具体的文章链接
#
# # 使用 requests 获取文章内容
# response = requests.get(article_url)
# article_content = response.text
#
# # 指定保存路径和文件名
# save_path = '/path/to/save/directory/article.pdf'  # 替换为你想要保存的路径和文件名
#
# # 指定 wkhtmltopdf 的可执行文件路径
# config = pdfkit.configuration(wkhtmltopdf='D:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf')
#
# # 使用 pdfkit 将内容保存为 PDF 文件
# try:
#     pdfkit.from_string(article_content, save_path, configuration=config)
#     print("文件已成功保存为 PDF。")
# except Exception as e:
#     print("保存 PDF 文件时发生错误:", str(e))
#



# import os
# import pdfkit
# import datetime
# import wechatsogou
# '''
# 遇到不懂的问题？Python学习交流群：1004391443满足你的需求，资料都已经上传群文件，可以自行下载！
# '''
# # 初始化API
# ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3)
#
#
# def url2pdf(url, title, targetPath):
#     '''
#     使用pdfkit生成pdf文件
#     :param url: 文章url
#     :param title: 文章标题
#     :param targetPath: 存储pdf文件的路径
#     '''
#     try:
#         content_info = ws_api.get_article_content(url)
#     except:
#         return False
#     # 处理后的html
#     html = f'''
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <title>{title}</title>
#     </head>
#     <body>
#     <h2 style="text-align: center;font-weight: 400;">{title}</h2>
#     {content_info['content_html']}
#     </body>
#     </html>
#     '''
#     try:
#         pdfkit.from_string(html, targetPath + os.path.sep + f'{title}.pdf')
#     except:
#         # 部分文章标题含特殊字符，不能作为文件名
#         filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.pdf'
#         pdfkit.from_string(html, targetPath + os.path.sep + filename)
#
#
# if __name__ == '__main__':
#     # 此处为要爬取公众号的名称
#     gzh_name = '浙江宣传'
#     targetPath = os.getcwd() + os.path.sep + gzh_name
#     # 如果不存在目标文件夹就进行创建
#     if not os.path.exists(targetPath):
#         os.makedirs(targetPath)
#     # 将该公众号最近10篇文章信息以字典形式返回
#     data = ws_api.get_gzh_article_by_history(gzh_name)
#     article_list = data['article']
#     for article in article_list:
#         url = article['content_url']
#         title = article['title']
#         url2pdf(url, title, targetPath)



import requests
import pdfkit
import xhtml2pdf

# 文章的网址链接
article_url = 'https://www.example.com/article'  # 替换为实际的文章链接

# 使用 requests 获取文章内容
response = requests.get(article_url)
article_content = response.text

# 指定保存路径和文件名
save_path = '/path/to/save/directory/article.pdf'  # 替换为你想要保存的路径和文件名

# 设置配置选项
options = {
    'no-stop-slow-scripts': None
}

# 使用 pdfkit 将内容保存为 PDF 文件
try:
    pdfkit.from_string(article_content, save_path, options=options)
    print("文件已成功保存为 PDF。")
except Exception as e:
    print("保存 PDF 文件时发生错误:", str(e))
