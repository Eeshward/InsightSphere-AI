import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

STOPWORDS = {
    "the","is","in","and","to","of","a","for","on","with","as","by","an","be",
    "are","this","that","from","or","at","it","was","were","has","have","had",
    "which","but","not","can","may","will","we","our","their","they","you",
    "your","into","than","also","such","these","those","its","using","used",
    "use","based","between","through","about","more","most","other","some"
}

def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def split_sentences(text: str):
    text = clean_text(text)
    if not text:
        return []
    return [
        s.strip()
        for s in re.split(r"(?<=[.!?])\s+", text)
        if len(s.strip()) > 20
    ]

def _tokenize(sentence: str):
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9_-]{2,}\b", sentence.lower())
    return [w for w in words if w not in STOPWORDS]

def extract_keywords(text: str, top_n=15):
    text = clean_text(text)
    if not text:
        return []

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=max(top_n * 3, 30),
            ngram_range=(1, 2)
        )
        matrix = vectorizer.fit_transform([text])
        features = vectorizer.get_feature_names_out()
        scores = matrix.toarray()[0]
        ranked = sorted(
            zip(features, scores),
            key=lambda x: x[1],
            reverse=True
        )
        return [(word, round(float(score), 4)) for word, score in ranked[:top_n]]
    except ValueError:
        counts = Counter(_tokenize(text))
        total = sum(counts.values()) or 1
        return [
            (word, round(count / total, 4))
            for word, count in counts.most_common(top_n)
        ]

def summarize_text(text: str, max_sentences=7):
    sentences = split_sentences(text)

    if not sentences:
        return "No readable text was found."

    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    word_freq = Counter()
    for sentence in sentences:
        word_freq.update(_tokenize(sentence))

    if not word_freq:
        return " ".join(sentences[:max_sentences])

    max_freq = max(word_freq.values())
    normalized = {w: f / max_freq for w, f in word_freq.items()}

    scored = []
    for index, sentence in enumerate(sentences):
        words = _tokenize(sentence)
        if not words:
            continue
        score = sum(normalized.get(w, 0) for w in words) / len(words)

        # Slight preference to earlier sentences because many documents
        # introduce key ideas near the beginning.
        position_bonus = 1.0 - min(index / max(len(sentences), 1), 0.4)
        scored.append((index, score * position_bonus, sentence))

    selected = sorted(scored, key=lambda x: x[1], reverse=True)[:max_sentences]
    selected = sorted(selected, key=lambda x: x[0])

    return " ".join(sentence for _, _, sentence in selected)

def get_important_points(text: str, count=8):
    sentences = split_sentences(text)
    if not sentences:
        return []

    keywords = {k.split()[0] for k, _ in extract_keywords(text, top_n=20)}
    scored = []

    for i, sentence in enumerate(sentences):
        tokens = _tokenize(sentence)
        if not tokens:
            continue

        keyword_hits = sum(1 for t in tokens if t in keywords)
        number_hits = len(re.findall(r"\b\d+(?:\.\d+)?%?\b", sentence))
        cue_hits = sum(
            cue in sentence.lower()
            for cue in [
                "important", "result", "conclusion", "objective", "problem",
                "proposed", "significant", "increase", "decrease", "accuracy",
                "performance", "method", "future", "risk", "benefit"
            ]
        )
        score = keyword_hits + (number_hits * 0.6) + (cue_hits * 1.2)
        scored.append((score, i, sentence))

    best = sorted(scored, key=lambda x: x[0], reverse=True)[:count]
    best = sorted(best, key=lambda x: x[1])
    return [s for _, _, s in best]

def analyze_text(text: str, summary_sentences=7, top_keywords=15):
    cleaned = clean_text(text)
    sentences = split_sentences(cleaned)
    words = re.findall(r"\b\w+\b", cleaned)

    return {
        "text": cleaned,
        "summary": summarize_text(cleaned, summary_sentences),
        "important_points": get_important_points(cleaned, 8),
        "keywords": extract_keywords(cleaned, top_keywords),
        "word_count": len(words),
        "sentence_count": len(sentences),
        "character_count": len(cleaned),
        "sentence_lengths": [
            len(re.findall(r"\b\w+\b", s)) for s in sentences
        ]
    }
