from javInfo_config import JavInfoConfig
from get_vedio_name import *
from serch_javdb import *
from nfo import *
import time

if __name__ == '__main__':
    config = JavInfoConfig()
    path = config.get_config('path')
    print(path)

    file_info = find_video_files(path)
    print(file_info)

    for fileinfo in file_info:
        print(fileinfo)
        javdata = javdbSerch(fileinfo)
        print(javdata)
        if javdata:
            xml_element = create_movie_xml(javdata)
            xml_str = etree.tostring(
                xml_element, pretty_print=True, encoding='utf-8').decode('utf-8')
            print(xml_str)
        time.sleep(3)
