from prompts import PromptGenerator
from openai import OpenAI
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class LlmLabeler:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.0, api_key: Optional[str] = None):
        # Priority: 1. Passed api_key, 2. Environment variable, 3. Error
        if api_key:
            self.client = OpenAI(api_key=api_key)
        elif os.getenv('OPENAI_API_KEY'):
            self.client = OpenAI()  # Uses OPENAI_API_KEY environment variable
        else:
            raise ValueError(
                "OpenAI API key not found. Please either:\n"
                "1. Set OPENAI_API_KEY environment variable\n"
                "2. Create a .env file with OPENAI_API_KEY=your-key\n" 
                "3. Pass api_key parameter to LlmLabeler(api_key='your-key')"
            )
        self.model = model
        self.temperature = temperature
        self.prompt_generator = PromptGenerator()

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=self.temperature,
                n=1,
                stop=None,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return ""

    def initial_label(self, post: str) -> bool:
        """Initial screening for rumors"""
        prompt = self.prompt_generator.get_initial_screening_prompt(post)
        response = self._call_openai(prompt)
        
        if not response or not response.strip():
            return False
        return True

    def verification_label_rumor_type(self, post: str) -> Optional[int]:
        """Final verification and rumor type classification"""
        prompt = self.prompt_generator.get_verification_prompt(post)
        response = self._call_openai(prompt)
        
        response = response.replace("'", "").replace('"', '').strip()
        
        if response and response.isnumeric():
            rumor_type = int(response)
            if 1 <= rumor_type <= 16:
                return rumor_type
        
        return None

