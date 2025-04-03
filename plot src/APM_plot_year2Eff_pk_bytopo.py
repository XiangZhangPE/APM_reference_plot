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
fs_min = pd.to_numeric(data['fs_min'], errors='coerce')
density = pd.to_numeric(data['Density'], errors='coerce')
eff_avg = pd.to_numeric(data['Eff_avg'], errors='coerce')
eff_pk = pd.to_numeric(data['Eff_pk'], errors='coerce')


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

# 设置字体
font_prop = fm.FontProperties(family='Cambria')
alpha_dots = 0.4
alpha_text = 0.9

# 设置图像尺寸
fig, ax = plt.subplots(figsize=(12, 4))
# fig, ax = plt.subplots()  # 不指定 figsize，使用默认尺寸
texts = []


# 遍历所有拓扑并绘制散点
for g in range(len(topologyNames)):
    idx = topology_labels == str(g + 1)

    # 过滤数据，确保数据不含 NaN
    valid_mask = idx & year.notna() & eff_pk.notna()
    
    x_data = year[valid_mask]
    y_data = eff_pk[valid_mask]
    inst_data = institution[valid_mask]
    ref_data = refnumber[valid_mask]

    # 清理 institution 和 year_data 数据
    cleaned_institution = []

    for inst, yr in zip(inst_data, x_data):
        # 清理 institution 中的 "industry" 并移除多余空格
        inst_cleaned = str(inst)
        if 'industry' in inst_cleaned.lower():
            inst_cleaned = inst_cleaned.replace('industry', '').replace('Industry', '').strip()
        cleaned_institution.append(inst_cleaned)

    if len(x_data) == 0:
        continue  # 跳过无数据的情况

    plt.scatter(x_data, y_data, s=40, c=topologyColors[g], marker=topologyMarkers[g], alpha=alpha_dots, label=f"{topologyNames[g]}")

    # 添加注释
    # for xi, yi, inst, ref in zip(x_data, y_data, inst_data, ref_data):
    for xi, yi, inst, ref in zip(x_data, y_data, cleaned_institution, ref_data):
        annotation_text = f"{inst}\n[{ref}]"
        texts.append(plt.text(xi, yi, annotation_text, fontsize=10, ha='center', alpha=alpha_text, fontproperties=font_prop))

# 调整文本防止重叠
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='grey', lw=0.5))

# 设置坐标轴
ax.set_xlabel('Year', fontproperties=font_prop, fontsize=12)
ax.set_ylabel('Peak Efficiency (%)', fontproperties=font_prop, fontsize=12)
# ax.legend(prop=font_prop, fontsize=10, loc='upper left')
ax.legend(prop=font_prop, fontsize=10, loc='best')
ax.grid(visible=True, linestyle='--', linewidth=0.5)

# 设置 X 轴主刻度的间隔为 2 年
import matplotlib.ticker as ticker
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))


# 限制 X 轴范围
ax.set_xlim(year.min(), year.max()+1)

# 保存图像
plt.savefig('outputs/year2Eff_pk_topo.png', dpi=300, bbox_inches='tight')
plt.show()
