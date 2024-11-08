import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
import matplotlib.font_manager as fm

# 读取数据
data = pd.read_csv('data/parsed_data.csv')
data_fbps = pd.read_csv('data/fbps.csv', dtype=str)
data_dab = pd.read_csv('data/dab.csv', dtype=str)
data_llc = pd.read_csv('data/llc.csv', dtype=str)
data_cfdab = pd.read_csv('data/cfdab.csv', dtype=str)

# 提取数据
year = data['Year']
institution = data['Institution']
refnumber = data['Refnumber']
fs_min = pd.to_numeric(data['fs_min'], errors='coerce')
density = pd.to_numeric(data['Density'], errors='coerce')
eff_avg = pd.to_numeric(data['Eff_avg'], errors='coerce')


mainVec = data['RealKey']

# 定义子列向量
subVecs = [data_fbps['Key'], data_dab['Key'], data_llc['Key'], data_cfdab['Key']]

# 创建用于存储来源子列的索引
sourceIdx = np.zeros(len(mainVec), dtype=int)
for i, subVec in enumerate(subVecs, 1):  # 从 1 开始索引
    matches = mainVec.isin(subVec)
    sourceIdx[matches] = i

# 将 sourceIdx 转换为字符串格式的标签
topology_labels = np.array(sourceIdx, dtype=str)

# 定义拓扑名称和颜色列表
topologyNames = ['FBPS', 'DAB', 'Resoannt', 'Current-Fed']  # 拓扑名称
topologyColors = ['#D32F2F',  # 红色
                  '#CC9900',  # 金色
                  '#6633FF', # 紫色
                  '#006633']   # 深绿色

topologyMarkers = ['o',  # 圆形
                  'D',  # 菱形
                  '^', # 上三角形
                  's']   # 方形

# 设置 Times New Roman 字体
# font_prop = fm.FontProperties(family='Times New Roman')
font_prop = fm.FontProperties(family='Cambria')
alpha_dots = 0.4
alpha_text = 0.9

# 创建图形
# plt.figure(figsize=(10, 6))
plt.figure
texts = []  # 用于存储注释对象，便于后面调整位置

# 遍历所有的 topologyNames 并绘制各类散点
for g in range(len(topologyNames)):
    idx = topology_labels == str(g + 1)  # 将拓扑索引转换为字符串
    x_data = fs_min[idx]
    y_data = density[idx]
    inst_data = institution[idx]
    year_data = year[idx]
    ref_data = refnumber[idx]
    
    # 去除 NaN 值以确保 x_data 和 y_data 大小一致
    valid_data = pd.concat([x_data, y_data, inst_data, year_data, ref_data], axis=1).dropna()
    x_data, y_data = valid_data['fs_min'], valid_data['Density']
    inst_data = valid_data['Institution']
    year_data = valid_data['Year']
    ref_data = valid_data['Refnumber']
    
    # 清理 institution 和 year_data 数据
    cleaned_institution = []
    cleaned_year_data = []
    
    for inst, yr in zip(inst_data, year_data):
        # 清理 institution 中的 "industry" 并移除多余空格
        inst_cleaned = str(inst)
        if 'industry' in inst_cleaned.lower():
            inst_cleaned = inst_cleaned.replace('industry', '').replace('Industry', '').strip()
        cleaned_institution.append(inst_cleaned)

        # 提取 year 的后两位
        if pd.notna(yr):
            yr_str = str(int(yr))[-2:]  # 仅取后两位
            cleaned_year_data.append(yr_str)
        else:
            cleaned_year_data.append("")

    # 绘制散点图，设置标记透明度
    plt.scatter(x_data, y_data, s=40, c=topologyColors[g], marker=topologyMarkers[g], alpha=alpha_dots, label=f"{topologyNames[g]}")
    
    # 添加注释，设置透明度
    for xi, yi, inst, yr, ref in zip(x_data, y_data, cleaned_institution, cleaned_year_data, ref_data):
        annotation_text = f"{inst}\n{yr} [{int(ref)}]"
        texts.append(plt.text(xi, yi, annotation_text, fontsize=9, ha='center', alpha=alpha_text, fontproperties=font_prop))

# 绘制回归线 regression analysis
sns.regplot(x=fs_min, y=density, ci=80, scatter_kws={"s": 20, "color": "blue", "alpha": 0}, line_kws={"color": "red", "linestyle": "--", "linewidth": 1})

# 调整文本以避免重叠
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='grey', lw=0.5))

# 设置标签、标题和网格
plt.xlabel('Nominal Switching Frequency (kHz)', fontproperties=font_prop, fontsize=12)
plt.ylabel('Power Density (kW/L)', fontproperties=font_prop, fontsize=12)
plt.legend(prop=font_prop, fontsize=10)
plt.grid(visible=True, linestyle='--',linewidth=0.5 )  # 设置虚线网格

# 设置 x 轴和 y 轴的范围
plt.xlim(40, 740)  # 替换 x_min 和 x_max 为你希望的范围
plt.ylim(0, 8.5)  # 替换 y_min 和 y_max 为你希望的范围

# 设置轴刻度字体
plt.xticks(fontproperties=font_prop, fontsize=10)
plt.yticks(fontproperties=font_prop, fontsize=10)

# 保存图像为高清 PNG 文件
plt.savefig('outputs/Fs2PD_regression.png', dpi=300, bbox_inches='tight')
plt.show()
