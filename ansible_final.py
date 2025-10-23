import subprocess
import re
import os

def showrun():
    playbook_file = 'playbook_showrun.yaml'
    student_id = "66070276"

    command = ['ansible-playbook', playbook_file]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=120
        )

        stdout_result = result.stdout
        print("Playbook Output:\n", stdout_result)

        # 🔍 ใช้ regex ดึง router name จาก debug msg
        match = re.search(r'Router name:\s*"?(.*?)"?\s*$', stdout_result, re.MULTILINE)
        if match:
            router_name = match.group(1)
        else:
            router_name = "UnknownRouter"

        # 🔧 ตั้งชื่อไฟล์ตาม router name
        output_filename = f"show_run_{student_id}_{router_name}.txt"
        print("Expected output filename:", output_filename)

        # ✅ ตรวจสอบว่า playbook สำเร็จไหม
        if 'failed=0' in stdout_result:
            if os.path.exists(output_filename):
                return 'ok', output_filename
            else:
                return 'Error: File not found after run.', None
        else:
            return 'Error: Ansible', None

    except subprocess.TimeoutExpired:
        return 'Error: Timeout expired', None
    except FileNotFoundError:
        return 'Error: ansible-playbook command not found', None
    except subprocess.CalledProcessError as e:
        print("Playbook failed:", e.stderr)
        return 'Error: Ansible', None
