# 打开 zeng-wang-lun.txt 文件准备写入
with open('resource/zeng-wang-lun.txt', 'w', encoding='utf-8') as file:
    # 写入《赠汪伦》的内容
    file.write(
        """赠汪伦（李白）
李白乘舟将欲行，忽闻岸上踏歌声。
桃花潭水深千尺，不及汪伦送我情。
        """)
