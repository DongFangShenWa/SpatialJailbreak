import pandas as pd

# 输入输出路径
tsv_path = '/Users/muzhiyi/Desktop/famous_dataset/alredy_harmful/ToxiCloakCN/Datasets/base_data.tsv'
output_json_path = '/Users/muzhiyi/Desktop/famous_dataset/alredy_harmful/toxicloakcn.json'

# 读取 TSV 文件（注意指定 sep='\t'）
df = pd.read_csv(tsv_path, sep='\t', on_bad_lines='skip')  # on_bad_lines 忽略格式错误行

# 过滤条件：
# 1. toxic == 1
# 2. content 字符长度 <= 10
filtered_df = df[(df['toxic'] == 1) & (df['content'].str.len() <= 10)]

# 将 DataFrame 转换为 JSON 格式并写入文件
filtered_df.to_json(
    output_json_path,
    orient='records',
    force_ascii=False,
    indent=2
)

print(f"成功提取并保存至: {output_json_path}")
