import json
import csv
import re
import pandas as pd

## 该文献运行前需求：output.bbl, APM_review_betterbib_xiang.json, APM_review_data_raw文件
## 该文件运行结束后可以得到APM_review_good_xiang.csv文件, 还会生成APM_reviw_temp.csv中间文件

## .bbl 文件是通过overleaf导出的reference编号文件，包含引文输出编号refnumber和引用索引citeKey !!! use overleaf Download other logs and output files to get it
## .json 文件是通过betterbibtex json功能导出的全部引用库，包含真实索引itemKey和引用索引citeKey !!! remember to enble 'item' option when export
## .csv 文件是通过zotero自带的csv功能导出的全部引用库，包含真实索引itemKey，但是不包含索引citeKey吗（raw文件） !!! use self-editted csv.json file to do csv export
## APM_reviw_temp.csv 是中间文件，用来匹配.bbl和.json文件，用于最终修饰输出.csv用的 ! dont need to mind it


# 1. 读取 .bbl 文件并提取 citationKey 和 Number
with open('output.bbl', 'r') as bbl_file:
    content = bbl_file.read()

# 使用正则表达式匹配 citationKey 和编号
pattern = r'\\bibitem\{([^}]+)\}'  # 匹配 \bibitem{citekey}
bbl_data = {match: i for i, match in enumerate(re.findall(pattern, content), start=1)}

# 2. 读取 JSON 文件并提取 citationKey 和 itemKey
json_file_path = 'APM_review_betterbib_xiang.json'
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

json_data = {item.get("citationKey"): item.get("itemKey") for item in data.get("items", []) if item.get("citationKey") and item.get("itemKey")}

# 整合数据
all_keys = set(bbl_data.keys()).union(json_data.keys())

# 3. 创建融合后的 CSV 文件 (暂时文件)
with open('APM_review_bib_temp.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["citationKey", "itemKey", "Number"])  # 写入表头
    for key in all_keys:
        writer.writerow([key, json_data.get(key, ""), bbl_data.get(key, "")])



# 3. 再次处理

# Load the two CSV files
file1_path = 'APM_review_rawcsv_xiang.csv'
file2_path = 'APM_review_bib_temp.csv'

# Reading both CSV files
df_xiang = pd.read_csv(file1_path)
df_numbered_xiang = pd.read_csv(file2_path)

# Perform the merge based on 'Key' in df_xiang and 'itemKey' in df_numbered_xiang
# Adding 'citationKey' and 'Number' columns from df_numbered_xiang to df_xiang based on matching rows
merged_df = df_xiang.merge(df_numbered_xiang[['itemKey', 'citationKey', 'Number']], 
                           left_on='Key', right_on='itemKey', how='left')

# Dropping the redundant 'itemKey' column after merge to keep the structure similar to df_xiang
merged_df.drop(columns=['itemKey'], inplace=True)

# Display the first few rows of the merged dataframe to verify the results
print(merged_df.head())

# Optionally, save the merged result to a new CSV file
merged_df.to_csv('APM_review_good_xiang.csv', index=False)
