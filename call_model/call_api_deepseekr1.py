import json
from openai import OpenAI
# import torch
import os
import glob
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import time
import datetime
def call_api_deepseekr1(question):
    client = OpenAI(api_key="", base_url="")
    messages = [{"role": "user", "content": question}]
    try:
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages
        )
    except Exception as e:
        print(f"API 调用失败: {e}")
        filtered_results.append({
            "index": qid,
            "label": "APIError",
            "instruction": question,
            "output": "NULL"
        })
    # 解析响应内容
    reasoning_content = getattr(response.choices[0].message, 'reasoning_content', "NULL")
    answer_content = getattr(response.choices[0].message, 'content', "NULL")
    output = f"{reasoning_content}\n</think>\n\n{answer_content}"
    return reasoning_content,answer_content,output
# 开始时间
start_time = datetime.datetime.now()
print(f"Start Time: {start_time}")

input_folder = "attack_6category/repeat_attack_6catgory"  # 输入文件夹路径
output_folder = "attack_6category/repeat_attack_output/deepseek_r1"  # 输出文件夹路径

os.makedirs(output_folder, exist_ok=True)  # 自动创建输出文件夹
json_files = glob.glob(os.path.join(input_folder, "*.json"))  # 获取所有 JSON 文件

for json_file_path in json_files:
    with open(json_file_path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print(f"无法解析文件: {json_file_path}")
            continue

    # 提取文件名，用于输出文件
    file_name = os.path.basename(json_file_path)
    output_json_path = os.path.join(output_folder, file_name)

    # 如果输出文件已存在，读取已有内容
    if os.path.exists(output_json_path):
        with open(output_json_path, "r", encoding="utf-8") as output_file:
            try:
                filtered_results = json.load(output_file)
            except json.JSONDecodeError:
                filtered_results = []
    else:
        filtered_results = []

    # 处理每个 JSON 文件的内容
    for qid, item in enumerate(data):
        # label = item['label']
        original = item.get("original", "")
        input_text = item.get("acrostic", "").strip()
        if not input_text:
            continue
        reasoning_content, answer_content, output = call_api_deepseekr1(input_text)
        # 添加结果到列表
        filtered_results.append({
            "index": qid,
            "original": original,
            "instruction": input_text,
            "output": output,
            "reasoning_content": reasoning_content,
            "answer_content": answer_content
        })

    # 保存处理后的结果到输出文件
    with open(output_json_path, "w", encoding="utf-8") as output_file:
        json.dump(filtered_results, output_file, indent=4, ensure_ascii=False)

    print(f"文件 {file_name} 处理完成，结果已保存至 {output_json_path}")
