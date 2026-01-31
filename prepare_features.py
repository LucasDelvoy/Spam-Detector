import re
import nltk
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import joblib

vectorizer = TfidfVectorizer(sublinear_tf=True, 
                             max_features=10000, 
                             ngram_range=(1, 2), 
                             min_df=3)

empty_words = nltk.download("stopwords")
stopwords_list = set(stopwords.words("english"))

def clean_text(text):
    txt = text.lower()
    x = re.sub(r'[^a-zA-Z]', " ", txt)
    words = x.split()

    clean_words = [word for word in words if word not in stopwords_list]
    cleaned_text = " ".join(clean_words)
    return cleaned_text

df = pd.read_csv("emails.csv")
df["text"] = df["text"].apply(clean_text)
X, y = df["text"], df["spam"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print(f"{X_train_tfidf.shape}, {X_test_tfidf.shape}")

data = {"X_train": X_train_tfidf, "y_train": y_train, "X_test": X_test_tfidf, "y_test": y_test}

joblib.dump(data, "output/data.pkl")
joblib.dump(vectorizer, "output/vectorizer.pkl")