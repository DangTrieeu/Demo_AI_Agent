import os
import time
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileWriterTool
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

file_writer = FileWriterTool()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
BASE_PATH = os.path.join(PROJECT_ROOT, "ai-demo-login", "src")

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

print("Giai đoạn 1 hoàn tất. Nghỉ 60s...")
time.sleep(60)

# --- GIAI ĐOẠN 2: VIẾT CODE ---
print("\n--- GIAI ĐOẠN 2: React Developer đang viết code... ---")

# 2.1 Viết Login.jsx
print("   > Đang viết Login.jsx...")
task_login = Task(
    description=f'''
    Dựa trên thiết kế sau:
    {result_design}

    Hãy viết file Login component và ghi vào "{BASE_PATH}Login.jsx".
    Sử dụng Tailwind CSS.
    ''',
    expected_output='Thông báo đã ghi file Login.jsx thành công.',
    agent=developer
)
crew_2_1 = Crew(agents=[developer], tasks=[task_login], verbose=True)
crew_2_1.kickoff()

print("   > Nghỉ 60s...")
time.sleep(60)

# 2.2 Viết Welcome.jsx
print("   > Đang viết Welcome.jsx...")
task_welcome = Task(
    description=f'''
    Dựa trên thiết kế sau:
    {result_design}

    Hãy viết file Welcome component và ghi vào "{BASE_PATH}Welcome.jsx".
    Sử dụng Tailwind CSS.
    ''',
    expected_output='Thông báo đã ghi file Welcome.jsx thành công.',
    agent=developer
)
crew_2_2 = Crew(agents=[developer], tasks=[task_welcome], verbose=True)
crew_2_2.kickoff()

print("   > Nghỉ 60s...")
time.sleep(60)

# 2.3 Viết App.jsx
print("   > Đang viết App.jsx...")
task_app = Task(
    description=f'''
    Dựa trên thiết kế sau:
    {result_design}

    Hãy viết file App.jsx (logic chính, state management) và ghi vào "{BASE_PATH}App.jsx".
    Kết nối Login và Welcome.
    ''',
    expected_output='Thông báo đã ghi file App.jsx thành công.',
    agent=developer
)
crew_2_3 = Crew(agents=[developer], tasks=[task_app], verbose=True)
result_coding = crew_2_3.kickoff()

print("Giai đoạn 2 hoàn tất. Nghỉ 60s để tránh giới hạn API...")
time.sleep(60)

# --- GIAI ĐOẠN 3: KIỂM THỬ ---
print("\n--- GIAI ĐOẠN 3: QA Engineer đang viết test... ---")
task_testing = Task(
    description=f'''
    Dựa trên code Login.jsx vừa được tạo (và kết quả sau: {result_coding}), hãy viết một file unit test sử dụng Jest/RTL.
    Kiểm tra 2 trường hợp: 1) render thành công, 2) gọi hàm onLogin khi nút được bấm.
    Lưu file test vào "{BASE_PATH}Login.test.js".
    ''',
    expected_output='Thông báo đã ghi file test thành công: Login.test.js.',
    agent=qa_tester
)

crew_phase_3 = Crew(agents=[qa_tester], tasks=[task_testing], verbose=True)
result_testing = crew_phase_3.kickoff()

print("\n######################")
print("QUY TRÌNH HOÀN THÀNH!")
print(f"Các file đã được tạo thành công trong thư mục: {BASE_PATH}")