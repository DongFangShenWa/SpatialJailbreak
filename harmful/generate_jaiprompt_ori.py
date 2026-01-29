import json
import re
from template import (  # 替换为你的脚本文件名（不带 .py）
    generate_acrostic,
    generate_telestich,
    generate_center,
    generate_corner,
    generate_staircase
)

# 输入输出路径
input_json_path = '/Users/muzhiyi/Desktop/famous_dataset/jailbreak_ori/original_already/policy_hate.json'
output_json_path = '/Users/muzhiyi/Desktop/famous_dataset/jailbreak_ori/jailbreak_already/policy_hate.json'

# 定义一个函数用于去除标点符号（含中英文标点）
def remove_punctuation(text):
    # 匹配所有标点符号（包括中文和英文）
    return re.sub(r'[^\w\s]', '', text)

# 读取原始 JSON 数据
with open(input_json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 存储处理后的数据
processed_data = []

# 对每个 item 进行处理
for item in data:
    harmful_question = item.get("text", "")

    if not harmful_question:
        continue  # 跳过空问题

    # 去除标点符号
    cleaned_question = remove_punctuation(harmful_question)

    jailbreaks = {
        "topic": "policy",#item.get("Category", "")+"\\"+item.get("Target Group", ""),
        "original": harmful_question,
        "cleaned": cleaned_question,  # 可选字段，保留清洗后的内容
        "acrostic": generate_acrostic(cleaned_question),
        "telestich": generate_telestich(cleaned_question),
        "center": generate_center(cleaned_question),
        "corner": generate_corner(cleaned_question),
        "staircase": generate_staircase(cleaned_question)
    }

    processed_data.append(jailbreaks)

# 写入新 JSON 文件
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(processed_data, f, ensure_ascii=False, indent=2)

print(f"已成功将 {len(processed_data)} 条数据转换并保存至: {output_json_path}")
