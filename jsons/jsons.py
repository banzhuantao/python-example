import json

obj = {
    "name": "张三",
    "age": 18,
    "hobbies": ["football", "basketball"],
    "address": {
        "city": "上海",
        "street": "上海路"
    },
    "gender": "male"
}

with open("session.json", "w", encoding="utf-8") as f:
    json.dump(obj, f, ensure_ascii=False, indent=4)

"""
import json

with open("session.json", "r", encoding="utf-8") as f:
    content = f.read()  # 读取文件内容
    obj = json.loads(content)  # 将字符串内容解析为 JSON 对象
    print(obj)
"""