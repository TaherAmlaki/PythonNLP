from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def get_dtm_for_sentences(sentences: list):
    vectorizer = TfidfVectorizer(max_features=2000)
    sentences = vectorizer.fit_transform(sentences)
    return sentences, vectorizer
