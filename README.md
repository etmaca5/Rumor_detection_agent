# Rumor Detection Agent

A multi-stage agent for detecting and classifying election-related rumors in social media posts. Combines fine-tuned RoBERTa models, keyword filtering, and LLM verification for precision rumor detection of social media posts.

## Architecture

The system uses a sequential filtering approach:

1. **RoBERTa Model**: Fine-tuned transformer for initial disinformation detection
2. **Keyword Filter**: Rule-based filtering using election-specific keywords  
3. **LLM Screening**: GPT-based initial rumor identification
4. **LLM Verification**: Strict classification into specific rumor types

This multi-stage design ensures high precision by requiring posts to pass multiple verification steps.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up OpenAI API key:
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

## Usage

### Single Post Classification
```python
from agent import Agent

agent = Agent()
is_rumor, rumor_type = agent.classify("The voter rolls are dirty!")

if is_rumor:
    print(f"Rumor Type: {rumor_type}")
    print(f"Category: {agent.get_rumor_category(rumor_type)}")
```

### CSV File Processing
```python
# defaults to included example posts
results = agent.classify_csv()

# Process custom CSV with detailed output
results = agent.classify_csv("your_posts.csv", verbose=True)
```

### Batch Processing
```python
posts = [
    "The election process is fundamentally fair",
    "Dead people are voting in this election",
    "The mail-in ballot system is fraudulent"
]

results = agent.classify_batch(posts)
```


## Election Rumor Types

This framework detects 16 specific election rumors as examples of the types of misinformation that can be identified:

1. **Dirty Voter Rolls**: Election officials don't clean the voter rolls. The voter rolls are inaccurate and they are not updated.
2. **Ballot Mail-In Fraud**: People can easily violate the integrity of the mail-in/absentee ballot request process to receive and cast unauthorized mail-in/absentee ballots, or prevent authorized voters from voting successfully in person.
3. **Drop Box Tampering**: Drop boxes used by election officials to collect returned mail-in/absentee ballots can be easily tampered with, stolen, or destroyed.
4. **Software Security**: Voting system software is not reviewed or tested and can be easily manipulated.
5. **Dead Voters**: Votes are being cast on behalf of dead people and these votes are being counted.
6. **Voter Registration Data Breach**: Someone possessing or posting voter registration data means voter registration databases have been hacked.
7. **Voter Registration Website Outage**: An online voter registration website experiences an outage and claims are made the election has been compromised.
8. **Hacking into Jurisdictions**: If state or local jurisdiction information technology (IT) has been compromised, the election results cannot be trusted.
9. **Voter Registration Manipulation**: Videos, images or emails suggesting voter registration information is being manipulated means voters will not be able to vote.
10. **Extra Mail-in Ballots**: A malicious actor can easily defraud an election by printing and sending in extra mail-in ballots.
11. **Ballot FWAB Fraud**: A malicious actor can easily defraud an election using the Federal Write-In Absentee Ballot (FWAB).
12. **Ballot Scanner Issues**: Problems with ballot scanners at my voting site mean that my ballot won’t be counted.
13. **Ballot Writing Instrument Issue**: Poll workers gave specific writing instruments, such as Sharpies, only to specific voters to cause their ballots to be rejected.
14. **Voter Intimidation Tactics**: Observers in the polling place are permitted to intimidate voters, campaign, and interfere with voting.
15. **Nonexistent Vote Disclosure**: Someone is claiming to know who I voted for.
16. **Polling Lookup Outage**: If polling place lookup sites experience an outage, election infrastructure must have been compromised.

These categories demonstrate how the framework can be applied to systematically detect domain-specific misinformation patterns.

## Configuration

### Custom Keywords

```python
from keyword_filter import KeywordFilter

# Add custom keywords
custom_filter = KeywordFilter(additional_keywords=["custom_keyword"])

# Or replace entirely
custom_filter = KeywordFilter(
    additional_keywords=["word1", "word2"], 
    overwrite_keywords=True
)
```

### Different LLM Models

```python
from llm_labeler import LlmLabeler

# Use a different model or temperature
labeler = LlmLabeler(model="gpt-4", temperature=0.1)
```


## Development

### Adding New Rumor Detection

1. Update `RUMORS` dictionary in `rumors_constants.py`
2. Add relevant keywords to `keyword_filter.py`
3. Update prompts in `prompts.py` if needed
