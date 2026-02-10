from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from prediction import predict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailInput(BaseModel):
    email: str
    
@app.get("/")
async def read_root():
    return{"Hello": "World"}

@app.get("/health")
async def read_health():
    return

@app.post("/predict")
async def read_predict(request: Request, payload: EmailInput):
    prediction = predict(payload.email)
    return prediction