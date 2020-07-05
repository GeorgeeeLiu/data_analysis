import requests
from lxml import etree
import csv
import random, time
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
}


def getInfo(perfume_url):
    headers = {
        'User-Agent': ua.random
    }
    while True:
        s = requests.session()
        r = s.get(perfume_url, headers=headers)
        html = r.text.encode('utf-8')
        result = etree.HTML(html)
        if r.status_code == 200:
            print('状态码', r.status_code)
            # # # # Longevity
            fullname = result.xpath('//*[@id="col1"]/div/div/h1/span/text()')[0]
            Longevity_poor = int(result.xpath('//td[@class="ndSum"]/text()')[0])
            Longevity_weak = int(result.xpath('//td[@class="ndSum"]/text()')[1])
            Longevity_moderate = int(result.xpath('//td[@class="ndSum"]/text()')[2])
            Longevity_long_lasting = int(result.xpath('//td[@class="ndSum"]/text()')[3])
            Longevity_very_long_lasting = int(result.xpath('//td[@class="ndSum"]/text()')[4])
            break
        else:
            print('状态码', r.status_code, 'error')
            time.sleep(random.uniform(100, 11))
            # # # # Sillage
            # Sillage_soft =  int(result.xpath('//td[@class="ndSum"]/text()')[5])
            # Sillage_moderate = int(result.xpath('//td[@class="ndSum"]/text()')[6])
            # Sillage_heavy = int(result.xpath('//td[@class="ndSum"]/text()')[7])
            # Sillage_enormous = int(result.xpath('//td[@class="ndSum"]/text()')[8])
            # return Longevity_poor, Longevity_weak, Longevity_moderate, Longevity_long_lasting, Longevity_very_long_lasting, Sillage_soft, Sillage_moderate, Sillage_heavy, Sillage_enormous
    time.sleep(random.uniform(10, 11))
    return fullname, Longevity_poor, Longevity_weak, Longevity_moderate, Longevity_long_lasting, Longevity_very_long_lasting
    # return r


# with open("url_popular.csv", "w", newline='', encoding='utf-8-sig') as file:
#     writer = csv.writer(file, delimiter=',', )
#     writer.writerow(['perfumers_name', 'perfume_name', 'url'])

# # # perfumers方法https://www.fragrantica.com/noses/
s = requests.session()
k = 1
url = 'https://www.fragrantica.com/noses/'
html = s.get(url, headers=headers).text.encode('utf-8')
perfumersList = etree.HTML(html)
for i in range(0, 343):  # 0-343: popular  343-1598: all
    headers = {
        'User-Agent': ua.random
    }
    s = requests.session()
    print(i)
    # print(perfumersList)
    perfumers_name = perfumersList.xpath('//div[@class="cell small-12 medium-4"]/a/text()')[i]
    perfumers_url = 'https://www.fragrantica.com' + \
                    perfumersList.xpath('//div[@class="cell small-12 medium-4"]/a/@href')[i]
    html1 = s.get(perfumers_url, headers=headers).text.encode('utf-8')
    perfume_result = etree.HTML(html1)
    # time.sleep(random.uniform(1.5, 2))
    perfumeList = perfume_result.xpath('//div[@class= "cell large-6"]')
    for perfume in perfumeList:
        perfume_name = perfume.xpath('div/div[1]/div[3]/h3/a/text()')[0].split('\n')[0]
        perfume_url = 'https://www.fragrantica.com' + perfume.xpath('div/div[1]/div[3]/h3/a/@href')[0]
        print(k, perfumers_name, perfume_name, perfume_url)
        ll = [perfumers_name, perfume_name, perfume_url]
        # fullname, Longevity_poor, Longevity_weak, Longevity_moderate, Longevity_long_lasting, Longevity_very_long_lasting = getInfo(perfume_url)
        # print(k, perfumers_name, perfume_name, fullname, Longevity_poor, Longevity_weak, Longevity_moderate, Longevity_long_lasting, Longevity_very_long_lasting)
        # list = [perfumers_name, perfume_name, fullname, Longevity_poor, Longevity_weak, Longevity_moderate, Longevity_long_lasting, Longevity_very_long_lasting,]
        with open("url_popular.csv", "a+", newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=',', )
            writer.writerow(ll)
        # print(getInfo(perfume_url), type(getInfo(perfume_url)))
        k += 1
        # time.sleep(random.uniform(1.5, 2))
