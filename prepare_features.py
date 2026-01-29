import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

vectorizer = TfidfVectorizer()

df = pd.read_csv("emails.csv")
X, y = df["text"], df["spam"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print(f"{X_train_tfidf.shape}, {X_test_tfidf.shape}")

data = {"X_train": X_train_tfidf, "y_train": y_train, "X_test": X_test_tfidf, "y_test": y_test}

joblib.dump(data, "output/data.pkl")
joblib.dump(vectorizer, "output/vectorizer.pkl")