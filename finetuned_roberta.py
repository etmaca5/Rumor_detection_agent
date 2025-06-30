from transformers import RobertaTokenizerFast, RobertaForSequenceClassification
import torch

class RobertaModel:
    def __init__(self, directory):
        self.directory = directory
        if self.directory:
            self.model = RobertaForSequenceClassification.from_pretrained(directory)
            self.tokenizer = RobertaTokenizerFast.from_pretrained(directory)
    
    # TODO: look in disinfo pipeline test
    def predict(self, post):
        inputs = self.tokenizer(post, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_class = logits.argmax(-1).item()
        if predicted_class == 1:
            return True
        else:
            return False

        