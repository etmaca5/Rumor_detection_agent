from rumors_constants import *
from keyword_filter import KeywordFilter
from finetuned_roberta import RobertaModel
from llm_labeler import LlmLabeler
from typing import Tuple, Optional, List, Dict


class Agent:
    def __init__(self, roberta_model_path: str = None, openai_api_key: Optional[str] = None):
        self.keyword_filter = KeywordFilter()
        self.roberta = RobertaModel(directory=roberta_model_path)
        self.llm = LlmLabeler(api_key=openai_api_key)

    def classify(self, post: str) -> Tuple[bool, Optional[int]]:
        """Classify a single post through the complete pipeline"""
        
        # Step 1: Finetuned RoBERTa Classification
        roberta_pred = self.roberta.predict(post)
        
        # Step 2: Run keyword filter on False labels
        if not roberta_pred and not self.keyword_filter.run_filter(post):
            return False, None

        # Step 3: Run initial LLM screening
        if not self.llm.initial_label(post):
            return False, None

        # Step 4: Verify that it is a rumor, getting type of rumor back
        rumor_label_pred = self.llm.verification_label_rumor_type(post)
        if not isinstance(rumor_label_pred, int):
            return False, None

        return True, rumor_label_pred
    
    def classify_batch(self, posts: List[str]) -> List[Tuple[bool, Optional[int]]]:
        """classify a batch of posts"""
        results = []
        for post in posts:
            result = self.classify_post(post)
            results.append(result)
        return results
    
    def get_rumor_info(self, rumor_type: int) -> Optional[str]:
        """Get the description of a rumor type"""
        return RUMORS.get(rumor_type)