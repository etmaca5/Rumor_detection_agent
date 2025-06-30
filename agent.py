from rumors_constants import *
from keyword_filter import *
from finetuned_roberta import *
from llm_labeler import *


class Agent:
    def __init__(self):
        self.keyword_filter = KeywordFilter()
        self.roberta = RobertaModel(directory=None) #TODO: change directory = None
        self.llm = LlmLabeler()
        # TODO: note should this class know about the prompts class ? Probably not so delete


    # Returns a tuple with bool, int - where bool is whether it is a rumor and int is the rumor type (if applicable)
    def classify_post(self, post):
        is_rumor = False
        is_rumor = None
        rumor_class = None
        # Step 1: Finetuned Roberta Classification
        roberta_pred = self.roberta(post)
        # Step 2: Run keyword filter on False labels
        if not roberta_pred and not self.keyword_filter.run_filter(post):
            return False, None

        # Step 3: Run initial LLM screening
        if not self.llm.initial_label(post):
            return False, None

        # Step 4: Verify that it is a rumor, getting type of rumor back
        rumor_label_pred = self.llm.verification_label_rumor_type(post):
        if not isinstance(rumor_label_pred, int):
            return False, None

        # Otherwise we have verified and can return
        return True, rumor_label_pred
    

    # TODO: def classify where you can pass in a batch of posts and get a list of tuples (or maybe a map)