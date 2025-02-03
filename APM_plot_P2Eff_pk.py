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

# 设置图像的输出比例为16:9
fig, ax = plt.subplots(figsize=(10, 8))
# fig, ax = plt.subplots()
plt.figure
texts = []  # 用于存储注释对象，便于后面调整位置

# Assume data is your DataFrame
# Loop through data and classify points
for i in range(len(data)):

    year_value = year.iloc[i]
    institution_value = institution.iloc[i]
    refnumber_value = refnumber.iloc[i] 
    power_value = power.iloc[i]
    density_value = density.iloc[i]
    eff_pk_value = eff_pk.iloc[i]
    eff_avg_value = eff_avg.iloc[i]

    # Assign what to plot as x and y value
    x_value = power_value
    y_value = eff_pk_value

    # Classify the institution into a group
    if pd.notna(institution_value) and 'industry' in str(institution_value).lower():
        group = 'industrial'
        color = groupColors['industrial']
        marker = groupMarkers['industrial']
        industrial_y.append(y_value)
        industrial_x.append(x_value)
    elif pd.isna(institution_value) or institution_value == '':
        group = 'oem'
        color = groupColors['oem']
        marker = groupMarkers['oem']
        oem_y.append(y_value)
        oem_x.append(x_value)
    else:
        group = 'academia'
        color = groupColors['academia']
        marker = groupMarkers['academia']
        academia_y.append(y_value)
        academia_x.append(x_value)
    
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


    # Only add annotations for valid points
    if pd.notna(y_value) and pd.notna(x_value) and np.isfinite(y_value) and np.isfinite(x_value):
        # Plot points with semi-transparency (alpha=0.6)
        plt.scatter(x_value, y_value, color=color, marker=marker, alpha=alpha_dots)  # Adjusted transparency
        if pd.notna(refnumber_value):
            refnumber_str = f"[{int(refnumber_value)}]"
            texts.append(plt.annotate(f"{institution_cleaned}\n{year_str} {refnumber_str}",
                            (x_value, y_value),
                            fontsize=9, alpha=alpha_text, ha='center', fontproperties=font_prop))
        else:
            texts.append(plt.annotate(f"{institution_cleaned}\n{year_str}",
                            (x_value, y_value),
                            fontsize=9, alpha=alpha_text, ha='center', fontproperties=font_prop))
            


# Scatter for different groups with semi-transparent points
plt.scatter(industrial_x, industrial_y, color='#d81159', alpha=alpha_dots, marker='^', label='Industrial')
plt.scatter(oem_x, oem_y, color='#79902e', alpha=alpha_dots, marker='D', label='OEM')
plt.scatter(academia_x, academia_y, color='#30517c', alpha=alpha_dots, marker='o', label='Academia')

# Set title, labels, and legend with Times New Roman font
plt.ylabel('Peak Efficiency (%)', fontproperties=font_prop, fontsize=12)
plt.xlabel('Power (kW)', fontproperties=font_prop, fontsize=12)
plt.legend(prop=font_prop, fontsize=10)  # Removed title='Institution Group'
plt.grid(visible=True, linestyle='--',linewidth=0.5 )  # 设置虚线网格

# Apply Times New Roman to axis ticks
plt.xticks(fontproperties=font_prop, fontsize=10)
plt.yticks(fontproperties=font_prop, fontsize=10)

# Set x-axis to logarithmic scale plt.xscale('log')
# plt.xscale('log')

# Adjust annotations to avoid overlap
if texts:
    adjust_text(texts,arrowprops=dict(arrowstyle='->',color='grey',lw=0.5))

plt.savefig('outputs/P2Eff_pk_field.png', dpi=300, bbox_inches='tight')

plt.show()
