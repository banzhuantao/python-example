# # import requests
# #
# # # robots.txt
# #
# # # 定义url
# # target_url = "https://www.tiobe.com/tiobe-index/"
# #
# # # 发送请求，获取数据
# # responses = requests.get(target_url)
# #
# # with open("resources/tiobe-index.html", "w", encoding="utf-8") as f:
# #     f.write(responses.text)
# #
# # print("========================= 成功 =========================")
#
# from lxml import html
# import json
#
# with open("resources/tiobe-index.html", "r", encoding="utf-8") as f:
#   content = f.read()
#   selector = html.fromstring(content)
#
#   # 获取 id="top20" 的 table 元素
#   table = selector.xpath("//table[@id='top20']")[0]
#
#   # 获取当前 table 元素下的 Programming Language 和 Ratings
#   languages = table.xpath(".//tbody/tr/td[5]/text()")
#   ratings = table.xpath(".//tbody/tr/td[6]/text()")
#
#   # 将 languages、ratings 写入到 tiobe-index.json 文件中
#   with open("resources/tiobe-index.json", "w", encoding="utf-8") as j:
#     obj = {}
#
#     for index, value in enumerate(languages):
#       obj[f"_{languages[index]}"] = ratings[index]
#
#     json.dump(obj, j, ensure_ascii=False, indent=2)
import csv

import requests
from lxml import html

target_url = "https://www.tiobe.com/tiobe-index/"
responses = requests.get(target_url)
selector = html.fromstring(responses.text)
headers = selector.xpath('//*[@id="top20"]/thead/tr/*/text()')
content = selector.xpath('//*[@id="top20"]/tbody/tr')
# print(content.xpath("./*/text()"))

with open("resources/tiobe-index.csv", "w", encoding="utf-8") as f:
  csv_writer = csv.DictWriter(f, fieldnames=headers)
  csv_writer.writeheader()
  csv_writer.writerows()