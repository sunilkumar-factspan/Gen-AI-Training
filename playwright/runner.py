import subprocess
import tempfile
import os
import uuid
import sys

def execute_code(code: str, timeout=30):
    file_path = None

    try:
        file_name = f"temp_{uuid.uuid4().hex}.py"
        file_path = os.path.join(tempfile.gettempdir(), file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        print("Executing:", file_path)

        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.getcwd()   # ✅ ensures output.png saved in project root
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "screenshot": os.path.join(os.getcwd(), "output.png")
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Execution timed out (30s)",
            "screenshot": None
        }

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)