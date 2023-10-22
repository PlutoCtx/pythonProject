# @Version: python3.10
# @Time: 2023/8/25 16:57
# @Author: PlutoCtx
# @Email: 15905898514@163.com
# @File: fetch_fun.py
# @Software: PyCharm
# @User: chent

import datetime
import os
import re

import requests
from PyPDF2 import PdfMerger, PdfReader
from PyPDF2.errors import PdfReadError

# PDF链接
url = 'http://paper.people.com.cn/rmrb/images/2023-08/25/20/rmrb2023082520.pdf'


def init_date(start_date, end_date):
    """
    to get a list of formatted date, like '%Y-%m/%d', it is directly used in the url concat,
    and it is user to generate the files folder
    :param start_date:  start date
    :param end_date:    end date
    :return: list of date
    """
    start_year, start_month, start_day = map(int, start_date.split('-'))
    end_year, end_month, end_day = map(int, end_date.split('-'))

    date_list = []

    current_date = datetime.date(start_year, start_month, start_day)

    while current_date <= datetime.date(end_year, end_month, end_day):
        formatted_date = current_date.strftime('%Y-%m/%d')
        date_list.append(formatted_date)
        current_date += datetime.timedelta(days=1)

    return date_list


def fetch_people_daily_paper(res_list):
    """
    to get People's Daily's everyday newspaper,
    first, get a day's every single paper, save it as named 'rmrb2022040101' and saved in folder '\\files\\yyyy-MM\\dd'
    second, generate the single paper into a complete one day's paper
    :param res_list:list of date that are in defined duration
    :return: files saved
    """
    characters_to_remove = [",", "-", "/"]  # 要去除的字符列表

    # 遍历指定日期范围内的每一天，获取报纸
    for i in res_list:
        # http://... +  2023-08/25/
        temp = 'http://paper.people.com.cn/rmrb/images/' + i + '/'
        flag = update_paper_number(i)

        global folder_path
        folder_path = ""

        # 生成链接，下载当日某一版面的pdf文件
        for j in range(1, flag + 1):
            # http://... +  2023-08/25/ + /XX
            tem = temp + str(j).zfill(2)
            # /rmrb2023082520.pdf'
            string = str(j).zfill(2) \
                     + '/rmrb' \
                     + "".join([c for c in i if c not in characters_to_remove]) \
                     + str(j).zfill(2) + ".pdf"

            print(temp + string)
            # 发送GET请求下载PDF文件
            response = requests.get(temp + string, stream=True)

            # 设置文件夹路径和文件名
            folder_path = "files/" + i + '/'
            file_name = 'rmrb' + "".join([c for c in i if c not in characters_to_remove]) + str(j).zfill(2) + ".pdf"

            # 创建文件夹（如果不存在）
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # 生成文件的完整路径
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, 'wb') as file:
                file.write(response.content)

        # 获取文件夹中的所有 PDF 文件
        pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

        # 根据日期和数字标号排序
        pdf_files = sorted(pdf_files, key=sort_by_date_and_number)

        # 创建 PdfFileMerger 对象...
        pdf_merger = PdfMerger()

        # 逐个合并 PDF 文件
        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder_path, pdf_file)

            try:
                # 通过尝试打开并检查 PDF 文件来捕获异常
                with open(pdf_path, "rb") as f:
                    pdf = PdfReader(f)

                    # 如果文件正常打开，则将其添加到合并器中
                    pdf_merger.append(pdf)

            except (PdfReadError, OSError) as e:
                # 当遇到 PdfReadError 或 OSError 时跳过该文件并打印错误消息
                print(f"跳过文件 '{pdf_file}'，发生错误: {str(e)}")

            # pdf_merger.append(pdf_path)

        # 合并后的文件保存路径
        output_path = "total_files/"

        # 创建文件夹（如果不存在）
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        # 生成文件的完整路径
        total_file_path = os.path.join(output_path,
                                       i.replace("/", "-") + ".pdf")

        # 将合并后的 PDF 保存到指定路径
        pdf_merger.write(total_file_path)
        pdf_merger.close()


# 定义排序函数
def sort_by_date_and_number(file_name):
    match = re.search(r'\d+', file_name)  # 匹配文件名中的连续数字部分
    if match:
        number = int(match.group())  # 提取连续数字部分并转换为整数
        return file_name[4: 12], number
    return file_name, 0  # 如果没有数字部分，则按原始文件名排序


def get_weekday(now_time):
    """
    :param now_time: like 2023-08/25
    :return: 0 for Mon, 1 for Thu ...
    """
    # 使用多个分隔符拆分字符串
    y, m, d = re.split(r"[-/]",
                       now_time)

    date = datetime.datetime(int(y),
                             int(m),
                             int(d))
    weekday = date.weekday()

    print(int(y),
          int(m),
          int(d),
          weekday)

    return weekday


def update_paper_number(now_time):
    """
    判断当日的报纸有多少份
    周末两天只有8份，工作日有20份
    :param now_time:  like 2023-08/25
    :return: 当日报纸数
    """
    weekday = get_weekday(now_time)
    if weekday == 5 or weekday == 6:
        return 8
    else:
        return 20


if __name__ == '__main__':
    start_date = input("input start date like 'yyyy-MM-dd':")
    end_date = input("input end date like 'yyyy-MM-dd':")
    res_list = init_date(start_date, end_date)
    fetch_people_daily_paper(res_list)

    print("文件保存成功！")
