import json

# 输入输出路径
input_path = '/Users/muzhiyi/Desktop/famous_dataset/alredy_harmful/hate_speech_offensive/data/data.json'
output_path = '/Users/muzhiyi/Desktop/famous_dataset/alredy_harmful/hate_speech_offensive_filtered.json'

# 存储符合条件的结果
filtered_data = []

# 打开并读取 JSON 文件
with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 遍历每条数据
for item in data:
    original_tweet = item.get("tweet", "")

    # 清洗 tweet 文本（去掉外层引号和空格）
    cleaned_tweet = original_tweet.strip().strip('"').strip("'").strip()

    clean_content = ""

    if ':' in cleaned_tweet:
        # 获取原始 tweet 中冒号的位置（不清洗前处理）
        colon_index = cleaned_tweet.find(':')
        if colon_index != -1:
            # 提取冒号后所有内容（含标点、引号、特殊符号等）
            after_colon = cleaned_tweet[colon_index+1:].strip()

            # 判断单词数是否 <= 10（用于过滤）
            word_count = len(after_colon.split())

            if word_count <= 10 and after_colon:
                # 保留从冒号后直到结尾的完整内容（原样保存）
                clean_content = after_colon

    else:
        # 不包含冒号时，直接判断整个 tweet 的单词数
        word_count = len(cleaned_tweet.split())
        if word_count <= 10 and cleaned_tweet:
            clean_content = cleaned_tweet

    # 如果有提取到 clean_content，则添加到结果中
    if clean_content:
        new_item = item.copy()
        new_item['clean_tweet'] = clean_content
        filtered_data.append(new_item)

# 写入新的 JSON 文件
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)
