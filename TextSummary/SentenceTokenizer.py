import spacy
import re


class Tokenizer:
    def __init__(self):
        self._nlp = spacy.load('en_core_web_sm', disable=['ner'])

    def tokenize_paragraphs(self, paragraphs: list):
        sentences = []
        for paragraph in paragraphs:
            sentences += self.tokenize_paragraph(paragraph)
        return sentences

    def tokenize_paragraph(self, paragraph: str):
        return [{"sentence": sent.text,
                 "sentence_tokenized": self.tokenize_sentence(sent.text)}
                for sent in self._nlp(paragraph).sents]

    def tokenize_sentence(self, sentence: str):
        sentence = re.sub("[\\n|\s]*[\d+.]+\s", " ", sentence)
        doc = self._nlp(sentence)
        tokens = [token for token in doc if not token.is_stop and token.is_alpha]
        tokens = [token.lemma_.lower() for token in tokens]
        return tokens
