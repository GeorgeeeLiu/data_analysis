import pandas as pd
import requests
from lxml import etree
import csv
import random, time
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter

p = [{'https': 'https://52.191.103.11:3128'},
     {'https': 'https://3.9.34.151:3128'},
     {'https': 'https://34.67.11.156:3128'},
     {'https': 'https://161.35.66.242:3128'},
     {'https': 'https://54.241.121.74:3128'},
     {'https': 'https://157.230.165.31:10492'},
     {'https': 'https://136.244.107.186:8080'},
     None]
proxies = None
times = 0


def getInfo(perfume_url):
    global proxies, times
    ua = UserAgent(verify_ssl=False)
    while True:
        try:
            headers = {'User-Agent': ua.random}
            s = requests.session()
            print('ip代理', proxies)
            s.mount('https://', HTTPAdapter(max_retries=1))  # 断线重连3次
            # s.mount('http://', HTTPAdapter(max_retries=3))
            re = s.get(perfume_url, headers=headers, proxies=proxies, timeout=2)
            html = re.text.encode('utf-8')
            result = etree.HTML(html)
            if re.status_code == 200:
                # print('状态码', re.status_code)
                # # # # Longevity
                fullname = result.xpath('//*[@id="col1"]/div/div/h1/span/text()')[0]
                Longevity_poor = int(result.xpath('//td[@class="ndSum"]/text()')[0])
                Longevity_weak = int(result.xpath('//td[@class="ndSum"]/text()')[1])
                Longevity_moderate = int(result.xpath('//td[@class="ndSum"]/text()')[2])
                Longevity_long_lasting = int(result.xpath('//td[@class="ndSum"]/text()')[3])
                Longevity_very_long_lasting = int(result.xpath('//td[@class="ndSum"]/text()')[4])
                # # # # Sillage
                # Sillage_soft =  int(result.xpath('//td[@class="ndSum"]/text()')[5])
                # Sillage_moderate = int(result.xpath('//td[@class="ndSum"]/text()')[6])
                # Sillage_heavy = int(result.xpath('//td[@class="ndSum"]/text()')[7])
                # Sillage_enormous = int(result.xpath('//td[@class="ndSum"]/text()')[8])
                # return Longevity_poor, Longevity_weak, Longevity_moderate, Longevity_long_lasting, Longevity_very_long_lasting, Sillage_soft, Sillage_moderate, Sillage_heavy, Sillage_enormous
                break
            else:
                print('状态码', re.status_code, 'error, 需要切换ip代理')
                proxies = random.choice(p)
            # time.sleep(random.uniform(100, 11))
        except Exception as e:
            times = times + 1
            proxies = random.choice(p)
            print(e, '重试第%s次' % times)
    return fullname, Longevity_poor, Longevity_weak, Longevity_moderate, Longevity_long_lasting, Longevity_very_long_lasting


df = pd.read_csv('url_all.csv')
#
# with open("data_all.csv", "w", newline='', encoding='utf-8-sig') as file:
#     writer = csv.writer(file, delimiter=',', )
#     writer.writerow(['name', 'poor', 'weak', 'moderate', 'long_lasting', 'very_long_lasting'])


num = len(df.url)
k = len(pd.read_csv('data_all.csv'))
a = k + 1
for i in range(a, num):
    fullname, Longevity_poor, Longevity_weak, Longevity_moderate, Longevity_long_lasting, Longevity_very_long_lasting = getInfo(
        df.url[i])
    print(k, fullname, Longevity_poor, Longevity_weak, Longevity_moderate,
          Longevity_long_lasting, Longevity_very_long_lasting)
    list = [fullname, Longevity_poor, Longevity_weak, Longevity_moderate,
            Longevity_long_lasting, Longevity_very_long_lasting, ]
    with open("data_all.csv", "a+", newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=',', )
        writer.writerow(list)
    k += 1
