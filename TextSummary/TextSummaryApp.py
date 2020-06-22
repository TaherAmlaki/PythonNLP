import sys
from concurrent.futures import ThreadPoolExecutor
from RetrieveDataFromWiki import get_data_from_title
from SentenceTokenizer import Tokenizer
from WordFrequency import generate_word_frequency_map_from_sentences
from DocumentTermMatrix import get_dtm_for_sentences
import numpy as np


if __name__ == "__main__":
    title = sys.argv[1]
    try:
        number_of_sentences = int(sys.argv[2])
    except (IndexError, ValueError):
        number_of_sentences = 3

    with ThreadPoolExecutor() as executor:
        future = executor.submit(get_data_from_title, title)
        tokenizer = Tokenizer()
        paragraphs = future.result()[-1]
    sentences = tokenizer.tokenize_paragraphs(paragraphs)
    word_frequencies = generate_word_frequency_map_from_sentences(sentences)
    for sent_ind in range(len(sentences)):
        sent_dict = sentences[sent_ind]
        score = sum([word_frequencies.get(token, 0) for token in sent_dict.get("sentence_tokenized", [])])
        sent_dict.update({"score": score})

    res = [s['sentence'] for s in sorted(sentences, key=lambda item: -item['score'])]
    res = ' '.join(res[:number_of_sentences])
    print("=====================================================================")
    print(res)
    print("=====================================================================")

    dtm, vectorizer = get_dtm_for_sentences([' '.join(sent['sentence_tokenized']) for sent in sentences])
    scores = dtm.sum(axis=1)
    scores = np.squeeze(np.asarray(scores))
    scores = np.argsort(-scores)[:number_of_sentences]
    res = [sentences[i]['sentence'] for i in scores]
    print(' '.join(res))
