# src/data_loader.py
import pandas as pd
import os
# 从项目根目录导入utils（注意路径：.. 表示上级目录）
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_data_path

class DataLoader:
    """数据加载器（可移植版）"""

    def __init__(self):
        # 只用“相对于项目根目录”的路径，不写绝对路径/当前目录路径
        self.data_path = get_data_path('data/sensor_data.csv')
        self.data = None

    def load_data(self):
        """加载CSV数据"""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(
                f"数据文件不存在: {self.data_path}\n请先运行 data/generate_data.py 生成数据！"
            )

        self.data = pd.read_csv(self.data_path, encoding='utf-8')
        self.data['date'] = pd.to_datetime(self.data['date'])
        return self.data

    def get_data(self):
        """获取数据"""
        if self.data is None:
            self.load_data()
        return self.data

    def get_summary(self):
        """获取数据摘要"""
        if self.data is None:
            self.load_data()
        return {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'date_range': (self.data['date'].min(), self.data['date'].max()),
            'locations': self.data['location'].unique().tolist()
        }

# 测试代码
if __name__ == '__main__':
    try:
        loader = DataLoader()
        data = loader.load_data()
        print("✅ 数据加载成功！")
        print(data.head())
        print("\n📊 数据摘要:")
        for key, value in loader.get_summary().items():
            print(f"{key}: {value}")
    except FileNotFoundError as e:
        print(f"❌ 错误：{e}")