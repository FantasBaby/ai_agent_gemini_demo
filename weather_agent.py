from google import genai
from google.genai import types


# =========================
# 1. 天气工具
# =========================

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

    return weather_data.get(city, {
        "error": "没有找到这个城市的天气"
    })


# =========================
# 2. Gemini客户端
# =========================

client = genai.Client(
    api_key="AQ.Ab8RN6LPlJ-de9eawljIvnu0TKrr-ECevyVV-gCyQ9suFAkJQg"
)


# =========================
# 3. 定义工具
# =========================

weather_tool = types.Tool(
    function_declarations=[

        types.FunctionDeclaration(

            name="get_weather",

            description="查询指定城市的天气",

            parameters={
                "type": "object",

                "properties": {

                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }

                },

                "required": ["city"]
            }
        )
    ]
)


# =========================
# 4. 获取用户问题
# =========================

user_question = input(
    "请输入你的问题："
)


# =========================
# 5. 第一次请求 Gemini
# =========================

response = client.models.generate_content(

    model="gemini-3.6-flash",

    contents=user_question,

    config=types.GenerateContentConfig(

        tools=[weather_tool]
    )
)


# =========================
# 6. 判断 Gemini 是否调用工具
# =========================

function_call = None

for candidate in response.candidates:

    for part in candidate.content.parts:

        if part.function_call:

            function_call = part.function_call

            break


# =========================
# 7. 不需要工具
# =========================

if function_call is None:

    print("\nGemini：")

    print(response.text)


# =========================
# 8. 需要工具
# =========================

else:

    print("\n========== 工具调用 ==========")

    print(
        "工具名称：",
        function_call.name
    )

    print(
        "工具参数：",
        function_call.args
    )


    # =========================
    # 9. Python执行工具
    # =========================

    if function_call.name == "get_weather":

        city = function_call.args["city"]

        weather_result = get_weather(city)


        print("\n========== 工具执行 ==========")

        print(
            "查询城市：",
            city
        )

        print(
            "返回结果：",
            weather_result
        )


    # =========================
    # 10. 把工具结果交给 Gemini
    # =========================

    tool_response = types.Part.from_function_response(

        name=function_call.name,

        response=weather_result
    )


    # =========================
    # 11. Gemini生成最终答案
    # =========================

    final_response = client.models.generate_content(

        model="gemini-3.6-flash",

        contents=[

            user_question,

            response.candidates[0].content,

            tool_response
        ],

        config=types.GenerateContentConfig(

            tools=[weather_tool]
        )
    )


    print("\n========== 最终回答 ==========")

    print(final_response.text)