import re
import json
from collections import Counter
import time

def parse_infobox_keys(infobox):
    """
    提取 infobox 中的顶层键，只匹配 `|键名=值` 的结构
    """
    # 匹配以 | 开头的顶层键，不解析嵌套内容
    pattern = r'^\|([^=]+)='
    matches = re.findall(pattern, infobox, re.MULTILINE)
    
    # 返回所有键
    return [key.strip() for key in matches]

def validate_jsonlines_and_collect_infobox_keys(file_path):
    """
    检查 JSONLines 文件，并统计 infobox 中的顶层键
    """
    infobox_keys_counter = Counter()
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            try:
                # 解析 JSON
                json_obj = json.loads(line)
                
                # 获取 infobox 并提取顶层键
                infobox = json_obj.get("infobox", "")
                keys = parse_infobox_keys(infobox)
                # if '航程：20000 海里/15 节\r\n|编制' in keys:
                #     print(line)
                infobox_keys_counter.update(keys)
            
            except json.JSONDecodeError:
                print(f"Line {line_number}: Invalid JSON format.")
            except Exception as e:
                print(f"Line {line_number}: Unexpected error: {e}")
    
    # 输出统计结果
    # print("\nAll unique top-level keys in infobox:")
    # for key, count in infobox_keys_counter.items():
    #     print(f"{key}: {count} occurrences")
    #     time.sleep(1)
    # print(len(infobox_keys_counter))
    # print("All unique top-level keys in infobox (sorted by count):")
    # for key, count in sorted_keys[:25]:
    #     print(f"{key}: {count} occurrences")
    sorted_keys = sorted(infobox_keys_counter.items(), key=lambda x: x[1], reverse=True)
    infobox_keys_dict = {key: count for key, count in sorted_keys}
    output_file = "subject_infobox.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(infobox_keys_dict, f, ensure_ascii=False, indent=4)

    print(f"Sorted infobox keys have been exported to {output_file}")

# 示例用法
file_path = "./bangumi-2024-11-19/subject.jsonlines"  # 替换为实际文件路径
validate_jsonlines_and_collect_infobox_keys(file_path)
