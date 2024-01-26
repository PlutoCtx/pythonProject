# @Version: python3.10
# @Time: 2024/1/6 12:13
# @Author: PlutoCtx
# @Email: 15905898514@163.com
# @File: read_csv.py
# @Software: PyCharm
# @User: chent

import pandas as pd
import numpy as np
df = pd.read_csv('01data.csv', encoding="gbk")
df_xlsx = pd.read_excel('../data/02data.xlsx')
# df_array = np.array(df)
# df_list = df_array.tolist()
#
# for l in df_list:
#     print(l)



urls_csv = df['NavigatedToUrl']
urls_excel = df_xlsx['NavigatedToUrl']

# for url in urls_csv:
#     print(url)

for url in urls_excel:
    print(url)
print(len(urls_excel))
