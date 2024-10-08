import sys
import requests
from javInfo_base import *
from lxml import etree
from nfo import *


def javdbSerch(fileinfo):

    # 初始话参数
    # file_name = 'SSIS-903'
    file_name = fileinfo['file_name']
    data_folder = f'D:/Python/adata/{file_name}'
    domin = 'https://javdb.com'
    url = 'https://javdb.com/search'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    # 获得主页面内容
    url = "https://javdb.com/search?q=" + file_name
    print(url)
    response = requests.get(url, headers=headers)
    page = response.text
    tree = etree.HTML(page)
    page_item = tree.xpath('//div[@class="item"]')
    response.close()

    for item in page_item:
        if item.xpath('./a/div[@class="video-title"]/strong/text()')[0] == file_name:
            sublink = item.xpath('./a/@href')[0]
            print(sublink)
            break
        else:
            print('NO FILM FOUND')
            response.close()
            return None

    # 获取详细页面内容

    sub_url = domin + sublink
    sub_response = requests.get(sub_url, headers=headers)
    sub_page = sub_response.text
    sub_tree = etree.HTML(sub_page)
    response.close()

    # pages 各种分类页面
    title_html = sub_tree.xpath('//h2[@class="title is-4"]')[0]
    cover_html = sub_tree.xpath('//div[@class="column column-video-cover"]')[0]
    panel_html = sub_tree.xpath('//nav[@class="panel movie-panel-info"]')[0]
    images_html = sub_tree.xpath(
        '//div[@class="tile-images preview-images"]')[0]
    magnets_content_html = sub_tree.xpath('//div[@class="magnet-links"]')[0]

    # 获取title
    javnfo = JavNfo()
    check_create_folder(data_folder)

    fanhao = title_html.xpath('./strong/text()')[0]
    print(fanhao)
    current_title = title_html.xpath(
        './strong[@class="current-title"]/text()')
    print(current_title)
    origin_title = title_html.xpath('./span[@class="origin-title"]/text()')
    print(origin_title)

    # 获取封面路径并保存

    # cover_url = cover_html.xpath('./a/img/@src')[0]
    # print(cover_url)
    # cover_name = file_name + '.jpg'
    # save_pic(cover_url, cover_name, data_folder)

    # 获取nfo信息

    riqi = panel_html.xpath(
        './div[./strong[contains(text(), "日期")]]/span/text()')[0]
    print(riqi)
    shichang = panel_html.xpath(
        './div[./strong[contains(text(), "時長")]]/span/text()')[0]
    shichang_num = extract_number_from_text(shichang, 0)
    print(shichang_num)
    daoyan = panel_html.xpath(
        './div[./strong[contains(text(), "導演")]]/span/a/text()')
    print(daoyan)
    pianshang = panel_html.xpath(
        './div[./strong[contains(text(), "片商")]]/span/a/text()')[0]
    print(pianshang)
    pingfen = panel_html.xpath(
        './div[./strong[contains(text(), "評分")]]/span/text()')[0]
    pingfen_num = extract_number_from_text(pingfen, 0)
    print(pingfen_num)
    vote_num = extract_number_from_text(pingfen, 1)
    print(vote_num)
    leibie = panel_html.xpath(
        './div[./strong[contains(text(), "類別")]]/span/a/text()')
    print(leibie)
    yanyuan = panel_html.xpath(
        './div[./strong[contains(text(), "演員")]]/span/a/text()')
    print(yanyuan)

    # 组装javdata
    javnfo.set_nfo_dict('folder_path', fileinfo['folder_path'])
    javnfo.set_nfo_dict('file_name', fileinfo['file_name'])

    javnfo.set_nfo_dict('num', fanhao)
    javnfo.set_nfo_dict('title', current_title)
    javnfo.set_nfo_dict('originaltitle', origin_title)

    javnfo.set_nfo_dict('releasedate', riqi)
    javnfo.set_nfo_dict('release', riqi)
    javnfo.set_nfo_dict('premiered', riqi)
    javnfo.set_nfo_dict('tagline', '发行日期 '+riqi)

    javnfo.set_nfo_dict('rating', pingfen_num)
    javnfo.set_nfo_dict('votes', vote_num)
    javnfo.set_nfo_dict('runtime', shichang_num)

    javnfo.set_nfo_dict('actor', yanyuan)
    javnfo.set_nfo_dict('director', daoyan)

    javnfo.set_nfo_dict('studio', pianshang)
    javnfo.set_nfo_dict('maker', pianshang)
    javnfo.set_nfo_dict('publisher', pianshang)
    javnfo.set_nfo_dict('label', pianshang)

    javnfo.set_nfo_dict('tag', leibie)
    javnfo.set_nfo_dict('genre', leibie)

    # 获取预览图片
    # preview_img_urls = images_html.xpath(
    #     './a[@class="tile-item"]/@href')
    # print(preview_img_urls)
    # for preview_img_url in preview_img_urls:
    #     preview_img_name = preview_img_url.split('/')[-1]
    #     save_pic(preview_img_url, preview_img_name, data_folder)

    # 获取磁链
    magnets_content = magnets_content_html.xpath(
        '//div[contains(@class,"item columns is-desktop")]')
    magnets = []
    for magnet_content in magnets_content:
        magnet_url = magnet_content.xpath('./div/a/@href')[0]
        magnet_title = magnet_content.xpath(
            './div/a/span[@class="name"]/text()')[0]
        magnet_size = magnet_content.xpath(
            './div/a/span[@class="meta"]/text()')[0]

        magnets.append({'magnet_title': magnet_title,
                       'magnet_url': magnet_url, 'magnet_size': magnet_size})

    print(magnets)

    magnet_path = data_folder + '/' + file_name + '-magnets.txt'
    with open(magnet_path, 'w', encoding='utf-8') as file:
        # 遍历列表中的每个字典
        for magnet in magnets:
            # 遍历字典中的每个键值对
            for key, value in magnet.items():
                # 将键和值分行写入文件
                file.write(f"{key}: {value}\n")
            # 在每个字典之后添加一个空行以分隔不同的字典
            file.write("\n")

    return javnfo


if __name__ == '__main__':
    fileinfo = {'file_name': 'SSIS-903'}
    javdbSerch(fileinfo)
