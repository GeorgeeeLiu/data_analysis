import requests
import jsonpath
import json
import xlrd
import xlwt
from xlutils.copy import copy


# 获得商品系列的ID
def getSeriesID(keyword):
    URL = 'https://gapi.imagefield.cn/plast/search?q={}'.format(keyword)
    re = requests.get(URL)
    html = json.loads(re.text)
    SeriesID = jsonpath.jsonpath(html, '$..items')[3]
    return SeriesID


# 获得系列信息
def getSeriesInfo(SeriesID):
    URL = 'https://api.imagefield.cn/trade/v2/categories?tagId={}&limit=100000&offset=0'.format(SeriesID)
    re = requests.get(URL)
    html = json.loads(re.text)
    count = jsonpath.jsonpath(html, 'count')[0]
    productid = jsonpath.jsonpath(html, '$..id')
    productname = jsonpath.jsonpath(html, '$..name')
    productCount = jsonpath.jsonpath(html, '$..productCount')  #  在卖人数
    wishCount = jsonpath.jsonpath(html, '$..wishCount')   # 想要人数
    return count, productid, productname, productCount, wishCount


# 获得系列产品信息
def getProductInfo(productid):
    URL = 'https://api.imagefield.cn/trade/v2/spus?categoryId={}&limit=10000&offset=0&orderBy=latest'.format(productid)
    re = requests.get(URL)
    html = json.loads(re.text)
    count = jsonpath.jsonpath(html, 'count')[0]
    if count == 0:
        productid = None
        productname = None
        minPrice = None
        minOnlinePrice = None
        orderCount = None
    else:
        productid = jsonpath.jsonpath(html, '$..id')
        productname = jsonpath.jsonpath(html, '$..name')[::3]  # 名称
        minPrice = jsonpath.jsonpath(html, '$..minPrice')  # 最低价格
        minOnlinePrice = jsonpath.jsonpath(html, '$..minOnlinePrice')
        orderCount = jsonpath.jsonpath(html, '$..orderCount')  # 付款人数
    return count, productid, productname, minPrice, orderCount, minOnlinePrice


# 写入excel
def write_excel_xls(path, sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿


# 追加excel
def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i+rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    # print("xls格式表格写入/追加数据成功！")



def data(keyword):
    r_kw = getSeriesID(keyword)
    ID = r_kw[0]['id']
    count, productid, productname, productCount, wishCount = getSeriesInfo(ID)
    data = []
    for i in range(0, count):
        data.append([productname[i],productCount[i], wishCount[i]])
    return data


if __name__ == '__main__':
    keyword = 'molly'  # 自行更改关键词
    name_xls = '潮玩.xls'
    sheet_name_xls = '潮玩信息'
    value_title = [['名称', '在卖人数', '想要人数']]  # 表头
    write_excel_xls(name_xls, sheet_name_xls, value_title)
    write_excel_xls_append(name_xls, data(keyword))










