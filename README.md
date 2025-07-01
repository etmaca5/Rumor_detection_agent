# Rumor Detection Agent

A comprehensive system for detecting and classifying election-related rumors and misinformation in social media posts. The agent uses a multi-stage pipeline combining fine-tuned RoBERTa models, keyword filtering, and LLM-based verification to accurately identify and categorize different types of election rumors.

## Features

- **Multi-stage Classification Pipeline**: Combines multiple approaches for high accuracy
- **16 Rumor Categories**: Covers various types of election-related misinformation (TODO: add link to )
- **Flexible Architecture**: Easy to extend with additional models or filters
- **Batch Processing**: Support for processing multiple posts at once
- **Robust Error Handling**: Graceful fallbacks when components are unavailable

## Architecture

The system consists of several key components:

1. **RoBERTa Model** (`finetuned_roberta.py`): Fine-tuned transformer model for initial disinformation detection
2. **Keyword Filter** (`keyword_filter.py`): Rule-based filtering using relevant keywords
3. **LLM Labeler** (`llm_labeler.py`): GPT-based verification and classification
4. **Prompt Generator** (`prompts.py`): Manages prompts for LLM interactions
5. **Agent** (`agent.py`): Main orchestrator that coordinates all components

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Rumor_detection_agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key (choose one method):

**Method 1: Environment file (recommended)**
```bash
# Copy the example file
cp .env.example .env
# Edit .env and add your API key
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

**Method 2: Environment variable**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

**Method 3: Pass directly in code**
```python
agent = Agent(openai_api_key='your-api-key-here')
```

## Usage

### Basic Usage

```python
from agent import Agent

# Initialize the agent
agent = Agent(roberta_model_path=None)  # Set path if you have a trained model

# Classify a single post
post = "The voter rolls are dirty and haven't been cleaned in years!"
is_rumor, rumor_type = agent.classify_post(post)

if is_rumor:
    print(f"Rumor detected! Type: {rumor_type}")
    print(f"Description: {agent.get_rumor_info(rumor_type)}")
else:
    print("Not a rumor")
```

### Batch Processing

```python
posts = [
    "Trump is the best candidate!",
    "Dead people are voting in this election",
    "The mail-in ballot system is fraudulent"
]

results = agent.classify_batch(posts)
for post, (is_rumor, rumor_type) in zip(posts, results):
    print(f"Post: {post}")
    print(f"Rumor: {is_rumor}, Type: {rumor_type}")
```

### Running the Example

```bash
python example_usage.py
```

## Rumor Categories

The system identifies 16 types of election-related rumors:

1. **Dirty Voter Rolls**: Claims about uncleaned voter registration lists
2. **Ballot Mail-In Fraud**: Allegations about mail-in ballot security
3. **Drop Box Tampering**: Claims about ballot drop box security
4. **Software Security**: Allegations about voting system vulnerabilities
5. **Dead Voters**: Claims about deceased people voting
6. **Voter Registration Data Breach**: Allegations about database hacks
7. **Voter Registration Website Outage**: Claims about system compromises
8. **Hacking into Jurisdictions**: Allegations about IT system breaches
9. **Voter Registration Manipulation**: Claims about data tampering
10. **Extra Mail-in Ballots**: Allegations about fraudulent ballot printing
11. **Ballot FWAB Fraud**: Claims about Federal Write-In ballot abuse
12. **Ballot Scanner Issues**: Allegations about scanner problems
13. **Ballot Writing Instrument Issue**: Claims about pen/marker problems
14. **Voter Intimidation Tactics**: Allegations about polling place interference
15. **Nonexistent Vote Disclosure**: Claims about vote privacy breaches
16. **Polling Lookup Outage**: Claims about lookup system compromises

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

## Pipeline Logic

1. **RoBERTa Screening**: Initial classification using fine-tuned model
2. **Keyword Filtering**: Fallback for posts not caught by RoBERTa
3. **LLM Initial Screening**: Broad rumor detection using GPT
4. **LLM Verification**: Strict classification into specific rumor types

Posts must pass through multiple stages to be classified as rumors, ensuring high precision.

## Error Handling

The system is designed to be robust:
- If RoBERTa model is unavailable, it falls back to keyword filtering
- If OpenAI API fails, errors are logged and processing continues
- Invalid rumor types are filtered out during verification

## Development

### Adding New Rumor Types

1. Update `RUMORS` dictionary in `rumors_constants.py`
2. Add relevant keywords to `keyword_filter.py`
3. Update prompts in `prompts.py` if needed


TODO: ADD a specific user's scraped posts for an example
TODO: ADD the exact rumor and also the rumor category
TODO: Add example usage script (bash)