def generate_word_frequency_map_from_sentences(sentences: list):
    words_frequencies = {}
    for sent_dict in sentences:
        for token in sent_dict.get("sentence_tokenized"):
            if words_frequencies.get(token) is None:
                words_frequencies[token] = 1
            else:
                words_frequencies[token] += 1
    return words_frequencies
