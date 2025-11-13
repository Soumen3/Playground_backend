import subprocess
import tempfile
import os


# List of restricted modules that shouldn't be imported
RESTRICTED_MODULES = [
    'os', 'sys', 'subprocess', 'shutil', 'pathlib',
    'socket', 'urllib', 'requests', 'http',
    '__import__', 'eval', 'exec', 'compile',
    'open', 'file', 'input', 'raw_input'
]

def check_code_safety(code: str) -> tuple[bool, str]:
    """
    Check if the code contains potentially dangerous operations.
    Returns (is_safe, error_message)
    """
    code_lower = code.lower()
    
    # Check for restricted imports
    for module in RESTRICTED_MODULES:
        if f'import {module}' in code_lower or f'from {module}' in code_lower:
            return False, f"Security Error: Module '{module}' is not allowed for security reasons."
    
    # Check for file operations
    dangerous_keywords = ['open(', 'file(', 'os.', 'sys.', 'subprocess.', 'shutil.', '__import__']
    for keyword in dangerous_keywords:
        if keyword in code_lower:
            return False, f"Security Error: Operation '{keyword}' is not allowed for security reasons."
    
    return True, ""


def run_code(code: str):
    # First, check code safety
    is_safe, error_msg = check_code_safety(code)
    if not is_safe:
        return {
            "stdout": "",
            "stderr": error_msg
        }
    
    # Use delete=False to avoid file locking issues on Windows
    temp_file = tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w")
    try:
        # Add restricted builtins to prevent dangerous operations
        safe_code = """
import sys
# Disable dangerous builtins
__builtins__.__dict__['open'] = None
__builtins__.__dict__['__import__'] = None
__builtins__.__dict__['eval'] = None
__builtins__.__dict__['exec'] = None
__builtins__.__dict__['compile'] = None
__builtins__.__dict__['input'] = None

# User code starts here
"""
        temp_file.write(safe_code + code)
        temp_file.close()  # Close the file so subprocess can access it on Windows
        
        result = subprocess.run(
            ["python3", temp_file.name],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=tempfile.gettempdir()  # Run in temp directory to limit file access
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Error: Code execution timed out (5 second limit)."
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