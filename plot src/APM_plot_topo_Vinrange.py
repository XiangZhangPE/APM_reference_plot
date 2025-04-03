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
bar_width = 0.08  # 设置柱子的宽度

# 遍历所有的 topologyNames 并绘制各类柱状图
for g in range(len(topologyNames)):
    idx = topology_labels == str(g + 1)  # 将拓扑索引转换为字符串
    vin_min_data = vin_min[idx]
    vin_max_data = vin_max[idx]
    
    # 去除 NaN 值以确保数据大小一致
    valid_data = pd.concat([vin_min_data, vin_max_data], axis=1).dropna()
    vin_min_data = valid_data['Vin_min']
    vin_max_data = valid_data['Vin_max']

    # # 绘制柱状图，设置透明度
    # for vin_min_val, vin_max_val in zip(vin_min_data, vin_max_data):
    #     plt.bar(g, vin_max_data.mean() - vin_min_data.mean(), bottom=vin_min_data.mean(), 
    #     color=topologyColors[g], alpha=alpha_dots, label=f"{topologyNames[g]}", edgecolor='black')

    # # 绘制每一个柱子，重叠
    # for vin_min_val, vin_max_val in zip(vin_min_data, vin_max_data):
    #     plt.bar(g, vin_max_val - vin_min_val, bottom=vin_min_val, 
    #             color=topologyColors[g], alpha=alpha_dots, edgecolor='black')

    # 绘制每一个柱子不重叠
    for i, (vin_min_val, vin_max_val) in enumerate(zip(vin_min_data, vin_max_data)):
        plt.bar(g + i * bar_width, vin_max_val - vin_min_val, bottom=vin_min_val, 
                width=bar_width, color=topologyColors[g], alpha=alpha_dots, edgecolor='black')

# 设置标签、标题和网格
ax.set_ylabel('Vin Range (V)', fontproperties=font_prop, fontsize=12)
ax.set_xlabel('Topologies', fontproperties=font_prop, fontsize=12)
ax.grid(visible=True, linestyle='--', linewidth=0.5)  # 设置虚线网格

# 设置轴刻度字体
ax.tick_params(axis='x', labelsize=10, labelrotation=0)
ax.tick_params(axis='y', labelsize=10, labelrotation=0)

# 设置 x 轴刻度和标签
ax.set_xticks(range(len(topologyNames)))
ax.set_xticklabels(topologyNames, fontproperties=font_prop, fontsize=10)

# 保存图像为高清 PNG 文件
plt.savefig('outputs/topo2vinrange.png', dpi=1200, bbox_inches='tight')
plt.show()