import requests

# robots.txt

# 定义url
target_url = "https://www.tiobe.com/tiobe-index/"

# 发送请求，获取数据
responses = requests.get(target_url)

with open("resources/tiobe-index.html", "w", encoding="utf-8") as f:
    f.write(responses.text)

print("========================= 成功 =========================")