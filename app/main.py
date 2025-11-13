from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import include_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

include_router(app)

@app.get("/")
async def read_root():
    return {"Message": "Welcome to the Python Playground Backend!"}