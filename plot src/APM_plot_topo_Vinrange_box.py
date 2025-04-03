import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text
import matplotlib.font_manager as fm

# 读取数据
data = pd.read_csv('data/parsed_data.csv')
data_fbps = pd.read_csv('data/fbps.csv', dtype=str)
data_dab = pd.read_csv('data/dab.csv', dtype=str)
data_llc = pd.read_csv('data/llc.csv', dtype=str)
data_cfdab = pd.read_csv('data/cfdab.csv', dtype=str)
data_dabsrc = pd.read_csv('data/dabsrc.csv', dtype=str)
data_2stage = pd.read_csv('data/2stage.csv', dtype=str)

# 提取数据
year = data['Year']
institution = data['Institution']
refnumber = data['Refnumber']
density = pd.to_numeric(data['Density'], errors='coerce')
eff_avg = pd.to_numeric(data['Eff_avg'], errors='coerce')
eff_pk = pd.to_numeric(data['Eff_pk'], errors='coerce')
vin_max = pd.to_numeric(data['Vin_max'], errors='coerce')
vin_min = pd.to_numeric(data['Vin_min'], errors='coerce')


mainVec = data['RealKey']

# 定义子列向量
subVecs = [data_fbps['Key'], data_dab['Key'], data_llc['Key'], data_cfdab['Key'], data_dabsrc['Key'], data_2stage['Key']]

# 创建用于存储来源子列的索引
sourceIdx = np.zeros(len(mainVec), dtype=int)
for i, subVec in enumerate(subVecs, 1):  # 从 1 开始索引
    matches = mainVec.isin(subVec)
    sourceIdx[matches] = i

# 将 sourceIdx 转换为字符串格式的标签
topology_labels = np.array(sourceIdx, dtype=str)

# 定义拓扑名称和颜色列表
topologyNames = ['FBPS', 'DAB', 'LLC', 'Current-Fed', 'DAB-src', '2-Stage']  # 拓扑名称
topologyColors = ['#D32F2F',  # 红色
                  '#CC9900',  # 金色
                  '#6633FF', # 紫色
                  '#006633', # 深绿色
                  '#024CAA', # 蓝色
                  '#32E0C4' # 
                  ]   

topologyMarkers = ['o',  # 圆形
                  'D',  # 菱形
                  '^', # 上三角形
                  's', # 方形
                  'D', # 菱形
                  'v', ]  # 下三角形

# 设置 Times New Roman 字体
# font_prop = fm.FontProperties(family='Times New Roman')
font_prop = fm.FontProperties(family='Cambria')
alpha_dots = 0.4
alpha_text = 0.9

# 设置图像的输出比例
fig, ax = plt.subplots(figsize=(5, 9))
texts = []  # 用于存储注释对象，便于后面调整位置

# 创建一个列表存储每个拓扑的电压范围数据，用于箱线图
vin_range_data = []
labels = []

# 遍历所有的 topologyNames 并收集数据
for g in range(len(topologyNames)):
    idx = topology_labels == str(g + 1)  # 将拓扑索引转换为字符串
    vin_min_data = vin_min[idx]
    vin_max_data = vin_max[idx]
    
    # 去除 NaN 值以确保数据大小一致
    valid_data = pd.concat([vin_min_data, vin_max_data], axis=1).dropna()
    vin_min_data = valid_data['Vin_min']
    vin_max_data = valid_data['Vin_max']
    
    # 计算电压范围 (Vin_max - Vin_min)
    vin_range = abs( vin_max_data - vin_min_data)
    
    # 添加到列表中
    if len(vin_range) > 0:  # 确保有数据
        vin_range_data.append(vin_range)
        labels.append(topologyNames[g])

# 创建箱线图
boxplot = ax.boxplot(vin_range_data, patch_artist=True)

# 设置箱线图颜色
for i, box in enumerate(boxplot['boxes']):
    box.set(color=topologyColors[i], alpha=alpha_dots)
    box.set(facecolor=topologyColors[i], alpha=alpha_dots)
    
# 设置线条颜色
for i, element in enumerate(boxplot['medians']):
    element.set(color='black', linewidth=1.5)
    
for i, element in enumerate(boxplot['whiskers']):
    element.set(color='black', linewidth=1)
    
for i, element in enumerate(boxplot['caps']):
    element.set(color='black', linewidth=1)
    
for i, element in enumerate(boxplot['fliers']):
    element.set(marker='o', markerfacecolor=topologyColors[i], markersize=6, 
                alpha=alpha_dots, markeredgecolor='black')

# 设置标签、标题和网格
ax.set_ylabel('Input Voltage Range (Vin-Vo) /V', fontproperties=font_prop, fontsize=12)
ax.grid(visible=True, linestyle='--', linewidth=0.5)  # 设置虚线网格

# 设置轴刻度字体
ax.tick_params(axis='y', labelsize=10, labelrotation=0)

# 设置 x 轴刻度和标签
ax.set_xticks(range(1, len(labels) + 1))
ax.set_xticklabels(labels, fontproperties=font_prop, fontsize=10, rotation=45, ha='right')

# 保存图像为高清 PNG 文件
plt.savefig('outputs/topo_vinrange_boxplot.png', dpi=1200, bbox_inches='tight')
plt.show()