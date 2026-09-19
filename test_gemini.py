from google import genai

# 把这里替换成你自己的 API Key
client = genai.Client(api_key="AQ.Ab8RN6LPlJ-de9eawljIvnu0TKrr-ECevyVV-gCyQ9suFAkJQg")


response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="你好，请用一句话介绍一下你自己。"
)

print(response.text)