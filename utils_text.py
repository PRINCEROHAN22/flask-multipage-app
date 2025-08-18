import re
from collections import Counter

STOPWORDS = {
    "the","a","an","and","or","but","if","while","of","to","in","on","for","with",
    "as","by","is","are","was","were","be","been","being","at","from","that","this",
    "it","its","into","about","over","under","after","before","than","then","so"
}

def split_sentences(text: str):
    # simple sentence splitter
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in parts if s.strip()]

def summarize(text: str, max_sentences: int = 2):
    sentences = split_sentences(text)
    if not sentences:
        return ""
    # build word frequency table
    words = re.findall(r"[a-zA-Z0-9']+", text.lower())
    freq = Counter(w for w in words if w not in STOPWORDS)
    if not freq:
        return " ".join(sentences[:max_sentences])

    # score sentences
    scores = []
    for idx, s in enumerate(sentences):
        s_words = re.findall(r"[a-zA-Z0-9']+", s.lower())
        score = sum(freq.get(w, 0) for w in s_words)
        scores.append((idx, score, s))

    # pick top-k by score, then restore original order
    top = sorted(scores, key=lambda t: t[1], reverse=True)[:max_sentences]
    top_sorted = [s for (_, _, s) in sorted(top, key=lambda t: t[0])]
    return " ".join(top_sorted)