import json
import random
from datetime import datetime, timedelta

# 基础数据配置
base_id = 200001
user_id = "coderpwh"
start_time = datetime(2025, 2, 1, 15, 10, 0)

# 可选项配置
activities = [
    ("打篮球", "打篮球非常好，运动增加免疫力"),
    ("跑步", "跑步有助于提高心肺功能，保持健康"),
    ("游泳", "游泳对关节友好，适合全身锻炼"),
    ("踢足球", "踢足球增强团队协作能力"),
    ("打羽毛球", "打羽毛球提高反应速度和灵活性"),
    ("骑自行车", "骑自行车有助于提升腿部肌肉力量"),
    ("做瑜伽", "做瑜伽帮助放松身心，改善柔韧性"),
    ("爬山", "爬山能锻炼耐力，享受自然风光"),
    ("跳绳", "跳绳是高效的有氧运动，燃烧卡路里"),
    ("打网球", "打网球锻炼全身协调性和爆发力")
]

places = ["深圳湾", "公园", "体育馆", "社区运动场", "学校操场",
          "河边", "健身房", "运动中心", "小区花园", "海滨长廊"]

time_phrases = ["昨天下午", "今天早上", "上周六晚上", "前天中午",
                "今天傍晚", "上周日清晨", "昨晚", "今天中午",
                "今天下午", "上周五傍晚"]

# 生成测试数据
test_data = []
for i in range(100):
    # 随机选择要素
    time_phrase = random.choice(time_phrases)
    place = random.choice(places)
    activity, prompt = random.choice(activities)

    # 构建内容
    user_content = f"我{time_phrase}去{place}{activity}了"
    current_time = start_time + timedelta(minutes=10 * i)

    # 构建完整记录
    record = {
        "id": str(base_id + i),
        "content": user_content,
        "map": {
            "id": str(base_id + i),
            "user_id": user_id,
            "user_content": user_content,
            "prompt_content": prompt,
            "create_time": current_time.strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    test_data.append(record)

# 转换为JSON格式
json_data = json.dumps(test_data, ensure_ascii=False, indent=2)

# 打印结果（实际使用时可以写入文件）
print(json_data)