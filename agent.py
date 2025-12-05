import os
import time
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileWriterTool
from dotenv import load_dotenv

# Tắt tính năng hỏi xem trace của CrewAI
os.environ["CREWAI_TRACING_ENABLED"] = "false"
os.environ["OTEL_SDK_DISABLED"] = "true"

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

file_writer = FileWriterTool()

# Script đang ở: .../AI_Agent/agent.py
# Dự án React ở: .../AI_Agent/ai-demo-login/src/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(SCRIPT_DIR, "ai-demo-login", "src")

BASE_PATH = BASE_PATH.replace("\\", "/")

if not BASE_PATH.endswith("/"):
    BASE_PATH += "/"

print(f"DEBUG: BASE_PATH set to: {BASE_PATH}")


# --- ĐỊNH NGHĨA AGENTS ---

# Agent 1: Solution Architect
architect = Agent(
    role='Solution Architect & UI Designer',
    goal='Thiết kế luồng ứng dụng Login và Welcome, xác định state và hardcode credentials',
    backstory='Bạn chịu trách nhiệm thiết kế logic, đảm bảo các component có thể kết nối với nhau.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Agent 2: React Developer
developer = Agent(
    role='Senior React Developer',
    goal='Viết code React component (Login, Welcome) và App.jsx sử dụng Tailwind CSS',
    backstory='Bạn viết code sạch, functional component. Bạn phải sử dụng FileWriterTool để tạo file.',
    tools=[file_writer],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Agent 3: QA Automation Engineer
qa_tester = Agent(
    role='QA Automation Engineer',
    goal='Viết Unit Test cho component Login để đảm bảo logic hoạt động',
    backstory='Bạn chuyên viết test dùng Jest và React Testing Library. Bạn phải tạo file test.',
    tools=[file_writer],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# --- 3. ĐỊNH NGHĨA TASKS VÀ CHẠY TỪNG GIAI ĐOẠN ---

print("Đội ngũ AI bắt đầu xây dựng giao diện Login...")

# --- GIAI ĐOẠN 1: THIẾT KẾ ---
print("\n--- GIAI ĐOẠN 1: Solution Architect đang thiết kế... ---")
task_design = Task(
    description='''
    Thiết kế logic:
    1. Tài khoản cứng là username="admin", password="123".
    2. Nếu đăng nhập đúng -> hiện Welcome.
    3. Nếu đăng nhập sai -> alert lỗi.
    4. Mô tả chính xác nội dung các file: Login.jsx, Welcome.jsx, và App.jsx (là nơi chứa logic chính).
    ''',
    expected_output='Bản mô tả logic và cấu trúc các file.',
    agent=architect
)

crew_phase_1 = Crew(agents=[architect], tasks=[task_design], verbose=True)
result_design = crew_phase_1.kickoff()

print("Giai đoạn 1 hoàn tất. Nghỉ 70s...")
time.sleep(70)

# --- GIAI ĐOẠN 2: VIẾT CODE ---
print("\n--- GIAI ĐOẠN 2: React Developer đang viết code... ---")

# 2.1 Viết Login.jsx
print("   > Đang viết Login.jsx...")
task_login = Task(
    description=f'''
    NHIỆM VỤ: Viết code cho Login component và lưu vào file.
    
    HƯỚNG DẪN CHI TIẾT:
    1. Tạo nội dung code React cho Login component dựa trên thiết kế: {result_design}
    2. Sử dụng Tailwind CSS cho giao diện đẹp.
    3. QUAN TRỌNG: Sử dụng công cụ "FileWriterTool" để ghi file.
    4. Đường dẫn file: "{BASE_PATH}Login.jsx"
    5. Nội dung file phải là code thuần (raw code), KHÔNG được bao quanh bởi markdown block (```jsx).
    6. Đảm bảo import React và các hook cần thiết.
    7. KHÔNG được tự ý thử lại nếu gặp lỗi nhỏ, hãy kiểm tra kĩ input trước khi gọi tool.
    ''',
    expected_output='Thông báo đã ghi file Login.jsx thành công.',
    agent=developer
)
crew_2_1 = Crew(agents=[developer], tasks=[task_login], verbose=True)
crew_2_1.kickoff()

print("   > Nghỉ 70s...")
time.sleep(70)

# 2.2 Viết Welcome.jsx
print("   > Đang viết Welcome.jsx...")
task_welcome = Task(
    description=f'''
    NHIỆM VỤ: Viết code cho Welcome component và lưu vào file.

    HƯỚNG DẪN CHI TIẾT:
    1. Tạo nội dung code React cho Welcome component dựa trên thiết kế: {result_design}
    2. Sử dụng Tailwind CSS.
    3. QUAN TRỌNG: Sử dụng công cụ "FileWriterTool" để ghi file.
    4. Đường dẫn file: "{BASE_PATH}Welcome.jsx"
    5. Nội dung file phải là code thuần (raw code), KHÔNG được bao quanh bởi markdown block.
    6. KHÔNG được tự ý thử lại các phương án khác nhau, hãy làm đúng ngay lần đầu.
    ''',
    expected_output='Thông báo đã ghi file Welcome.jsx thành công.',
    agent=developer
)
crew_2_2 = Crew(agents=[developer], tasks=[task_welcome], verbose=True)
crew_2_2.kickoff()

print("   > Nghỉ 70s...")
time.sleep(70)

# 2.3 Viết App.jsx
print("   > Đang viết App.jsx...")
task_app = Task(
    description=f'''
    NHIỆM VỤ: Viết code cho App component và lưu vào file.

    HƯỚNG DẪN CHI TIẾT:
    1. Tạo nội dung code React cho App.jsx để kết nối Login và Welcome.
    2. Logic: {result_design}
    3. QUAN TRỌNG: Sử dụng công cụ "FileWriterTool" để ghi file.
    4. Đường dẫn file: "{BASE_PATH}App.jsx"
    5. Nội dung file phải là code thuần (raw code), KHÔNG được bao quanh bởi markdown block.
    6. Đảm bảo import đúng đường dẫn các component con (./Login, ./Welcome).
    ''',
    expected_output='Thông báo đã ghi file App.jsx thành công.',
    agent=developer
)
crew_2_3 = Crew(agents=[developer], tasks=[task_app], verbose=True)
result_coding = crew_2_3.kickoff()

print("Giai đoạn 2 hoàn tất. Nghỉ 70s để tránh giới hạn API...")
time.sleep(70)

# --- GIAI ĐOẠN 3: KIỂM THỬ ---
print("\n--- GIAI ĐOẠN 3: QA Engineer đang viết test... ---")
task_testing = Task(
    description=f'''
    NHIỆM VỤ: Viết Unit Test cho Login component.

    HƯỚNG DẪN CHI TIẾT:
    1. Dựa trên code Login.jsx và App.jsx vừa tạo.
    2. Viết test case sử dụng Jest và React Testing Library.
    3. Test case 1: Render thành công (tìm text "Đăng nhập" hoặc tương tự).
    4. Test case 2: Gọi hàm onLogin khi nhập đúng admin/123 và bấm nút.
    5. QUAN TRỌNG: Sử dụng công cụ "FileWriterTool" để ghi file.
    6. Đường dẫn file: "{BASE_PATH}Login.test.js"
    7. Nội dung file phải là code thuần.
    ''',
    expected_output='Thông báo đã ghi file test thành công: Login.test.js.',
    agent=qa_tester
)

crew_phase_3 = Crew(agents=[qa_tester], tasks=[task_testing], verbose=True)
result_testing = crew_phase_3.kickoff()

print("Giai đoạn 3 hoàn tất. Nghỉ 70s...")
time.sleep(70)

print("\n######################")
print("QUY TRÌNH HOÀN THÀNH!")
print(f"Các file đã được tạo thành công trong thư mục: {BASE_PATH}")