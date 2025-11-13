from pydantic import BaseModel


class CodeRequest(BaseModel):
    """Schema for code execution request."""
    code: str


class CodeResponse(BaseModel):
    """Schema for code execution response."""
    stdout: str
    stderr: str
