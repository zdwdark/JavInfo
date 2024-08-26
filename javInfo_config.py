import json
import os
import requests
from PIL import Image
from io import BytesIO


class JavInfoConfig:

    def __init__(self):
        self.config_data = {}  # 存储配置信息
        self.config_file = "config.json"
        current_dir = os.getcwd()

        file_path = os.path.join(current_dir, self.config_file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:  # 创建配置文件
                json.dump(self.config_data, file)    # 写入默认配置信息
        else:
            with open(file_path, 'r') as file:  # 读取配置文件
                self.config_data = json.load(file)  # 加载配置信息

    def get_config(self, key):  # 获取配置信息
        if key in self.config_data:  # 判断配置信息是否存在
            return self.config_data[key]  # 返回配置信息
        else:
            return None

    def set_config(self, key, value):
        self.config_data[key] = value
        with open(self.config_file, 'w') as file:  # 写入配置文件
            json.dump(self.config_data, file)


class JaveData:

    def __init__(self):
        self.data = {}  # 存储jav信息

    def get_data(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    def add_data(self, key, value):
        self.data[key] = value


def save_pic(pic_url, pic_name, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    response = requests.get(pic_url, verify=False)
    if response.status_code == 200:
        # 使用 BytesIO 将图片数据转换为文件对象
        image_file = BytesIO(response.content)

        # 使用 PIL 打开图片文件对象
        image = Image.open(image_file)

        # 构建完整的保存路径
        full_path = save_path + '/' + pic_name

        # 保存图片到指定路径
        image.save(full_path)
        print(f"图片已保存到 {full_path}")
    else:
        print(f"图片下载失败，状态码：{response.status_code}")


"""
if __name__ == '__main__':
    config = JavInfoConfig()
    print(config.get_config("path"))

"""
