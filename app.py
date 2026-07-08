import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
# 
# load_dotenv()


from src.main import (
    health_router, 
    prompt_management_router
    )


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5137",
    "*"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(prompt_management_router, prefix="/prompt-management", tags=["Prompt Management"])


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=3010)
    uvicorn.run('app:app')