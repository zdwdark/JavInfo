import os

# 定义支持的视频文件扩展名
VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mov', '.mkv')


def find_video_files(directory):
    """
    在指定目录及其子目录中搜索视频文件，并返回不包含扩展名的文件名列表。
    如果目录不存在或没有找到视频文件，返回相应的提示信息。
    :param directory: 要搜索的目录路径
    :return: 文件名列表或提示信息字符串
    """

    video_files = []
    # 遍历目录及其子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件扩展名
            if file.lower().endswith(VIDEO_EXTENSIONS):
                # 只保留文件名，不包含扩展名
                file_name, file_extension = os.path.splitext(file)
                file_info = {
                    'folder_path': root,  # 文件所在的文件夹路径
                    'file_name': file_name   # 文件名
                }
                video_files.append(file_info)

    # 检查是否找到视频文件
    if not video_files:
        return "No video files found in the specified directory."
    else:
        return video_files


'''
if __name__ == "__main__":
    directory_path = 'D:/Python/adata'
    print(f"Searching for video files in {directory_path}...")
    result = find_video_files(directory_path)
    print(result)

'''
