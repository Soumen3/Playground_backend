from fastapi import APIRouter
from schemas.playground import CodeRequest, CodeResponse
from services.python_executor import run_code

router = APIRouter(
    prefix="/playground",
    tags=["playground"]
)



@router.post("/execute", response_model=CodeResponse)
async def execute_code(request: CodeRequest):
    """
    Execute Python code and return the output.
    """
    result = run_code(request.code)
    return CodeResponse(**result)
