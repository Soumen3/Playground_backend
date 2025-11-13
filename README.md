# 🐍 Python Playground - Backend

A secure FastAPI backend server that executes Python code in a sandboxed environment. Built with security-first principles to safely run user-submitted Python code with proper restrictions and timeout limits.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi)
![Security](https://img.shields.io/badge/Security-First-red?style=for-the-badge&logo=security)

## ✨ Features

- 🚀 **Fast API** - High-performance async API with FastAPI
- 🛡️ **Secure Execution** - Multi-layer security to prevent malicious code
- ⏱️ **Timeout Protection** - 5-second execution limit prevents infinite loops
- 🔒 **Module Restrictions** - Blocks dangerous imports (os, sys, subprocess, etc.)
- 🌐 **CORS Enabled** - Ready for frontend integration
- 📝 **Input Validation** - Pydantic schemas for request/response validation
- 🔍 **Code Analysis** - Pre-execution safety checks
- 🎯 **RESTful API** - Clean, well-documented endpoints

## 🛡️ Security Features

### Multi-Layer Protection

1. **Pre-Execution Code Analysis**
   - Scans for restricted module imports
   - Detects dangerous keywords and operations
   - Returns security errors before execution

2. **Restricted Modules**
   - File system: `os`, `sys`, `pathlib`, `shutil`
   - Network: `socket`, `urllib`, `requests`, `http`
   - Execution: `eval`, `exec`, `compile`, `__import__`
   - I/O: `open`, `file`, `input`

3. **Runtime Protection**
   - Disables dangerous built-in functions
   - Sets `open`, `eval`, `exec`, etc. to `None`
   - Prevents dynamic code execution

4. **Environment Isolation**
   - Runs in temporary directory
   - Limited file system access
   - Subprocess execution with timeout

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Runtime:** Python 3.8+
- **Validation:** Pydantic
- **CORS:** FastAPI CORS Middleware
- **Server:** Uvicorn (ASGI server)

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Soumen3/Playground_backend.git
   cd Playground_backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the server:**
   ```bash
   cd app
   uvicorn main:app --reload
   ```

6. **Access the API:**
   - API: `http://localhost:8000`
   - Docs: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## 📝 API Endpoints

### Root Endpoint
```http
GET /
```
**Response:**
```json
{
  "Message": "Welcome to the Python Playground Backend!"
}
```

### Execute Code
```http
POST /playground/execute
```

**Request Body:**
```json
{
  "code": "print('Hello, World!')"
}
```

**Response:**
```json
{
  "stdout": "Hello, World!\n",
  "stderr": ""
}
```

**Error Response (Security):**
```json
{
  "stdout": "",
  "stderr": "Security Error: Module 'os' is not allowed for security reasons."
}
```

**Error Response (Timeout):**
```json
{
  "stdout": "",
  "stderr": "Error: Code execution timed out (5 second limit)."
}
```

## 📁 Project Structure

```
Playground_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py           # API router configuration
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── routes/
│   │           ├── __init__.py
│   │           └── playground.py  # Playground endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Configuration settings
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── playground.py       # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   └── python_executor.py  # Code execution logic
│   └── utils/
│       ├── __init__.py
│       └── logger.py           # Logging utilities
├── tests/
│   └── test_playground.py      # Unit tests
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔧 Configuration

### CORS Settings

CORS is configured to allow all origins for development. For production, update `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Timeout Settings

Default timeout is 5 seconds. To change, edit `services/python_executor.py`:

```python
result = subprocess.run(
    ["python3", temp_file.name],
    capture_output=True,
    text=True,
    timeout=5  # Change this value
)
```

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

Test specific file:
```bash
pytest tests/test_playground.py
```

## 🚀 Deployment

### Production Considerations

1. **Use a production ASGI server:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

2. **Set specific CORS origins:**
   - Update `allow_origins` to match your frontend domain

3. **Add rate limiting:**
   - Implement rate limiting to prevent abuse

4. **Container isolation:**
   - Consider Docker containers for better isolation

5. **Monitoring:**
   - Add logging and monitoring for production use

### Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📊 API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 🔒 Security Warnings

⚠️ **Important Security Notes:**

1. This is a demonstration project - **NOT production-ready** for untrusted users
2. Additional security layers needed for public deployment:
   - Container isolation (Docker)
   - Resource limits (CPU, memory)
   - Network isolation
   - Rate limiting
   - User authentication

3. The current implementation prevents common attacks but should not be exposed to untrusted users without additional hardening

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Related

- [Frontend Repository](../Playground_frontend) - React frontend for the playground
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 💡 Tips

- Always activate the virtual environment before running the server
- Use `--reload` flag during development for auto-restart
- Check `/docs` endpoint for interactive API testing
- Monitor console output for debugging information
- Test security restrictions with sample malicious code

---

Built with 🚀 FastAPI and ❤️ for Python
