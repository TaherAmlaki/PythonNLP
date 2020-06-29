from sklearn.utils.extmath import randomized_svd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
from Tokenizer import Tokenizer


class LsaSummarizer:
    def __init__(self, request):
        self._text = request.get("text")
        max_vocab = request.get("VocabSize")
        self._max_vocab = max_vocab if max_vocab is not None else 1000
        topics_size = request.get("NumberOfSentencesInSummary")
        self._n_components = topics_size if topics_size is not None else 3
        self._id = request.get("id")
        self._vectorizer_arg = request.get("DocTermMatrixCalculation")
        self._method = request.get("SentenceSelectionMethod")
        self._title = request.get("title")

    def start(self, queue):
        tokenizer = Tokenizer()
        tokenized_text = tokenizer.tokenize_paragraph(self._text)
        sentences = [sent for sent, _ in tokenized_text]
        tokenized_text = [' '.join(sent) for _, sent in tokenized_text]

        vectorizer = self._get_vectorizer()
        dtm = vectorizer.fit_transform(tokenized_text)

        u, sigma, vT = randomized_svd(dtm.T,
                                      n_components=self._n_components,
                                      n_iter=5,
                                      random_state=None)
        sigma = np.diag(sigma)
        scores = self._sentence_selection(vT, sigma)
        scores.sort()
        summary = ' '.join([sentences[i] for i in scores])
        similarity = tokenizer.calculate_similarity(self._text, summary)
        res = {"id": self._id, "summary": summary, "similarity": similarity, 'status': "done"}
        if self._title is not None:
            res['title'] = self._title
        queue.put(res)

    def _get_vectorizer(self):
        if self._vectorizer_arg is None or self._vectorizer_arg.lower() == "tf-idf":
            vectorizer = TfidfVectorizer(max_features=self._max_vocab)
        elif self._vectorizer_arg.lower() == "wf":
            vectorizer = CountVectorizer(max_features=self._max_vocab)
        else:
            vectorizer = CountVectorizer(max_features=self._max_vocab, binary=True)
        return vectorizer

    def _sentence_selection(self, vT, sigma) -> list:
        if self._method is not None and self._method == "SJ":
            new_arr = np.matmul(sigma, sigma)
            new_arr = np.matmul(new_arr, vT)
            scores = np.sum(np.abs(new_arr) ** 2, axis=0) ** (1.0 / 2)
            return np.argsort(-scores)[:self._n_components].tolist()
        else:
            # the method used here is GL
            return list(set(np.argmax(vT, axis=1).tolist()))
