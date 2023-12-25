from transformers import BertTokenizer, BertModel
import torch
from scipy.spatial.distance import cosine
from gensim.models import KeyedVectors
import re


class Word2Bert:
    def __init__(self, sentence1, sentence2):
        self.sentence1 = sentence1
        self.sentence2 = sentence2
        self.model_path = "C:/Users/vixha/Downloads/GoogleNews-vectors-negative300.bin"

        # Load the Word2Vec model
        self.model_w2v = KeyedVectors.load_word2vec_format(self.model_path, binary=True)

        # Load pre-trained BERT model and tokenizer
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.bert_model = BertModel.from_pretrained('bert-base-uncased')

    def preprocess(self):
        pattern = re.compile("<.*?>")
        self.sentence1 = pattern.sub(r'', self.sentence1)
        self.sentence2 = pattern.sub(r'', self.sentence2)
        pattern = re.compile(r'https?://\S+|www\.\S+')
        self.sentence1 = pattern.sub(r'', self.sentence1)
        self.sentence2 = pattern.sub(r'', self.sentence2)
        exclude = "[!\#\$%\&\(\)\*\+,\.\"/:;<=>\?@\[\\\\]\^_`\{\|\}\~0123456789]"
        self.sentence1 = self.sentence1.translate(str.maketrans('', '', exclude))
        self.sentence2 = self.sentence2.translate(str.maketrans('', '', exclude))

    # Define a function to get the Word2Vec embedding for a sentence
    def get_w2v_embedding(self, sentence):
        words = sentence.split()
        vectors = [self.model_w2v[word] for word in words if word in self.model_w2v.key_to_index]
        if vectors:
            return sum(vectors) / len(vectors)
        else:
            return None

    # Define a function to get the BERT embedding for a sentence
    def get_bert_embedding(self, sentence):
        input_ids = torch.tensor(self.tokenizer.encode(sentence, add_special_tokens=True)).unsqueeze(0)
        outputs = self.bert_model(input_ids)
        return outputs.last_hidden_state.squeeze(0).mean(dim=0).detach().numpy()

    def run(self):
        self.preprocess()
        w2v_embedding1 = self.get_w2v_embedding(self.sentence1)
        w2v_embedding2 = self.get_w2v_embedding(self.sentence2)
        bert_embedding1 = self.get_bert_embedding(self.sentence1)
        bert_embedding2 = self.get_bert_embedding(self.sentence2)
        w2v_similarity = 1 - cosine(w2v_embedding1, w2v_embedding2)
        bert_similarity = 1 - cosine(bert_embedding1, bert_embedding2)
        return w2v_similarity, bert_similarity


