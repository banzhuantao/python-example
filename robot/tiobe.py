import requests
import csv
from lxml import html
import re

# 常量
TMDB_BASE_URL = "https://www.themoviedb.org"
TMDB_TOP_URL = f"{TMDB_BASE_URL}/movie/top-rated"
MOVIE_LIST_FILE = "csv_data/movie_list.csv"


# 获取电影详情
def get_movie_info(movie_info_url):
    # 1. 发送请求，获取电影详情数据
    response = requests.get(movie_info_url, timeout=60)

    # 2. 解析数据，获取电影详情
    document = html.fromstring(response.text)
    movie_info = {
        "电影名称": document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/a[1]/text()')[0],
        "年份": document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/span/text()')[0][1:-1],
        "上映时间": re.search(r"\d{4}-\d{2}-\d{2}",
                              document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[2]/text()')[
                                  0]).group(),
        "类型": ",".join(document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[3]/a/text()')),
        "时长": document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[4]/text()')[0].strip(),
        "评分": document.xpath('//*[@id="consensus_pill"]/div/div[1]/div/div/@data-percent')[0],
        "语言": ",".join(
            document.xpath('//*[@id="media_v4"]/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()')),
        "导演": ",".join(document.xpath('//*[@id="original_header"]/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()')),
        "演员": ",".join(document.xpath('//*[@id="cast_scroller"]/ol/li[@class="card"]/p[1]/a/text()')),
        "简介": document.xpath('//*[@id="original_header"]/div[2]/section/div[3]/div/p/text()')[0]

    }

    # 3. 返回电影详情
    return movie_info


# 保存电影数据为 csv 文件
def save_all_movies(all_movies):
    with open(MOVIE_LIST_FILE, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile,
                                fieldnames=["电影名称", "年份", "上映时间", "类型", "时长", "评分", "语言", "导演",
                                            "演员",
                                            "简介"])
        # 写入表头
        writer.writeheader()
        # 写入数据
        writer.writerows(all_movies)

# 主函数，定义核心逻辑
def main():
    # 1. 发送请求，获取高分电影榜单数据
    response = requests.get(TMDB_TOP_URL, timeout=60)

    # 2. 解析数据，获取电影榜单
    document = html.fromstring(response.text)
    movie_list = document.xpath("//*[@class='media-list-results contents']/div")

    # 3. 遍历电影列表，获取电影详情
    all_movies = []
    for movie in movie_list:
        movie_urls = movie.xpath(".//a[@class='flex w-full']/@href")
        if movie_urls:
            # 电影详情的 url
            movie_info_url = TMDB_BASE_URL + movie_urls[0]
            # 发送请求，获取电影详情数据
            movie_info = get_movie_info(movie_info_url)
            all_movies.append(movie_info)

    # 4. 保存数据为 csv 文件
    save_all_movies(all_movies)


if __name__ == "__main__":
    main()
