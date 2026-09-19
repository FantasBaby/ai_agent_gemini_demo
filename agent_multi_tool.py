from google import genai
from google.genai import types

# 1. 天气工具

def get_weather(city):
    weather_data = {
        "南京": {
            "temperature": 25,
            "weather": "小雨",
            "wind": "3级"
        },
        "上海": {
            "temperature": 27,
            "weather": "多云",
            "wind": "2级"
        },
        "北京": {
            "temperature": 20,
            "weather": "晴",
            "wind": "2级"
        }
    }
    return weather_data.get(
        city,
        {"error": "没有找到这个城市的天气"}
    )

# 2. 计算器工具

def calculate(expression):
    try:
        result = eval(expression)
        return {
            "expression": expression,
            "result": result
        }

    except Exception as e:
        return {
            "error": "计算失败"
        }


# 3. 创建 Gemini 客户端

client = genai.Client(
    api_key="AQ.Ab8RN6LPlJ-de9eawljIvnu0TKrr-ECevyVV-gCyQ9suFAkJQg"
)

# 4. 告诉 Gemini 有哪些工具

tools = types.Tool(
    function_declarations=[
        # ---------- 天气工具 ----------
        types.FunctionDeclaration(
            name="get_weather",
            description="查询指定城市的天气信息",
            parameters={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，例如南京、上海、北京"
                    }
                },
                "required": ["city"]
            }
        ),

        # ---------- 计算器工具 ----------
        types.FunctionDeclaration(
            name="calculate",
            description="计算数学表达式，例如 123*456、100/5+20",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "需要计算的数学表达式"
                    }
                },
                "required": ["expression"]
            }
        )
    ]
)

# 5. 获取用户问题

user_question = input("请输入你的问题：")

# 6. 第一次请求 Gemini

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=user_question,
    config=types.GenerateContentConfig(
        tools=[tools]
    )
)

# 7. 检查 Gemini 有没有要求调用工具

function_call = None

for candidate in response.candidates:
    for part in candidate.content.parts:
        if part.function_call:
            function_call = part.function_call
            break
    if function_call:
        break

# 8. 如果没有调用工具

if function_call is None:
    print("\n========== Gemini直接回答 ==========")
    print(response.text)

# 9. 如果调用了工具

else:
    print("\n========== Agent决定 ==========")
    print("工具名称：", function_call.name)
    print("工具参数：", function_call.args)

    # 10. 根据工具名称执行对应 Python 函数

    if function_call.name == "get_weather":
        city = function_call.args["city"]
        print("\nAgent调用：get_weather")
        weather_result = get_weather(city)
    elif function_call.name == "calculate":
        expression = function_call.args["expression"]
        print("\nAgent调用：calculate")
        weather_result = calculate(expression)
    else:
        weather_result = {
            "error": "未知工具"
        }

    # 11. 查看工具执行结果

    print("\n========== 工具执行结果 ==========")
    print(weather_result)

    # 12. 把工具结果交给 Gemini

    tool_response = types.Part.from_function_response(
        name=function_call.name,
        response=weather_result
    )

    # 13. 第二次请求 Gemini

    final_response = client.models.generate_content(

        model="gemini-3.6-flash",
        contents=[
            user_question,
            response.candidates[0].content,
            tool_response
        ],
        config=types.GenerateContentConfig(
            tools=[tools]
        )
    )

    # 14. 输出最终答案

    print("\n========== Agent最终回答 ==========")
    print(final_response.text)