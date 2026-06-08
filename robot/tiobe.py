import requests
import csv
from lxml import html
import re

# 常量
TMDB_BASE_URL = "https://www.themoviedb.org"
TMDB_TOP_ONE_PAGE_URL = f"{TMDB_BASE_URL}/movie/top-rated"
TMDB_TOP_AFTER_ONE_PAGE_URL = f"{TMDB_BASE_URL}/discover/movie/items"
MOVIE_LIST_FILE = "csv_data/movie_list.csv"

# 格式化电影年份
def format_year(year):
    match = re.search(r"\d+", year)
    if match:
        return match.group()
    return None

# 格式化电影上映时间
def format_release_date(release_date):
    match = re.search(r"\d{4}-\d{2}-\d{2}", release_date)
    if match:
        return match.group()
    return None

# 格式化电影时长
def format_duration(duration):
    g_duration = duration[0] if duration else ""
    h_res = re.search(r"(\d+)h", g_duration)
    m_res = re.search(r"(\d+)m", g_duration)
    h = int(h_res.group(1)) if h_res else 0
    m = int(m_res.group(1)) if m_res else 0
    return h * 60 + m

# 获取电影详情
def get_movie_info(movie_info_url):
    # 1. 发送请求，获取电影详情数据
    response = requests.get(movie_info_url, timeout=60)

    # 2. 解析数据，获取电影详情
    document = html.fromstring(response.text)

    # 电影名称
    movie_name= document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/a[1]/text()')
    # 年份
    year= document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/span/text()')
    # 上映时间
    release_date= document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[2]/text()')
    # 类型
    genre= document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[3]/a/text()')
    # 时长
    duration= document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[4]/text()')
    # 评分
    rating= document.xpath('//*[@id="consensus_pill"]/div/div[1]/div/div/@data-percent')
    # 语言
    language= document.xpath('//*[@id="media_v4"]/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()')
    # 导演
    director= document.xpath('//*[@id="original_header"]/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()')
    # 演员
    performers= document.xpath('//*[@id="cast_scroller"]/ol/li[@class="card"]/p[1]/a/text()')
    # 简介
    description= document.xpath('//*[@id="original_header"]/div[2]/section/div[3]/div/p/text()')

    movie_info = {
        "电影名称": movie_name[0] if movie_name else "",
        "年份": format_year(year[0] if year else ""),
        "上映时间": format_release_date(release_date[0] if release_date else ""),
        "类型": ",".join(genre) if genre else "",
        "时长": format_duration(duration),
        "评分": rating[0] if rating else "",
        "语言": language[0].strip() if language else "",
        "导演": director[0].strip() if director else "",
        "演员": ",".join(performers) if performers else "",
        "简介": description[0] if description else ""
    }

    # 3. 返回电影详情
    return movie_info


# 保存电影数据为 csv 文件
def save_all_movies(all_movies):
    with open(MOVIE_LIST_FILE, "w", newline="", encoding="utf-8-sig") as csvfile:
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
    all_movies = []

    # 获取 1-5 页的电影排名数据
    for page_num in range(1, 6):
        print(f"开始获取 第{page_num}页 榜单数据")

        # 1. 发送请求，获取高分电影榜单数据
        if page_num == 1:
            response = requests.get(TMDB_TOP_ONE_PAGE_URL, timeout=60)
        else:
            response = requests.post(TMDB_TOP_AFTER_ONE_PAGE_URL.format(page_num), data=f"air_date.gte=&air_date.lte=&certification=&certification_country=CN&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page_num}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2026-12-08&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&watch_region=CN&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400", timeout=60)

        # 2. 解析数据，获取电影榜单
        document = html.fromstring(response.text)
        movie_list = document.xpath("//*[@class='media-list-results contents']/div")

        # 3. 遍历电影列表，获取电影详情
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
