import matplotlib.pyplot as plt

# 设置字体为 DejaVu Sans，这是一个支持法文字母的字体
plt.rcParams['font.family'] = 'Cambria'

# 测试绘图
plt.text(0.5, 0.5, 'Bonjour, ça va ?', ha='center', va='center', fontsize=20)
plt.show()
