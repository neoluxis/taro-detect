# -*- coding: UTF-8 -*-
import requests
import json
import os
import time
# 创建一个文件夹
path = 'downloaded'
if not os.path.exists(path):
    os.mkdir(path)
# 导入一个请求头
header = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
# 用户（自己）输入信息指令
keyword = input('请输入你想下载的内容：')
label = input('Label: ')
page = input('请输入你想爬取的页数：')
page = int(page) + 1
n = 140
pn = 1
# pn代表从第几张图片开始获取，百度图片下滑时默认一次性显示30张
for m in range(1, page):
    url = 'https://image.baidu.com/search/acjson?'
    param = {
        'tn': 'resultjson_com',
        'logid': ' 7517080705015306512',
        'ipn': 'rj',
        'ct': '201326592',
        'is': '',
        'fp': 'result',
        'queryWord': keyword,
        'cl': '2',
        'lm': '-1',
        'ie': 'utf-8',
        'oe': 'utf-8',
        'adpicid': '',
        'st': '',
        'z': '',
        'ic': '',
        'hd': '',
        'latest': '',
        'copyright': '',
        'word': keyword,
        's': '',
        'se': '',
        'tab': '',
        'width': '',
        'height': '',
        'face': '',
        'istype': '',
        'qc': '',
        'nc': '1',
        'fr': '',
        'expermode': '',
        'force': '',
        'cg': 'star',
        'pn': pn,
        'rn': '30',
        'gsm': '1e',
    }
    # 定义一个空列表，用于存放图片的URL
    image_url = list()
    # 将编码形式转换为utf-8
    response = requests.get(url=url, headers=header, params=param)
    response.encoding = 'utf-8'
    response = response.text
    # 把字符串转换成json数据
    data_s = json.loads(response)
    a = data_s["data"]  # 提取data里的数据
    for i in range(len(a)-1):  # 去掉最后一个空数据
        data = a[i].get("thumbURL", "not exist")  # 防止报错key error
        image_url.append(data)

    for image_src in image_url:
        image_data = requests.get(url=image_src, headers=header).content  # 提取图片内容数据
        image_name = '{}'.format(n+1) + '.jpg'  # 图片名
        image_path = path + '/' + label + '-' + image_name  # 图片保存路径
        with open(image_path, 'wb') as f:  # 保存数据
            f.write(image_data)
            print(image_name, '下载成功啦！！！')
            f.close()
        n += 1
    pn += 29
    time.sleep(1)


