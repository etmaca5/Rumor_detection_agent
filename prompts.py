"""
File containing prompts for the LLM labeler - exact replicas from original pipeline
"""
from rumor_constants import *


class PromptGenerator:
    def __init__(self):
        pass

    def get_initial_screening_prompt(self, text: str) -> str:
        """Initial screening prompt - filters for potential election rumors (chatgpt_filter_disinfo)"""
        return (
            f"Based on the following post on a political social media page, I want you to tell me if it spreading an election rumor from one or more the following rumors "
            f"(the keys/labels in the dictionary are not the rumors, the rumors are the values / sentences):\n"
            f"{RUMORS}\n"
            f"If the post is specifically spreading any of the rumors described "
            f"tell me which rumor it is spreading by returning only the key label from the rumors dictionary corresponding to the rumor. "
            f"Precision in the classification of whether or not it is a rumor crucial. Be as accurate as possible. "
            f"Also many of these posts are not necessarily about the election so those should not be classified as rumors. "
            f"For example return 'Dirty Voter Rolls' if it is related/spreading a voter roll rumor, such as election officials not cleaning the voter rolls. "
            f"If it is related to multiple rumors, label it with the first of those rumors. "
            f"If it is not related to any of the election rumors mentioned return an empty string. "
            f"For example: return '' for a post about how Trump is a better candidate than Kamala, she is stupid and lies and is a complete fraud. "
            f"Remember the post has to be about a specific rumor mentioned above for it to count as spreading the rumor, it needs to be somewhat clear that it is talking about that rumor and not something else unrelated. "
            f"You should not assume the posts are about these rumors specifically, they could be about other rumors which may sound similar. "
            f"I only care about those rumors mentioned (election interference by removing Trump as president or distracting him is not a rumor that we are trying to follow)."
            f"Now do that with this post:\n"
            f"{text}"
        )

    def get_confirmation_prompt(self, text: str) -> str:
        """Simple confirmation prompt - used by roberta path (chatgpt_confirm_disinfo)"""
        return (
            f"Based on the following posts on a political social media page, I want you to tell me if it's spreading an election rumor from one or more the following rumors: \n"
            f"{RUMORS}\n"
            f"If the post is specifically spreading any of the rumors described"
            f"tell me which rumor it is spreading by returning only the key label from the rumors dictionary which corresponds to the rumor discussed in the post."
            f"Precision in the classification of the misinformation rumor and whether or not the post is a rumor is crucial. Be as accurate as possible."
            f"For example return 'Voter Rolls' if it is related/spreading a voter roll rumor, such as election officials not cleaning the voter rolls."
            f"If it is related to multiple rumors, label it with the first of those rumors"
            f"If it is not related to any of the election rumors mentioned return an empty string '"
            f"For example: return '' for a post about how Trump is a better candidate than Kamala, she is stupid and lies and is a complete fraud."
            f"I only care about those rumors mentioned (election interference by removing Trump as president or distracting him is not a rumor that we are trying to follow)."
            f"Now do that with this post:\n"
            f"{text}"
        )

    def get_verification_prompt(self, text: str) -> str:
        """Verification prompt - confirms specific election rumors (chatgpt_confirm_disinfo)"""
        return (
            f"Based on the following post on a social media page, I want you to classify the post as rumor-spreading if it corresponds to any of the following election fraud rumors (you are only labeling based on the following election rumors, not unrelated rumors or general fraud). "
            f"If it doesn't fit with any of the rumors then I want you to return an empty string. If it does correspond with a rumor return the rumor (just the number of the rumor in the key). "
            f"It is common for users / fake news websites to invent statistics that seem like facts, giving a sense of credibility; be skeptical of claims and regard the list of rumors as the source of truth. "
            f"(for instance: saying that officials cleaned the voter rolls is not misinformation / rumor-spreading. But on the other hand saying that voter rolls are dirty because of an anecdote is misinformation and should be labeled as rumor 1). "
            f"Another example is if a post talks about facts, but then implies that there is some fraud related to the rumors, then it is misinformation. "
            f"It is absolutely crucial that you properly classify this post as one of the rumors or not, please analyze it carefully. The post may discuss the election issues mentioned but not actually spread the specific rumors discussed, these posts should not be labeled as rumor-spreading for our case "
            f"(for instance a post about there being a bizarrely high amount of votes is not necessarily spreading one of the rumors mentioned, unless it discusses specifically that one of the rumors is causing the increase in votes). "
            f"For example return 2 if the post is about how your votes can easily be prevented via mail, or that non-citizens are casting mail-in ballots."
            f"Another example is return an empty string '' if the post is about Kamala Harris being a dirty liar who wants to cheat. "
            f"Another example is return an empty string '' if the post is plainly about the election being rigged but not specifying how exactly with a provided rumor. "
            f"Here are the rumors (again be cautious about labeling a post as misinformation and make sure you only label it as misinformation if it corresponds to the rumor): \n"
            f"{RUMORS_NUMBERED}\n"
            f"Here is the post:\n"
            f"{text}"
        )