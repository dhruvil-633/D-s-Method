import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

MODEL_NAME = "ProsusAI/finbert"

class FinBERTScorer:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        self.model.eval()

        # label mapping used by FinBERT
        self.label_map = {0: -1, 1: 0, 2: 1}

    @torch.no_grad()
    def score_batch(self, texts):
        """
        texts: list[str]
        returns: float sentiment in [-1, 1]
        """

        if not texts:
            return 0.0

        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="pt"
        )

        outputs = self.model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)

        # expected sentiment value
        scores = []
        for p in probs:
            score = sum(
                p[i].item() * self.label_map[i]
                for i in range(3)
            )
            scores.append(score)

        return float(np.mean(scores))
