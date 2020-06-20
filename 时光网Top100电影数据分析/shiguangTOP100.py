import pandas as pd
import requests
from bs4 import BeautifulSoup

# s = requests.session()
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
# }
# s.headers.update(headers)
df = pd.DataFrame(columns=('排名', '电影', '评分', '类型', '年度票房（美元）', '上映日期'))  # 表头
x = 0
for i in range(0, 10):
    url = 'http://movie.mtime.com/boxoffice/?year=2018&area=global&type=MovieRankingHistory'\
          '&category=all&page={}&display=table&timestamp=1592399312017&version=07bb781100018'\
          'dd58eafc3b35d42686804c6df8d&dataType=json'.format(
        str(i))
    # r = s.get(url=url, verify=False).text
    r = requests.get(url=url, verify=False).text  # 对网站进行访问
    bs = BeautifulSoup(r, 'lxml')  # 对网站进行解析
    tr = bs.find_all('tr')
    # 获取数据
    for j in tr[1:]:
        td = j.find_all('td')
        rank = td[0].text  # 排名
        title = td[1].a.text  # 电影名称
        rateing = float(td[1].div.text)  # 评分
        type = td[2].text  # 电影类型
        tick_num = td[3].text  # 票房
        release_date = td[4].text  # 上映日期
        list = [rank, title, rateing, type, tick_num, release_date]
        print(list)
        df.loc[x] = list
        x = x + 1

df.to_excel('raw_data.xlsx', index=False, encoding="GB18030")  # 数据导出excel


