import joblib
import string
import re
import openai
import numpy as np
from transformers import BertTokenizer, BertModel
import torch


class selfModel:
    def __init__(self, text):
        self.model = joblib.load("C:/Users/vixha/Downloads/model23.pkl")
        self.text = text
        self.API_KEY = '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'
        openai.api_key = self.API_KEY
        self.bert_model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    def preprocess(self):
        text = self.text
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\d+', '', text)
        return text

    def tokenize(self):
        tokens_sent1 = self.tokenizer.encode(self.text, add_special_tokens=True)
        with torch.no_grad():
            outputs1 = self.bert_model(torch.tensor([tokens_sent1]))
        embeddings = np.mean(outputs1[2][-4].squeeze().numpy(), axis=0)
        return embeddings

    def run(self):
        self.text = self.preprocess()
        embedding = self.tokenize()
        prediction = self.model.predict([embedding])
        return prediction
