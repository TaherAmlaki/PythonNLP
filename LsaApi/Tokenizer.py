import spacy
import re


class Tokenizer:
    def __init__(self, nlp=None, custom_stopwords: list = None):
        self._nlp = nlp
        if self._nlp is None:
            self._nlp = spacy.load('en_core_web_md')
        if custom_stopwords:
            for word in custom_stopwords:
                lexeme = self._nlp.vocab[word]
                lexeme.is_stop = True

    def tokenize_paragraph(self, paragraph: str):
        return [(sent.text, self.tokenize_sentence(sent.text)) for sent in self._nlp(paragraph).sents]

    def tokenize_sentence(self, sentence: str):
        sentence = re.sub("[\\n|\s]*[\d+.]+\s", " ", sentence)
        doc = self._nlp(sentence)
        tokens = [token for token in doc if not token.is_stop and token.is_alpha]
        tokens = [token.lemma_.lower() for token in tokens if 2 < len(token)]
        return tokens

    def calculate_similarity(self, doc1, doc2):
        doc1 = self._nlp(doc1)
        doc2 = self._nlp(doc2)
        similarity = round(doc1.similarity(doc2) * 100.0)
        return f"{similarity}%"
