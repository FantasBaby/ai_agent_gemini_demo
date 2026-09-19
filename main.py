# ============================================
# 1. 天气工具
# ============================================

def get_weather(city):
    """
    模拟天气查询工具
    """
    weather_data = {
        "南京": {
            "city": "南京",
            "temperature": 25,
            "weather": "小雨",
            "wind": "3级"
        },
        "上海": {
            "city": "上海",
            "temperature": 27,
            "weather": "多云",
            "wind": "2级"
        },
        "北京": {
            "city": "北京",
            "temperature": 20,
            "weather": "晴",
            "wind": "2级"
        }
    }

    # 根据城市查询天气
    result = weather_data.get(city)

    if result is None:
        return {
            "error": f"暂时没有{city}的天气数据"
        }
    return result


# ============================================
# 2. Agent
# ============================================

def agent(user_input):
    print("\n========== Agent开始工作 ==========")
    # 第一步：判断用户是否需要查询天气
    if "天气" in user_input or "穿什么" in user_input:
        print("Agent判断：需要查询天气")
         
        # 第二步：从用户问题中找到城市
         
        cities = ["南京", "上海", "北京"]
        city = None
        for item in cities:
            if item in user_input:
                city = item
                break

        # 如果没有找到城市
        if city is None:
            print("Agent：没有找到城市")
            return "请告诉我你想查询哪个城市的天气。"

        # 第三步：调用天气工具

        print("Agent调用工具：get_weather")
        print("工具参数：", city)
        weather = get_weather(city)

        # 第四步：查看工具返回结果
         
        print("工具返回：", weather)
         
        # 第五步：Agent根据天气生成建议
         
        temperature = weather["temperature"]
        weather_type = weather["weather"]
        wind = weather["wind"]
        # 根据天气给出穿衣建议
        if "小雨" in weather_type:
            clothes = "建议穿长袖或薄外套，并携带雨伞。"
        elif temperature >= 30:
            clothes = "天气较热，建议穿短袖。"
        elif temperature >= 20:
            clothes = "温度比较舒适，建议穿长袖或薄外套。"
        else:
            clothes = "天气比较冷，建议穿厚外套。"

         
        # 第六步：生成最终回答
         
        answer = (
            f"{city}今天{temperature}℃，"
            f"{weather_type}，"
            f"风力{wind}。"
            f"\n{clothes}"
        )
        return answer

    else:
        print("Agent判断：不需要查询天气")
        return "我是一个天气助手，可以帮你查询天气并提供穿衣建议。"

# ============================================
# 3. 主程序
# ============================================

user_input = input("请输入你的问题：")

result = agent(user_input)

print("\n========== 最终回答 ==========")

print(result)
