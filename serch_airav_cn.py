import sys
import requests
from javInfo_config import *
from lxml import etree


def airavSerch(fileinfo):

    domin = "https://airav.io"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

    # 获得主页面内容
    url = "https://airav.io/cn/search_result?kw=" + fileinfo['file_name']
    print(url)
    response = requests.get(url, headers=headers)
    page = response.text

    # 解析主页面结构
    tree = etree.HTML(page)
    serch_list = tree.xpath('//div[@class="oneVideo-top"]')

    if not serch_list:
        response.close()
        print("未找到相关番号")
        return None

    link_result = serch_list[0].xpath("./a/@href")
    response.close()

    # 查询子页面

    suburl = domin + link_result[0]
    subresponse = requests.get(suburl, headers=headers)

    # 解析子页面
    info_tree = etree.HTML(subresponse.text)
    info_class = info_tree.xpath('//div[@class="video-info"]')
    info_group = info_class[0].xpath('./div/ul')
    lenth_info_group = len(info_group)

    # 获取信息
    javdata = JaveData()

    fanhao = info_group[0].xpath('./li[contains(text(), "番号")]/span/text()')
    description = info_class[0].xpath('./p[@class="my-3"]/text()')
    label = info_group[0].xpath(
        './li[contains(text(), "标籤")]/a/text()')
    nvyou = info_group[0].xpath(
        './li[contains(text(), "女優")]/a/text()')
    changshang = info_group[0].xpath(
        './li[contains(text(), "厂商")]/a/text()')
    subresponse.close()

    # 组装javdata
    javdata.add_data('folder_path', fileinfo['folder_path'])
    javdata.add_data('file_name', fileinfo['file_name'])
    javdata.add_data('num', fanhao)
    javdata.add_data('plot', description)
    javdata.add_data('tag', label)
    javdata.add_data('changshang', changshang)

    return javdata.data


"""
if __name__ == '__main__':
    directory_path = get_json_path()
    print(f"Searching for video files in {directory_path}...")
    list_result = find_video_files(directory_path)
    print(list_result)
    for fanhao in [d['file_name'] for d in list_result]:
        print(airavSerch(fanhao))

"""
