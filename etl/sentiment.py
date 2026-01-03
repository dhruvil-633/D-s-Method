from etl.finbert import FinBERTScorer

finbert = FinBERTScorer()

def score_sentiment_batch(texts):
    """
    texts: list of article texts
    """
    return finbert.score_batch(texts)
