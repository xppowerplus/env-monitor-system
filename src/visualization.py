import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
# 导入通用工具（解决路径问题）
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_data_path

class DataVisualizer:
    """数据可视化器（可移植版）"""

    def __init__(self, data):
        self.data = data
        # 初始化时确保docs文件夹存在
        self.docs_dir = get_data_path('docs')
        if not os.path.exists(self.docs_dir):
            os.makedirs(self.docs_dir)
            print(f"✅ 创建docs文件夹：{self.docs_dir}")

    def plot_time_series(self, save_name='timeseries.png'):
        """绘制时间序列图（修复路径+字体）"""
        # 优化中文显示（兼容更多符号）
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.family'] = 'sans-serif'

        fig, axes = plt.subplots(3, 1, figsize=(12, 10))

        # 温度趋势
        axes[0].plot(self.data['date'], self.data['temperature'], marker='o', color='red')
        axes[0].set_title('温度变化趋势')
        axes[0].set_ylabel('温度(℃)')
        axes[0].grid(True)

        # 湿度趋势
        axes[1].plot(self.data['date'], self.data['humidity'], marker='s', color='blue')
        axes[1].set_title('湿度变化趋势')
        axes[1].set_ylabel('湿度(%)')
        axes[1].grid(True)

        # PM2.5趋势（替换上标³为普通文字，避免字体问题）
        axes[2].plot(self.data['date'], self.data['pm25'], marker='^', color='green')
        axes[2].set_title('PM2.5变化趋势')
        axes[2].set_ylabel('PM2.5(μg/m3)')  # 把³改成3，避免字体缺失
        axes[2].set_xlabel('日期')
        axes[2].grid(True)
        axes[2].axhline(y=75, color='orange', linestyle='--', label='良/轻度污染界线')
        axes[2].legend()

        plt.tight_layout()
        # 用可移植路径保存
        save_path = os.path.join(self.docs_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ 时间序列图已保存到 {save_path}")
        plt.show()

    def plot_distribution(self, save_name='distribution.png'):
        """绘制数据分布图（修复路径+字体）"""
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        # 温度分布
        axes[0, 0].hist(self.data['temperature'], bins=10, color='red', alpha=0.7)
        axes[0, 0].set_title('温度分布')
        axes[0, 0].set_xlabel('温度(℃)')

        # 湿度分布
        axes[0, 1].hist(self.data['humidity'], bins=10, color='blue', alpha=0.7)
        axes[0, 1].set_title('湿度分布')
        axes[0, 1].set_xlabel('湿度(%)')

        # PM2.5分布（替换上标³）
        axes[1, 0].hist(self.data['pm25'], bins=10, color='green', alpha=0.7)
        axes[1, 0].set_title('PM2.5分布')
        axes[1, 0].set_xlabel('PM2.5(μg/m3)')  # 把³改成3
        axes[1, 0].axvline(x=75, color='orange', linestyle='--', label='良/轻度污染界线')
        axes[1, 0].legend()

        # 站点对比
        location_avg = self.data.groupby('location')[['temperature', 'humidity', 'pm25']].mean()
        x = range(len(location_avg))
        width = 0.25
        axes[1, 1].bar([i - width for i in x], location_avg['temperature'], width, label='温度', color='red')
        axes[1, 1].bar(x, location_avg['humidity'], width, label='湿度', color='blue')
        axes[1, 1].bar([i + width for i in x], location_avg['pm25']/5, width, label='PM2.5/5', color='green')
        axes[1, 1].set_title('站点指标对比')
        axes[1, 1].set_xticks(x)
        axes[1, 1].set_xticklabels(location_avg.index)
        axes[1, 1].legend()

        plt.tight_layout()
        save_path = os.path.join(self.docs_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ 分布图已保存到 {save_path}")
        plt.show()

    def plot_correlation(self, save_name='correlation.png'):
        """绘制相关性热图（修复路径+字体）"""
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False

        corr = self.data[['temperature', 'humidity', 'pm25']].corr()

        plt.figure(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0,
                    square=True, linewidths=1)
        plt.title('环境指标相关性分析')
        plt.tight_layout()
        save_path = os.path.join(self.docs_dir, save_name)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ 相关性热图已保存到 {save_path}")
        plt.show()

# 测试代码
if __name__ == '__main__':
    from data_loader import DataLoader

    # 加载数据
    loader = DataLoader()
    data = loader.load_data()

    # 可视化
    visualizer = DataVisualizer(data)
    visualizer.plot_time_series()
    visualizer.plot_distribution()
    visualizer.plot_correlation()