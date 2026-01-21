import pandas as pd
import numpy as np

class DataAnalyzer:
    """数据分析器"""

    def __init__(self, data):
        self.data = data

    def basic_statistics(self):
        """基础统计分析"""
        stats = {}
        for column in ['temperature', 'humidity', 'pm25']:
            stats[column] = {
                '均值': self.data[column].mean(),
                '中位数': self.data[column].median(),
                '标准差': self.data[column].std(),
                '最小值': self.data[column].min(),
                '最大值': self.data[column].max()
            }
        return pd.DataFrame(stats).T

    def location_analysis(self):
        """按站点分析"""
        return self.data.groupby('location').agg({
            'temperature': ['mean', 'std'],
            'humidity': ['mean', 'std'],
            'pm25': ['mean', 'std', 'max']
        }).round(2)

    def time_trend(self):
        """时间趋势分析"""
        daily_avg = self.data.groupby(self.data['date'].dt.date).agg({
            'temperature': 'mean',
            'humidity': 'mean',
            'pm25': 'mean'
        }).reset_index()
        return daily_avg

    def air_quality_assessment(self):
        """空气质量评估"""
        def get_aqi_level(pm25):
            if pm25 <= 35:
                return '优'
            elif pm25 <= 75:
                return '良'
            elif pm25 <= 115:
                return '轻度污染'
            elif pm25 <= 150:
                return '中度污染'
            elif pm25 <= 250:
                return '重度污染'
            else:
                return '严重污染'

        self.data['air_quality'] = self.data['pm25'].apply(get_aqi_level)

        quality_count = self.data['air_quality'].value_counts()
        good_days = (self.data['pm25'] <= 75).sum()

        return {
            'quality_distribution': quality_count,
            'good_days_ratio': f"{good_days/len(self.data)*100:.1f}%"
        }

    def temperature_extremes(self):
        """温度极值分析"""
        hot_days = self.data[self.data['temperature'] > 30]
        cold_days = self.data[self.data['temperature'] < 15]

        return {
            '高温天数': len(hot_days),
            '低温天数': len(cold_days),
            '最高温日期': self.data.loc[self.data['temperature'].idxmax(), 'date'],
            '最低温日期': self.data.loc[self.data['temperature'].idxmin(), 'date']
        }

# 测试代码
if __name__ == '__main__':
    from data_loader import DataLoader

    loader = DataLoader()
    data = loader.load_data()

    analyzer = DataAnalyzer(data)

    print("=== 基础统计分析 ===")
    print(analyzer.basic_statistics())

    print("\n=== 站点分析 ===")
    print(analyzer.location_analysis())

    print("\n=== 空气质量评估 ===")
    print(analyzer.air_quality_assessment())

    print("\n=== 温度极值分析 ===")
    print(analyzer.temperature_extremes())
