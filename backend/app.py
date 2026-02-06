from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from prediction import predict

app = FastAPI()

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