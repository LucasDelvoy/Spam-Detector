import joblib
import nltk
import re
from torch import nn, optim, FloatTensor, load, no_grad
from typing import Union
from fastapi import FastAPI, Request, Form
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from pydantic import BaseModel

app = FastAPI()
empty_words = nltk.download("stopwords")
stopwords_list = set(stopwords.words("english"))

class EmailInput(BaseModel):
    email: str

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.layer1 = nn.Linear(10000, 128)
        self.first_filter = nn.ReLU()
        self.hidden_layer = nn.Linear(128, 16)
        self.second_filter = nn.ReLU()
        self.layer2 = nn.Linear(16, 1)
        self.last_filter = nn.Sigmoid()
    
    def forward(self, x):
        x = self.layer1(x)
        x = self.first_filter(x)
        x = self.hidden_layer(x)
        x = self.second_filter(x)
        x = self.layer2(x)
        x = self.last_filter(x)
        return x

try:
    model = Model()
    model.load_state_dict(load("../output/model.pth", weights_only=True))
    model.eval()
    print("Model successfully loaded!")
except FileNotFoundError:
    print("Couldn't find model")
    model = None
except Exception as e:
    print(f"Error loading model: {e}")
    
vectorizer = joblib.load("../output/vectorizer.pkl")

def clean_text(text):
    txt = text.lower()
    x = re.sub(r'[^a-zA-Z]', " ", txt)
    words = x.split()

    clean_words = [word for word in words if word not in stopwords_list]
    cleaned_text = " ".join(clean_words)
    return cleaned_text

@app.get("/")
async def read_root():
    return{"Hello": "World"}

@app.get("/health")
async def read_health():
    if model is not None:
        return("Model Loaded")
    else:
        return("Error, model not loaded")

@app.post("/predict")
async def read_predict(request: Request, payload: EmailInput):
    
    cleaned_mail = clean_text(payload.email)
    vect_mail = vectorizer.transform([cleaned_mail])
    mail = FloatTensor(vect_mail.toarray())
    
    with no_grad():
        score = model(mail)

        if score.item() > 0.8:
            return {"status": "spam"}
        else:
            return {"status": "mail"}