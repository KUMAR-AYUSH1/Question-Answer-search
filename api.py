from fastapi import FastAPI
from pydantic import BaseModel,Field
import pandas as pd

df = pd.read_csv("cleaned_data.csv")
import joblib

vectorizer = joblib.load("vectorizer.joblib")
knn = joblib.load("knn_model.joblib")
import re
from nltk.corpus import stopwords

def clean_data(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9]", ' ', text) # remove special characters
    text = re.sub(r"\s+", ' ', text) # remove extra spaces
    text = ' '.join([word for word in text.split() if word not in (stopwords.words('english'))])
    return text


app = FastAPI(
    title="Question Answer Search API",
    version="1.0.0"
)

class Item(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        examples=["What is anomaly detection?"]
    )

@app.get("/")
async def root():
    return {"message": "API for question answering search"}

@app.post("/ask")
async def ask(item: Item):
    question = item.question
    question = clean_data(question)
    question = vectorizer.transform([question])
    question = knn.kneighbors(question, return_distance=False)[0][0]
    answer = df.iloc[question]['Answer']
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)