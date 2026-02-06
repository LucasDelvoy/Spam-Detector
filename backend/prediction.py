import re
import nltk
import joblib
from nltk.corpus import stopwords
from fastapi import HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
from torch import FloatTensor, no_grad
from model import load_model

empty_words = nltk.download("stopwords")
stopwords_list = set(stopwords.words("english"))
vectorizer = joblib.load("../output/vectorizer.pkl")
model = load_model()


def clean_text(text):
    txt = text.lower()
    x = re.sub(r'[^a-zA-Z]', " ", txt)
    words = x.split()

    clean_words = [word for word in words if word not in stopwords_list]
    cleaned_text = " ".join(clean_words)
    return cleaned_text

def prediction_score(score):

    if score.item() > 0.95:
        return "Obvious Spam"
    
    elif 0.8 <= score.item() <= 0.95:
        return "Potential Spam"
    
    elif 0.6 <= score.item() < 0.8:
        return "Suspicious Mail"
    
    else:
        return "Mail"
    
def predict(email):
    if not email.strip():
        return HTTPException(status_code=400, detail="Email is empty")
    
    if not isinstance(email, str):
        return HTTPException(status_code=400, detail="Please write a correct email")
    
    if len(email) >= 5000:
        return HTTPException(status_code=400, detail="Email is too long (max 5k characters)")

    cleaned_mail = clean_text(email)
    vect_mail = vectorizer.transform([cleaned_mail])
    mail = FloatTensor(vect_mail.toarray())
    
    with no_grad():
        score = model(mail)
        score_percentage = "{:.1%}".format(score.item())
        result = prediction_score(score)

        if score.item() > 0.8:
            return {"status": "spam",
                    "score": score_percentage,
                    "prediction": result}
        else:
            return {"status": "mail",
                    "score": score_percentage,
                    "prediction": result}