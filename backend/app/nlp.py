from transformers import pipeline
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT

kw_model = KeyBERT(model=SentenceTransformer("all-MiniLM-L6-v2"))


sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    return_all_scores=False,
)

emotions_pipeline = pipeline(
    "sentiment-analysis",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=False,
    top_k=None,
)

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def analyze_sentiment(text: str, top_k: int = 3) -> tuple[str, float]:
    result = sentiment_pipeline(text[:512], top_k=top_k)[0]
    return result["label"].lower(), float(result["score"])


def analyze_emotions(text: str, top_k: int = 3) -> dict[str, float]:
    results = emotions_pipeline(text[:512], top_k=top_k)
    return {r["label"].lower(): float(r["score"]) for r in results}


def get_embedding(text: str) -> list[float]:
    return embedding_model.encode(text, normalize_embeddings=True).tolist()


def extract_keywords(text: str, top_k: int = 5):
    keywords = kw_model.extract_keywords(
        text, keyphrase_ngram_range=(1, 2), stop_words="english", top_n=top_k
    )
    return [word for word, score in keywords]
