from dotenv import load_dotenv
load_dotenv()

import os
import json
import subprocess


# =============================
# TOOL: đọc file
# =============================
def read_file_tool(path: str) -> str:
    if not os.path.exists(path):
        return f"ERROR: File not found at path: {path}"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# =============================
# TOOL: ghi file (SỬA CODE)
# =============================
def write_file_tool(path: str, content: str) -> str:
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"SUCCESS: File {path} has been updated."
    except Exception as e:
        return f"ERROR writing file: {str(e)}"


TOOLS = {
    "read_file": read_file_tool,
    "write_file": write_file_tool,
}


# =============================
# Gọi Ollama raw
# =============================
def call_ollama(prompt: str, model="qwen2.5"):
    cmd = ["ollama", "run", model]

    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )

    output, error = process.communicate(prompt)

    if error and error.strip():
        print("⚠ OLLAMA ERROR:", error)

    return output


# =============================
# ReAct Agent Step
# =============================
def react_step(model, user_msg):
    system = """
Bạn là một AI Agent chuyên debug và sửa code Python.

⚠ BẮT BUỘC:
- LUÔN trả lời bằng tiếng Việt.
- LUÔN sử dụng JSON chuẩn.
- KHÔNG trả dấu ``` hoặc ký tự đặc biệt ngoài JSON.

JSON Format:
{
  "thought": "giải thích bằng tiếng Việt",
  "action": "read_file" hoặc "write_file" hoặc "finish",
  "action_input": "đường dẫn file",
  "content": "nội dung file mới nếu action=write_file",
  "final_answer": "kết luận nếu action=finish"
}

Luật:
- Nếu cần xem file → action = "read_file".
- Nếu cần sửa code → action = "write_file".
- Nếu đã xong → action = "finish".
"""

    full_prompt = system + "\n\nNgữ cảnh hiện tại:\n" + user_msg
    raw = call_ollama(full_prompt, model)

    try:
        json_start = raw.index("{")
        json_end = raw.rindex("}") + 1
        data = json.loads(raw[json_start:json_end])
        return data
    except:
        return {"action": "finish", "final_answer": raw}


# =============================
# MAIN LOOP
# =============================
def run_agent():
    print("=== LOCAL AI DEBUGGER + AUTO FIXER (Ollama ReAct Agent – Vietnamese) ===")

    model = "qwen2.5"
    code_path = input("Nhập đường dẫn file code (vd: sample_code/main.py): ").strip()
    error_msg = input("Nhập lỗi gặp phải: ").strip()

    if not os.path.exists(code_path):
        print(f"\n❌ File không tồn tại: {code_path}")
        return

    user_msg = f"""
Debug và sửa file Python sau:

Đường dẫn: {code_path}
Lỗi gặp phải: {error_msg}
"""

    loop_limit = 10
    loop_count = 0

    while True:
        loop_count += 1
        if loop_count > loop_limit:
            print("\n⚠ Dừng lại để tránh loop vô hạn.")
            break

        step = react_step(model, user_msg)

        print("\n[SUY NGHĨ]", step.get("thought", ""))
        print("[HÀNH ĐỘNG]", step.get("action", ""))

        action = step.get("action")

        # ---- TOOL: READ FILE ----
        if action == "read_file":
            file_path = step.get("action_input", code_path)
            result = read_file_tool(file_path)

            print("[TOOL RESULT]\n", result)
            user_msg += f"\nKết quả read_file:\n{result}\n"
            continue

        # ---- TOOL: WRITE FILE ----
        if action == "write_file":
            file_path = step.get("action_input", code_path)
            new_content = step.get("content", "")

            result = write_file_tool(file_path, new_content)

            print("[TOOL RESULT]\n", result)
            user_msg += f"\nFile updated:\n{result}\n"
            continue

        # ---- FINISH ----
        if action == "finish":
            print("\n=== KẾT LUẬN CUỐI CÙNG ===")
            print(step.get("final_answer", ""))
            break


if __name__ == "__main__":
    run_agent()
