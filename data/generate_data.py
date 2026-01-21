# data/generate_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
# 导入通用工具
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_data_path

# 设置随机种子
np.random.seed(42)

# 生成30天的传感器数据
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(30)]

# 生成模拟数据
data = {
    'date': dates,
    'temperature': np.random.normal(25, 5, 30),  # 温度：均值25，标准差5
    'humidity': np.random.normal(60, 10, 30),    # 湿度：均值60，标准差10
    'pm25': np.random.normal(50, 20, 30),         # PM2.5：均值50，标准差20
    'location': ['站点A']*15 + ['站点B']*15
}

df = pd.DataFrame(data)

# 确保数值在合理范围
df['humidity'] = df['humidity'].clip(0, 100)
df['pm25'] = df['pm25'].clip(0, 500)

# 用可移植路径保存
csv_path = get_data_path('data/sensor_data.csv')
df.to_csv(csv_path, index=False, encoding='utf-8')

print("✅ 传感器数据已生成！")
print(df.head())