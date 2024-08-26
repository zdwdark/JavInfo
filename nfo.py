from lxml import etree
from javInfo_config import *


def create_movie_xml(javdata):

    # 创建根元素
    movie = etree.Element("movie")

    # 添加 XML 声明
    movie.attrib['{http://www.w3.org/2001/xmlschema-instance}schemaLocation'] = 'http://www.w3.org/2001/XMLSchema'
    movie.attrib['{http://www.w3.org/2001/xmlschema-instance}noNamespaceSchemaLocation'] = 'schema.xsd'

    # 辅助函数，用于添加 CDATA 元素
    def create_cdata_element(parent, tag, text):
        cdata_element = etree.SubElement(parent, tag)
        cdata = etree.CDATA(text)
        cdata_element.text = cdata

    for key, value in javdata.items():
        # 为字典的每个键创建一个子元素，并设置其文本内容为字典的值
        if type(value) == list:
            for item in value:
                element = etree.SubElement(movie, key)
                element.text = item
        else:
            element = etree.SubElement(movie, key)
            element.text = value

    return movie
