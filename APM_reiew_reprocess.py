import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from adjustText import adjust_text
import matplotlib.font_manager as fm

## 该文献运行前需求：APM_review_good_xiang.csv文件
## 该文件运行结束后可以得到parsed_data.csv文件（用于画图的元数据）

# 读取 CSV 文件
data = pd.read_csv('data/APM_review_good_xiang.csv')

print(data.columns)
      
# 提取所需列
col11 = data['Archive']  # 假设第11列的列名是 "Archive"
col12 = data['Archive Location']  # 假设第12列的列名是 "Archive Location"
year = data['Publication Year']
institution = data['Rights']
realkey = data['Key']
citationkey = data['citationKey']
refnumber = data['Number']

# 初始化存储解析数据的变量
Power = [];
Density = [];
Vo = [];
Vin = [];
fs = [];
Eff_pk = [];
Eff_avg = [];
Eff_low = [];

for i in range(len(data)):
    # 初始化当前行的临时值
    vo_temp = [np.nan, np.nan]
    vin_temp = [np.nan, np.nan]
    fs_temp = [np.nan, np.nan]

    # 获取当前行的内容并检查是否为空
    col11_value = col11.loc[i]
    if pd.notna(col11_value):
        # 按逗号分隔字段
        parts11 = col11_value.split(',')

        # 解析每个字段的键和值
        for part in parts11:
            key, value = map(str.strip, part.split('='))
            
            # 根据键提取值并处理范围
            if key == 'Vo':
                if '-' in value:
                    vo_values = value.split('-')
                    vo_temp = [float(vo_values[0].replace('V', '')), float(vo_values[1].replace('V', ''))]
                else:
                    vo_temp = [float(value.replace('V', '')), np.nan]
            elif key == 'Vin':
                if '-' in value:
                    vin_values = value.split('-')
                    vin_temp = [float(vin_values[0].replace('V', '')), float(vin_values[1].replace('V', ''))]
                else:
                    vin_temp = [float(value.replace('V', '')), np.nan]
            elif key == 'fs':
                if '-' in value:
                    fs_values = value.split('-')
                    fs_temp = [float(fs_values[0].replace('kHz', '')), float(fs_values[1].replace('kHz', ''))]
                else:
                    fs_temp = [float(value.replace('kHz', '')), np.nan]

    # 将当前行的结果添加到最终列表
    Vo.append(vo_temp)
    Vin.append(vin_temp)
    fs.append(fs_temp)


# 逐行解析 `col12` 列的数据
for j in range(len(data)):
    # 初始化当前行的临时值
    power_temp = np.nan
    density_temp = np.nan
    eff_pk_temp = np.nan
    eff_avg_temp = np.nan

    # 检查当前行是否为空
    col12_value = col12.loc[j]
    if pd.notna(col12_value):
        # 按逗号分割每个字段
        parts12 = col12_value.split(',')

        # 处理每个字段
        for part in parts12:
            # 按等号分割键和值
            field = part.strip().split('=')
            if len(field) == 2:
                key = field[0].strip()
                value = field[1].strip()

                # 根据键名提取并处理对应的值
                if key == 'Power':
                    power_temp = float(re.sub(r'[kW]', '', value))
                elif key == 'PD':
                    density_temp = float(re.sub(r'[kW/L(case)]', '', value))
                elif key == 'Eff_pk':
                    eff_pk_temp = float(value)
                elif key == 'Eff_avg':
                    eff_avg_temp = float(value)
    
    # 将当前行的解析结果添加到最终列表中
    Power.append(power_temp)
    Density.append(density_temp)
    Eff_pk.append(eff_pk_temp)
    Eff_avg.append(eff_avg_temp)


# 将解析后的数据转为 DataFrame
parsed_data = pd.DataFrame({
    'Year': year,  # 加载 Publication Year 列
    'Institution': institution,  # 加载 Rights 列
    'RealKey': realkey,  # 加载 Key 列
    'Citationkey': citationkey,  # 加载 citationKey 列
    'Refnumber': refnumber,  # 加载 Number 列
    'Vo_min': [vo[0] for vo in Vo],
    'Vo_max': [vo[1] for vo in Vo],
    'Vin_min': [vin[0] for vin in Vin],
    'Vin_max': [vin[1] for vin in Vin],
    'fs_min': [f[0] for f in fs],
    'fs_max': [f[1] for f in fs],
    'Power': Power,
    'Density': Density,
    'Eff_pk': Eff_pk,
    'Eff_avg': Eff_avg
})

# 输出解析后的数据
print(parsed_data)
parsed_data.to_csv('data/parsed_data.csv', index=False)


# # 数据清洗（如果需要）
# # 例如，去掉所有包含 NaN 的行
# cleaned_data = parsed_data.dropna()

# # 保存清洗后的数据到新的 CSV 文件
# cleaned_data.to_csv('parsed_apm_data.csv', index=False)

# # 进一步分析示例（可选）
# # 计算 Power 和 Efficiency 的基本统计信息
# stats = cleaned_data[['Power', 'Eff_pk', 'Eff_avg']].describe()
# print(stats)

# 可视化


