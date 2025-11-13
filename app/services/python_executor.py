import subprocess
import tempfile
import os


def run_code(code: str):
    # Use delete=False to avoid file locking issues on Windows
    temp_file = tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w")
    try:
        temp_file.write(code)
        temp_file.close()  # Close the file so subprocess can access it on Windows
        
        result = subprocess.run(
            ["python3", temp_file.name],
            capture_output=True,
            text=True,
            timeout=5
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Error: Code execution timed out."
        }
    finally:
        # Manually delete the temp file
        try:
            os.unlink(temp_file.name)
        except Exception:
            pass  # Ignore errors during cleanup

    return None


if __name__ == "__main__":
    # Example usage
    print(run_code("print('Hello, World!')"))