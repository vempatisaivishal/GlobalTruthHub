from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_sentence_similarity(sentence1, sentence2):
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    exclude = '[!\#\$%\&\(\)\*\+,\.\"/:;<=>\?@\[\^_`\{\|\}\~]'
    sentence_embeddings = model.encode([sentence1.translate(str.maketrans('', '', exclude)).lower(), sentence2.translate(str.maketrans('', '', exclude)).lower()])
    similarity = cosine_similarity([sentence_embeddings[0]], [sentence_embeddings[1]])[0][0]

    return similarity

# print(calculate_sentence_similarity("rcb didn't qualify for semi finals in 2023", "rcb didn't won the 2023 cup"))