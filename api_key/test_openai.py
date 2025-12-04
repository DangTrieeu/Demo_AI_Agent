import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 1. Thêm base_url trỏ về Groq
client = OpenAI(
    base_url="https://api.groq.com/openai/v1", 
    api_key=os.getenv("GROQ_API_KEY")
)

try:
    # Gọi API đơn giản để test
    response = client.chat.completions.create(
        # 2. Đổi model sang model mà Groq hỗ trợ (VD: Llama 3)
        model="llama-3.3-70b-versatile", 
        messages=[
            {"role": "user", "content": "Hello! This is a test."}
        ]
    )

    print("API KEY OK! Model trả lời:")
    # Lưu ý: Thư viện mới dùng dấu chấm (.) thay vì ngoặc vuông ['content']
    print(response.choices[0].message.content) 

except Exception as e:
    print("❌ API KEY lỗi hoặc sai Model:")
    print(e)