import subprocess
import threading
import sys
from typing import Optional

def spin_up_fastapi_service(module_path: str, port: int, stdout_callback: Optional[callable] = None):
    """
    Spins up a FastAPI service using uvicorn from the given module path (e.g., 'api.services.cookies')
    on the specified port, in a separate thread. Stdout is sent to the callback or printed.
    """
    def run():
        process = subprocess.Popen(
            [
                sys.executable, "-m", "uvicorn",
                f"{module_path}:app",
                "--host", "127.0.0.1",
                "--port", str(port)
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True
        )
        for line in process.stdout:
            if stdout_callback:
                stdout_callback(line)
            else:
                print(f"[{module_path}]", line, end="")
        process.stdout.close()
        process.wait()

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return thread