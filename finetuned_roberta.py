from transformers import RobertaTokenizerFast, RobertaForSequenceClassification
import torch
import os

class RobertaModel:
    def __init__(self, directory: str = 'roberta_model'):
        self.directory = directory
        self.model = None
        self.tokenizer = None
        
        if self.directory and os.path.exists(directory):
            os.environ["TOKENIZERS_PARALLELISM"] = "false"
            try:
                self.model = RobertaForSequenceClassification.from_pretrained(directory)
                self.tokenizer = RobertaTokenizerFast.from_pretrained(directory)
                self.model.eval()
            except Exception as e:
                print(f"Warning: Could not load RoBERTa model from {directory}: {e}")
                print("RoBERTa predictions will return False for all inputs")
    
    def predict(self, post: str) -> bool:
        """Predict if a post contains disinformation"""
        if self.model is None or self.tokenizer is None:
            return False
            
        try:
            inputs = self.tokenizer(post, return_tensors='pt', truncation=True, padding=True)
            with torch.no_grad():
                outputs = self.model(**inputs)
            logits = outputs.logits
            predicted_class = logits.argmax(-1).item()
            return predicted_class == 1
        except Exception as e:
            print(f"Error during RoBERTa prediction: {e}")
            return False

        