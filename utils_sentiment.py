# utils_sentiment.py
import re

POS = {
    "good","great","awesome","amazing","love","loved","like","liked","happy",
    "excellent","fantastic","nice","cool","wonderful","positive","win","wins",
    "successful","success","fast","clean","smooth"
}
NEG = {
    "bad","terrible","awful","hate","hated","dislike","sad","angry","worse","worst",
    "poor","boring","bug","bugs","problem","problems","fail","failed","failure",
    "negative","slow","mess","broken","crash","crashes"
}

_word = re.compile(r"[a-z']+", re.I)

def _tokens(text: str):
    return _word.findall(text.lower())

def sentiment_score(text: str) -> float:
    toks = _tokens(text)
    if not toks:
        return 0.0
    score = 0
    for t in toks:
        if t in POS: score += 1
        if t in NEG: score -= 1
    # light normalization
    return round(score / max(3, len(toks)) * 10, 3)

def sentiment_label(text: str):
    s = sentiment_score(text)
    if s > 0.05: return "positive", s
    if s < -0.05: return "negative", s
    return "neutral", s
