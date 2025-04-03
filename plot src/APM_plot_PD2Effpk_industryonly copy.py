import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text
import matplotlib.font_manager as fm

# 读取 CSV 文件
data = pd.read_csv('data/parsed_data.csv')

# Use Cambria font for all text
font_prop = fm.FontProperties(family='Cambria')

# Define colors for different groups
groupColors = {'industrial': '#d81159', 'oem': '#79902e'}
groupMarkers = {'industrial': '^', 'oem': 'D'}
alpha_dots = 0.3
alpha_text = 0.9

# Create empty lists to store data points for each group
industrial_x, industrial_y = [], []
oem_x, oem_y = [], []

# 设置图像的输出比例为16:9
fig, ax = plt.subplots(figsize=(19, 9))
plt.figure
texts = []  # 用于存储注释对象，便于后面调整位置

# Loop through data and classify points
for i in range(len(data)):
    year_value = data.loc[i, 'Year']
    institution_value = data.loc[i, 'Institution']
    refnumber_value = data.loc[i, 'Refnumber']
    power_value = data.loc[i, 'Power']
    density_value = data.loc[i, 'Density']
    eff_pk_value = data.loc[i, 'Eff_pk']

    # Assign what to plot as x and y value
    x_value = density_value
    y_value = eff_pk_value

    # Classify the institution into a group
    if pd.notna(institution_value) and 'industry' in str(institution_value).lower():
        group = 'industrial'
        color = groupColors['industrial']
        marker = groupMarkers['industrial']
        industrial_y.append(y_value)
        industrial_x.append(x_value)
    elif pd.isna(institution_value) or institution_value == '':
        # group = 'oem'
        # color = groupColors['oem']
        # marker = groupMarkers['oem']
        # oem_y.append(y_value)
        # oem_x.append(x_value)

        # Skip oem points (do not plot them)
        continue
    else:
        # Skip academia points (do not plot them)
        continue

    # Add annotations
    if pd.notna(year_value):
        # year_int = int(year_value)
        # year_str = str(year_int)[-2:]

        year_str = str(int(year_value))
    else: 
        year_str = ""

    # Clean up institution name
    institution_cleaned = str(institution_value)
    if 'industry' in institution_cleaned.lower():
        institution_cleaned = institution_cleaned.replace('industry', '').replace('Industry', '').strip()

    # Only add annotations for valid points
    if pd.notna(y_value) and pd.notna(x_value) and np.isfinite(y_value) and np.isfinite(x_value):
        # Plot points with semi-transparency (alpha=0.6)
        plt.scatter(x_value, y_value, color=color, marker=marker, alpha=alpha_dots)  # Adjusted transparency
        if pd.notna(refnumber_value):
            refnumber_str = f"[{int(refnumber_value)}]"
            texts.append(plt.annotate(f"{institution_cleaned}\n{year_str} {refnumber_str}",
                            (x_value, y_value),
                            fontsize=12, alpha=alpha_text, ha='center', fontproperties=font_prop))
        else:
            texts.append(plt.annotate(f"{institution_cleaned}\n{year_str}",
                            (x_value, y_value),
                            fontsize=12, alpha=alpha_text, ha='center', fontproperties=font_prop))

# Scatter for industrial and oem groups with semi-transparent points
plt.scatter(industrial_x, industrial_y, color='#d81159', alpha=alpha_dots, marker='^', label='Industrial')
# plt.scatter(oem_x, oem_y, color='#79902e', alpha=alpha_dots, marker='D', label='OEM')

# Set title, labels, and legend
plt.ylabel('Peak Efficiency (%)', fontproperties=font_prop, fontsize=12)
plt.xlabel('Power Density (kW/L)', fontproperties=font_prop, fontsize=12)
plt.legend(prop=font_prop, fontsize=10)  # Removed title='Institution Group'
plt.grid(visible=True, linestyle='--', linewidth=0.5)

# Apply Cambria to axis ticks
plt.xticks(fontproperties=font_prop, fontsize=10)
plt.yticks(fontproperties=font_prop, fontsize=10)

# 设置 x 轴和 y 轴的范围
plt.xscale('log')  # X 轴为对数刻度
plt.xlim(0, 10)
# plt.ylim(0, 9)

# 调整文本以避免重叠
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='grey', lw=0.6))
# adjust_text(texts, 
#             arrowprops=dict(arrowstyle='->', color='grey', lw=1, shrinkA=0, shrinkB=0),
#             expand_text=(0.5, 0.5), 
#             expand_points=(0.5, 0.5))

# Save and show the plot
plt.savefig('outputs/PD2Eff_pk_oem.png', dpi=600, bbox_inches='tight')
plt.show()
