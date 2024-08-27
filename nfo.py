from lxml import etree
from javInfo_base import *

'''
Emby 支持的 NFO 字段包括但不限于以下：

Title: 电影或媒体的标题。
OriginalTitle: 原始语言的标题。
SortTitle: 用于排序的标题。
Year: 发行年份。
Studio: 制作公司。
Rating: 评分。
Director: 导演。
Writer: 编剧。
Actors: 演员列表。
Genres: 电影类型或风格。
Plot: 剧情概述。
Tagline: 电影标语或口号。
Runtime: 播放时长。
Cover: 封面图片的链接。
Back Cover: 背面图片的链接。
Disc Art: 光盘艺术图片的链接。
Logo: 电影或系列的徽标图片链接。
Clear Art: 清晰的艺术作品图片链接。
Banner: 横幅图片链接。
Thumb: 缩略图图片链接。
TheMovieDb Id: TheMovieDb 的唯一识别码。
TheOpenMovieDatabase Id: The Open Movie Database 的唯一识别码。
'''


class JavNfo:

    def __init__(self):
        self.nfo_dict = {'title': '', 'originaltitle': '', 'num': '', 'sorttitle': '',
                         'release': '', 'releasedate': '', 'premiered': '', 'tagline': '',
                         'actor': [], 'director': [],
                         'mpaa': '', 'customrating': '', 'countrycode': '',
                         'rating': '', 'criticrating': '', 'votes': '', 'year': '',
                         'runtime': '', 'studio': '', 'maker': '', 'publisher': '', 'label': '',
                         'tag': [], 'genre': [],
                         'poster': '', 'cover': '', 'trailer': '', 'website': '', 'javdbid': '',
                         'folder_path': '', 'file_name': ''}

    def set_nfo_dict(self, key, value):
        self.nfo_dict[key] = value

    def get_nfo_dict(self, key):
        return self.nfo_dict[key]

    def create_nfo(self):

        # 创建根元素
        movie = etree.Element("movie")
        javdict = self.nfo_dict
        # 添加 XML 声明
        movie.attrib['{http://www.w3.org/2001/xmlschema-instance}schemaLocation'] = 'http://www.w3.org/2001/XMLSchema'
        movie.attrib['{http://www.w3.org/2001/xmlschema-instance}noNamespaceSchemaLocation'] = 'schema.xsd'

        for key, value in javdict.items():
            # 为字典的每个键创建一个子元素，并设置其文本内容为字典的值
            if type(value) == list:
                for item in value:
                    element = etree.SubElement(movie, key)
                    element.text = item
            else:
                if key in ['plot', 'outline', 'originalplot']:
                    element = etree.SubElement(movie, key)
                    cdata = etree.CDATA(value)
                    element.text = cdata
                else:
                    element = etree.SubElement(movie, key)
                    element.text = value
        return movie
