import numpy as np
import pandas as pd
import seaborn as sns
import re
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码

df_raw = pd.read_excel('raw_data.xlsx')  # 读取原数据

# 数据预处理
df = df_raw
del df['排名']  # 删掉排名这一列


# 将年度票房改为亿美元，数据格式为浮点格式
def tranTickNum(s):
    s = re.sub(r'亿', '', s)
    s = float(s)
    return s


df['年度票房（亿美元）'] = df['年度票房（美元）'].apply(tranTickNum)
del df['年度票房（美元）']  # 删掉旧数据


# 将上映日期改为日期格式
def tran2date(s):
    s = re.sub(r'年', '/', s)
    s = re.sub(r'月', '/', s)
    s = re.sub(r'日', '', s)
    return s


df['上映日期'] = df['上映日期'].apply(tran2date)
df['上映日期'] = pd.to_datetime(df['上映日期'], format='%Y/%m/%d', errors='coerce')
df['上映年份'] = df['上映日期'].map(lambda x: x.year)
df.loc[(df['上映年份'] >= 1970), '年代'] = '1970-79'
df.loc[(df['上映年份'] >= 1980), '年代'] = '1980-89'
df.loc[(df['上映年份'] >= 1990), '年代'] = '1990-99'
df.loc[(df['上映年份'] >= 2000), '年代'] = '2000-09'
df.loc[(df['上映年份'] >= 2010), '年代'] = '2010-20'
del df['上映年份']

print(df.head())
# print(df.info())
# print(df.describe())


# 时光网TOP100电影评分分布图
plt.figure(figsize=(10, 5))  # 调节图形大小
plt.hist(df['评分'], edgecolor='black', alpha=0.7, bins=23)  # 画直方图
plt.title("时光网TOP100电影评分分布图")
plt.ylabel('频数')
plt.xlabel('评分')
plt.show()

# 时光网TOP100电影中各年代电影的平均票房数
dft = df.groupby('年代')['年度票房（亿美元）'].mean()
rank = dft.argsort().argsort()
pal = sns.color_palette("Reds_d", len(dft))
plt.figure(figsize=(5, 5))
g = sns.barplot(x=dft.index, y=dft, palette=np.array(pal[::-1])[rank])
index = np.arange(len(dft.index))
for a, b in zip(index, dft):
    g.text(a, b, '%.2f' % b, color="black", ha="center")
plt.title("时光网TOP100电影中各年代电影的平均票房数")
plt.show()

# 时光网TOP100电影中各年代电影数量
dftt = df.groupby('年代')['电影'].count()
rank = dftt.argsort().argsort()
pal = sns.color_palette("Reds_d", len(dftt))
plt.figure(figsize=(5, 5))
g = sns.barplot(x=dftt.index, y=dftt, palette=np.array(pal[::-1])[rank])
index = np.arange(len(dftt.index))
for a, b in zip(index, dftt):
    g.text(a, b, b, color="black", ha="center")
plt.title("时光网TOP100电影中各年代电影数量")
plt.ylabel('电影数量')
plt.show()

# 不同类型电影的平均年度票房数
x = ['传记', '剧情', '冒险', '奇幻', '家庭', '科幻', '爱情', '惊悚', '战争', '犯罪', '悬疑']
y1 = []
for i in x:
    y1.append(df.loc[df['类型'].str.contains(i)]['年度票房（亿美元）'].mean())
data_bar = pd.DataFrame(zip(x, y1))
data_bar = data_bar.sort_values(by=1)
plt.figure(figsize=(5, 5))
plt.barh(range(len(data_bar)), data_bar[1], tick_label=data_bar[0])
plt.title('不同类型电影的平均年度票房数（亿美元）')
plt.ylabel('电影类型')
plt.xlabel('年度票房数（亿美元）')
plt.show()

# 各类电影占比
y2 = []
for i in x:
    y2.append(df.loc[df['类型'].str.contains(i)]['电影'].count())
x_pie = ['其他']
y_pie = []
y_else = []
for i in x:
    k = df.loc[df['类型'].str.contains(i)]['电影'].count()
    if k >= 3:
        x_pie.append(i)
        y_pie.append(k)
    else:
        y_else.append(k)
y_pie.insert(0, sum(y_else))
plt.figure(figsize=(8, 8))  # 调节图形大小
labels = x_pie  # 定义标签
sizes = y_pie  # 每块值
explode = (0, 0, 0.03, 0, 0.03, 0, 0)  # 将某一块分割出来，值越大分割出的间隙越大
patches, text1, text2 = plt.pie(sizes,
                                explode=explode,
                                labels=labels,
                                autopct='%3.2f%%',  # 数值保留固定小数位
                                shadow=True,  # 阴影
                                startangle=90,  # 逆时针起始角度设置
                                pctdistance=0.8
                                )
plt.title('各类电影占比')
plt.legend()
plt.show()
