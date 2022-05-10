from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re
from pyecharts import options as opts
from pyecharts.charts import Map

import datetime

now_time = datetime.datetime.now()

time = datetime.datetime.now().strftime('%Y-%m-%d')

def dxy_data_down(article_url):
    """

    """
    url = urlopen(article_url)
    soup = BeautifulSoup(url, 'html.parser')   # parser解析
    
    f = open("疫情数据.txt","w",encoding="utf-8")
    f.write(str(soup))
    f.close()

dxy_data_down("https://ncov.dxy.cn/ncovh5/view/pneumonia")
# json字符串前后关键词
json_start = "try { window.getAreaStat = "
# 字符串包含的括号要进行转义
json_end = "}catch\(e\){}"

# json字符串正则匹配
# (.*?)是匹配所有内容
regular_key = json_start + "(.*?)" + json_end




def get_json():

    f = open("疫情数据.txt", "r", encoding="utf-8")
    f_content = f.read()
    f.close()
    
    # json字符串前后关键词
    json_start = "try { window.getAreaStat = "
    # 字符串包含的括号要进行转义
    json_end = "}catch\(e\){}"
    
    # json字符串正则匹配
    # (.*?)是匹配所有内容
    regular_key = json_start + "(.*?)" + json_end
    # 参数rs.S可以无视换行符，将所有文本视作一个整体进行匹配
    re_content = re.search(regular_key, f_content, re.S)
    # group()用于获取正则匹配后的字符串
    content = re_content.group()
    
    # 去除json字符串的前后关键词
    content = content.replace(json_start, '')
    # 尾巴要去掉转义符号
    json_end = "}catch(e){}"
    content = content.replace(json_end, '')
    
    #  print(content)
    return content

json_content = get_json()




def display_provinces(json_content):

    json_data = json.loads(json_content)
    
    # 省份数据展示
    print(time+"全国各省份疫情数据如下：")
    for i in json_data:
        print("【省份名】：" + i["provinceName"])
        print("现存确诊：" + str(i["currentConfirmedCount"]))
        print("累计确诊：" + str(i["confirmedCount"]))
        print("死亡：" + str(i["deadCount"]))
        print("治愈：" + str(i["curedCount"]))
        print()

display_provinces(json_content)


def get_provinces(json_content):
    """
    
    """
    # 将字符串转化为字典
    json_data = json.loads(json_content)
    
    data = []
    
    # 省份数据展示
    for i in json_data:
        # 省份名称处理，和地图对应
        province_name = i["provinceName"]
        if(len(province_name)>1):
            if(province_name[-1] == "省"):
                province_name = province_name[:-1]
            if(province_name[-1] == "市"):
                province_name = province_name[:-1]
        if(len(province_name)>3):
            if(province_name[-3:] == "自治区"):
                province_name = province_name[:-3]
        if(len(province_name)>3):
            if(province_name[-3:] == "维吾尔"):
                province_name = province_name[:-3]
        if(len(province_name)>2):
            if(province_name[-2:] == "壮族"):
                province_name = province_name[:-2]
            if(province_name[-2:] == "回族"):
                province_name = province_name[:-2]
        
        data.append((province_name, i["currentConfirmedCount"]))
         
    print("全国各省份疫情数据如下：")
    for i in data:
        print(i)
        
    return data

    province_name = i["provinceName"]
    if(len(province_name)>1):
        if(province_name[-1] == "省"):
            province_name = province_name[:-1]
            if(province_name[-1] == "市"):
                province_name = province_name[:-1]
        if(len(province_name)>3):
            if(province_name[-3:] == "自治区"):
                province_name = province_name[:-3]
        if(len(province_name)>3):
            if(province_name[-3:] == "维吾尔"):
                province_name = province_name[:-3]
        if(len(province_name)>2):
            if(province_name[-2:] == "壮族"):
                province_name = province_name[:-2]
        if(province_name[-2:] == "回族"):
            province_name = province_name[:-2]


data = get_provinces(json_content)

pieces = [
    {'min': 10000, 'color': '#540d0d'},
    {'max': 9999, 'min': 1000, 'color': '#9c1414'},
    {'max': 999, 'min': 500, 'color': '#d92727'},
    {'max': 499, 'min': 100, 'color': '#ed3232'},
    {'max': 99, 'min': 10, 'color': '#f27777'},
    {'max': 9, 'min': 1, 'color': '#f7adad'},
    {'max': 0, 'color': '#f7e4e4'},
]

def create_china_map():
    ''' 
     作用：生成中国疫情地图
    '''
    (
        Map()
        .add(
            series_name=time+" 现存确诊", 
            data_pair=data, 
            maptype="china", 
            # 是否默认选中，默认为True
            is_selected=True,
            # 是否启用鼠标滚轮缩放和拖动平移，默认为True
            is_roam=True,
            # 是否显示图形标记，默认为True
            is_map_symbol_show=True
        )
        # 系列配置项
        # 关闭标签名称显示
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        # 全局配置项
        .set_global_opts(
            # 设置标题
            title_opts=opts.TitleOpts(title="中国疫情地图"),
            # 设置视觉配置项分段显示
            visualmap_opts=opts.VisualMapOpts(
                pieces=pieces,
                is_piecewise=True,
                is_show=True
            )
        )
        # 生成本地html文件
        .render("中国疫情地图.html")
    )
    
create_china_map()

