"""
File containing prompts for the LLM labeler
"""
from rumors_constants import RUMORS


class PromptGenerator:
    def __init__(self):
        self.initial_system_prompt = (
            "You are analyzing social media posts to identify potential election rumors. "
            "Be precise in classification - only flag posts that clearly spread the specific rumors listed. "
            "There are many posts about elections that are NOT spreading these specific rumors."
        )
        
        self.verification_system_prompt = (
            "You are performing final verification of potential election misinformation with high precision. "
            "Only classify posts as rumor-spreading if they precisely match the listed rumors. "
            "Distinguish between election talk / facts and actual rumor-spreading."
        )

    def get_initial_screening_prompt(self, text: str) -> str:
        """Initial screening prompt"""
        return (
            f"{self.initial_system_prompt}\n\n"
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
            f"The majority of posts you receive should not be about these rumors, and you should not assume the posts are about these rumors specifically, they could be about other rumors which may sound similar. "
            f"I only care about those rumors mentioned (election interference by removing Trump as president or distracting him is not a rumor that we are trying to follow)."
            f"Now do that with this post:\n"
            f"{text}"
        )

    def get_verification_prompt(self, text: str) -> str:
        """Final verification prompt"""
        return (
            f"{self.verification_system_prompt}\n\n"
            f"Based on the following post on a social media page, I want you to classify the post as rumor-spreading if it corresponds precisely to any of the following election fraud rumors (you are only labeling based on the following election rumors, not unrelated rumors or general fraud). "
            f"The post should also not be denying the specific rumor it should be spreading it for it to be considered disinformation. "
            f"If it doesn't exactly fit with any of the rumors then I want you to return an empty string. If it does correspond with a specific rumor return the rumor (just the number of the rumor in the key). "
            f"It could also be that the post is about correct facts related to a rumor and is not actually spreading falsehoods / not being accusatory about the specific rumor, please judge how correct these facts seem based on the given rumors "
            f"(for instance saying someone cleaned voter rolls is not disinformation / is not rumor-spreading. But on the other hand saying that voter rolls are dirty because of an anecdote is disinformation and should be labeled as 1). "
            f"Another example is if a post talks about facts, but then implies that there is some fraud related to the rumors, then it is disinformation. "
            f"It is absolutely crucial that you properly classify this post as one of the rumors or not, please analyze it carefully. The post may discuss the election issues mentioned but not actually spread the specific rumors discussed, these posts should not be labeled as rumor-spreading for our case. "
            f"it is common for the post being about election fraud and not being considered rumor spread (for instance a general post about there being an impossible amount of votes is not rumor spreading, unless it discusses specifically that one of the rumors is causing the increase in votes) "
            f"For example return 1 if it is spreading a voter roll rumor, such as election officials not cleaning the voter rolls and thus leading to rigging. "
            f"Another example is return an empty string '' if the post is about Kamala Harris being a dirty liar who wants to cheat. "
            f"Another example is return an empty string '' if the post is plainly about the election being rigged but not specifying how exactly with a provided rumor. "
            f"Another example is return an empty string '' if the post states that voter rolls are being cleaned / ineligible. On the other hand stating that voter rolls need to be cleaned or the election will be rigged should return 1. "
            f"Here are the rumors (again be cautious about labeling a post as disinformation and make sure you only label it as disinformation if it corresponds to the rumor): \n"
            f"{RUMORS}\n"
            f"Here is the post:\n"
            f"{text}"
        )