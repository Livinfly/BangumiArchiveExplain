import re
import json
from collections import Counter

def parse_infobox_keys(infobox):
    """
    提取 infobox 中的顶层键，只匹配 `|键名=值` 的结构
    """
    # 匹配以 | 开头的顶层键，不解析嵌套内容
    pattern = r'^\|([^=]+)='
    matches = re.findall(pattern, infobox, re.MULTILINE)
    
    # 返回所有键
    return [key.strip() for key in matches]

def validate_json_and_collect_infobox_keys(file_path):
    """
    检查 JSON 文件，并统计 infobox 中的顶层键以及 career 和 type - career 的关系
    """
    infobox_keys_counter = Counter()
    career_counter = Counter()
    type_career_counter = Counter()
    
    # 读取 JSON 文件
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            try:
                # 解析 JSON 数据
                json_obj = json.loads(line)
                
                # 获取 infobox 并提取顶层键
                infobox = json_obj.get("infobox", "")
                keys = parse_infobox_keys(infobox)
                infobox_keys_counter.update(keys)
                
                # 获取 career 字段并统计职业
                career = json_obj.get("career", [])
                career_counter.update(career)
                
                # 获取 type 字段并统计 type - career 关系
                type_value = json_obj.get("type", "")
                for c in career:
                    type_career_counter[(type_value, c)] += 1
            
            except json.JSONDecodeError:
                print(f"Line {line_number}: Invalid JSON format.")
            except Exception as e:
                print(f"Line {line_number}: Unexpected error: {e}")
    
    # 排序并输出统计结果
    sorted_infobox_keys = sorted(infobox_keys_counter.items(), key=lambda x: x[1], reverse=True)
    sorted_career = sorted(career_counter.items(), key=lambda x: x[1], reverse=True)
    sorted_type_career = sorted(type_career_counter.items(), key=lambda x: (x[0][0], -x[1]))
    # 输出到文件
    for sorted_keys, output_file in [(sorted_infobox_keys, "person_infobox.json"), 
                                     (sorted_career, "person_career.json"),
                                     (sorted_type_career, "person_type_career.json"), ]:
        sorted_keys_dict = {key: count for key, count in sorted_keys}
        if 'type' in output_file: 
            sorted_keys_dict = [{"type": t, "career": c, "count": count} for ((t, c), count) in sorted_keys]
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(sorted_keys_dict, f, ensure_ascii=False, indent=4)
        print(f"Statistics have been exported to {output_file}")

# 示例用法
file_path = "./bangumi-2024-11-19/person.jsonlines"  # 替换为实际的 JSON Lines 文件路径
validate_json_and_collect_infobox_keys(file_path)
