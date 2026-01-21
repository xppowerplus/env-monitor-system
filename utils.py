# utils.py（项目根目录下）
import os

def get_project_root():
    """
    动态获取项目根目录（无论脚本在哪个子文件夹运行，都能找到根目录）
    返回：项目根目录的绝对路径（可移植，不绑定具体盘符/用户）
    """
    # 当前文件（utils.py）的路径 → 就是项目根目录
    current_path = os.path.abspath(__file__)
    project_root = os.path.dirname(current_path)
    return project_root

def get_data_path(relative_path):
    """
    拼接“项目根目录 + 相对路径”
    参数：relative_path - 相对于项目根目录的路径（比如 'data/sensor_data.csv'）
    返回：可移植的绝对路径
    """
    project_root = get_project_root()
    return os.path.join(project_root, relative_path)