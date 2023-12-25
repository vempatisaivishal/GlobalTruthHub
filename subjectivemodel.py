import json
import requests
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch


class subjective:
    def __init__(self):
        self.headers = {"Authorization": "Bearer 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"}
        self.API_URL = "https://api-inference.huggingface.co/models/lighteternal/fact-or-opinion-xlmr-el"
        self.model_name = "lighteternal/fact-or-opinion-xlmr-el"
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def api_request(self, text):
        data = self.query({"text": text})
        print(data)
        data1, label = data[0]['score'], data[0]['label']
        if label == 'LABEL_0':
            return "subjective"
        else:
            return "objective"

    def query(self, payload):
        send_data = json.dumps(payload)
        response = requests.request("POST", self.API_URL, headers=self.headers, data=send_data)
        return json.loads(response.content.decode("utf-8"))

    def send_request(self, text):
        inputs = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')

        with torch.no_grad():
            outputs = self.model(**inputs)

        predicted_label = torch.argmax(outputs.logits).item()

        if predicted_label == 0:
            return "subjective"

        else:
            return "objective"
