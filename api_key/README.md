# AI Squad Demo

Dự án này sử dụng CrewAI để tạo ra một đội ngũ AI agents tự động thiết kế, code và kiểm thử một ứng dụng React đơn giản (Login page).

## Yêu cầu hệ thống

- Python 3.10 trở lên

## Cài đặt

Để chạy được script này, bạn cần cài đặt các thư viện sau:

```bash
pip install crewai crewai-tools python-dotenv litellm
```

## Cấu hình

1. Tạo file `.env` trong cùng thư mục với `run_ai_squad.py`.
2. Thêm API Key của Groq vào file `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Chạy chương trình

Mở terminal tại thư mục chứa file và chạy lệnh:

```bash
python run_ai_squad.py
```

## Cấu trúc dự án

- `run_ai_squad.py`: Script chính điều phối các AI agents.
- `.env`: File chứa biến môi trường (API Key).
- `ai-demo-login/`: Thư mục đích nơi AI sẽ sinh ra code React.
