import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text
import matplotlib.font_manager as fm

# 读取 CSV 文件
data = pd.read_csv('data/parsed_data.csv')

print(data.columns)
      
# 提取所需列
year = data['Year']
institution = data['Institution']
refnumber = data['Refnumber']
vomin = data['Vo_min']
vomax = data['Vo_max']
fs_min = data['fs_min']
fs_max = data['fs_max']
power = data['Power']
density = data['Density']
eff_pk = data['Eff_pk']
eff_avg = data['Eff_avg']


# Use Times New Roman font for all text
# font_prop = fm.FontProperties(family='Times New Roman')
font_prop = fm.FontProperties(family='Cambria')

# Define colors for different groups
groupColors = {'industrial': '#d81159', 'oem': '#79902e', 'academia': '#30517c'}
groupMarkers = {'industrial': '^', 'oem': 'D', 'academia': 'o'}
alpha_dots = 0.3
alpha_text = 0.9

# Create empty lists to store data points for each group
industrial_x, industrial_y = [], []
oem_x, oem_y = [], []
academia_x, academia_y = [], []

# List to store annotation texts
texts = []

# Assume data is your DataFrame
# Loop through data and classify points
for i in range(len(data)):
    institution_value = data['Institution'].iloc[i]
    year_value = data['Year'].iloc[i]
    refnumber_value = data['Refnumber'].iloc[i]

    # Classify the institution into a group
    if pd.notna(institution_value) and 'industry' in str(institution_value).lower():
        group = 'industrial'
        color = groupColors['industrial']
        marker = groupMarkers['industrial']
        industrial_x.append(density.iloc[i])
        industrial_y.append(eff_avg.iloc[i])
    elif pd.isna(institution_value) or institution_value == '':
        group = 'oem'
        color = groupColors['oem']
        marker = groupMarkers['oem']
        oem_x.append(density.iloc[i])
        oem_y.append(eff_avg.iloc[i])
    else:
        group = 'academia'
        color = groupColors['academia']
        marker = groupMarkers['academia']
        academia_x.append(density.iloc[i])
        academia_y.append(eff_avg.iloc[i])
    
    # Add annotations
    if pd.notna(year_value):
        year_int = int(year_value)
        year_str = str(year_int)[-2:]
    else: 
        year_str = ""

    # Clean up institution name
    institution_cleaned = str(institution_value)
    if 'industry' in institution_cleaned.lower():
        institution_cleaned = institution_cleaned.replace('industry', '').replace('Industry', '').strip()

    density_value = data['Density'].iloc[i]
    eff_avg_value = data['Eff_avg'].iloc[i]

    # Only add annotations for valid points
    if pd.notna(density_value) and pd.notna(eff_avg_value) and np.isfinite(density_value) and np.isfinite(eff_avg_value):
        # Plot points with semi-transparency (alpha=0.6)
        plt.scatter(eff_avg_value, density_value, color=color, marker=marker, alpha=alpha_dots)  # Adjusted transparency
        if pd.notna(refnumber_value):
            refnumber_str = f"[{int(refnumber_value)}]"
            texts.append(plt.annotate(f"{institution_cleaned}\n{year_str} {refnumber_str}",
                            (eff_avg_value, density_value),
                            fontsize=9, alpha=alpha_text, ha='center', fontproperties=font_prop))
        else:
            texts.append(plt.annotate(f"{institution_cleaned}\n{year_str}",
                            (eff_avg_value, density_value),
                            fontsize=9, alpha=alpha_text, ha='center', fontproperties=font_prop))


# Scatter for different groups with semi-transparent points
plt.scatter(industrial_y, industrial_x, color='#d81159', alpha=alpha_dots, marker='^', label='Industrial')
plt.scatter(oem_y, oem_x, color='#79902e', alpha=alpha_dots, marker='D', label='OEM')
plt.scatter(academia_y, academia_x, color='#30517c', alpha=alpha_dots, marker='o', label='Academia')

# Set title, labels, and legend with Times New Roman font
plt.xlabel('Average Efficiency (%)', fontproperties=font_prop, fontsize=12)
plt.ylabel('Power Density (kW/L)', fontproperties=font_prop, fontsize=12)
plt.legend(prop=font_prop, fontsize=10)  # Removed title='Institution Group'
plt.grid(visible=True, linestyle='--',linewidth=0.5 )  # 设置虚线网格

# Apply Times New Roman to axis ticks
plt.xticks(fontproperties=font_prop, fontsize=10)
plt.yticks(fontproperties=font_prop, fontsize=10)

# 设置 x 轴和 y 轴的范围
plt.xlim(0.895, 0.97)  # 替换 x_min 和 x_max 为你希望的范围
plt.ylim(0, 9)  # 替换 y_min 和 y_max 为你希望的范围

# Adjust annotations to avoid overlap
if texts:
    # adjust_text(texts,arrowprops=dict(arrowstyle='->',color='grey',lw=1))
    adjust_text(texts,arrowprops=dict(arrowstyle='->',color='grey',lw=0.5))

plt.savefig('Eff_avg2PD.png', dpi=300, bbox_inches='tight')

plt.show()

