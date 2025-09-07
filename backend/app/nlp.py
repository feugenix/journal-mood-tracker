from transformers import pipeline

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


def analyze_sentiment(text: str, top_k: int = 3) -> tuple[str, float]:
    result = sentiment_pipeline(text[:512], top_k=top_k)[0]
    return result["label"].lower(), float(result["score"])


def analyze_emotions(text: str, top_k: int = 3) -> dict[str, float]:
    results = emotions_pipeline(text[:512], top_k=top_k)
    return {
        r["label"].lower(): float(r["score"]) for r in results
    }
