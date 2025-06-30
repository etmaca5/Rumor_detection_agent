# Rumor_detection_agent
Truth Social Rumor Detection Agent - used to find Election Rumor posts on Truth Social

SPEC:
# TODO: make as generalizable as possible + add instructions

Create a agent (basically brain file) which will call each pieces of the system, within this:
1. Call to the roberta model, a seperate class
2. Call to keyword class, which also can take in arguments for additional keywords to consider
3. Call to an LLM class, args: LLM classifier - default chatgpt4omini, temperature 0, etc.
4. Need a class with the mapping of rumors + type of rumors
4. Prompt class which basically just returns a string, need system prompt + regular prompt parameters

additional requirements:
5. Logging of everything
6. Output format? 
7. Write instructions for how to use it here


# TODO: Should show another folder for how the syntethic data for the roberta model was generated
# TODO: why not also do some unit testing on each of the classes
# TODO: figure out if the model is small enough to just push to git
