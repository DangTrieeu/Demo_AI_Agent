# AI Agent - Automated React App Generator

Dự án này demo một đội ngũ AI (AI Squad) tự động sử dụng **CrewAI** và **Groq (Llama 3)** để thiết kế, lập trình và kiểm thử một ứng dụng React Login hoàn chỉnh.

## 🤖 Đội ngũ AI (The Squad)

Hệ thống bao gồm 3 agent chuyên biệt:

1.  **Solution Architect**: Thiết kế luồng ứng dụng và logic nghiệp vụ.
2.  **Senior React Developer**: Viết code React sạch, sử dụng Tailwind CSS.
3.  **QA Automation Engineer**: Viết Unit Test (Jest/RTL) để đảm bảo chất lượng code.

## 🚀 Tính năng

- **Quy trình tự động hóa**: Từ thiết kế -> Code -> Test.
- **Công nghệ**: Python (Orchestration), React + Vite (Frontend), Tailwind CSS.
- **Hiệu năng cao**: Sử dụng model Llama 3 70b thông qua Groq API.

## 🛠️ Cài đặt

1.  **Clone dự án**:

    ```bash
    git clone <repository-url>
    cd AI_Agent
    ```

2.  **Cài đặt thư viện Python**:

    ```bash
    pip install crewai crewai-tools python-dotenv
    ```

3.  **Cấu hình môi trường**:
    - Tạo file `.env` tại thư mục gốc.
    - Thêm Groq API Key của bạn vào:
      ```env
      GROQ_API_KEY=gsk_...
      ```

## 🏃‍♂️ Hướng dẫn sử dụng

1.  **Chạy AI Agent**:

    ```bash
    python agent.py
    ```

    Các agent sẽ bắt đầu làm việc và tự động sinh code vào thư mục `ai-demo-login/src/`.
    _Lưu ý: Script có thời gian nghỉ giữa các task để tránh Rate Limit của Groq._

2.  **Chạy ứng dụng React**:
    Sau khi AI hoàn thành công việc:
    ```bash
    cd ai-demo-login
    npm install
    npm run dev
    ```

## 📂 Cấu trúc dự án

```
AI_Agent/
├── agent.py            # Script chính điều phối AI Squad
├── .env                # Biến môi trường (API Key)
├── ai-demo-login/      # Dự án React (Vite)
│   ├── src/            # Nơi chứa code do AI tạo ra (Login.jsx, App.jsx,...)
│   └── ...
└── README.md           # Tài liệu dự án
```
