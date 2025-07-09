from rumor_constants import *
from rumor_constants import *
from keyword_filter import KeywordFilter
from finetuned_roberta import RobertaModel
from llm_labeler import LlmLabeler
from typing import Tuple, Optional, List, Dict
import csv
import os
import csv
import os


class Agent:
    def __init__(self, roberta_model_path: str = None, openai_api_key: Optional[str] = None):
        self.keyword_filter = KeywordFilter()
        self.roberta = RobertaModel(directory=roberta_model_path)
        self.llm = LlmLabeler(api_key=openai_api_key)
        self.false_positives = 0

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
            self.false_positives += 1
            return False, None

        return True, rumor_label_pred
    
    def classify_batch(self, posts: List[str]) -> List[Tuple[bool, Optional[int]]]:
        # classify a batch of posts
        results = []
        for post in posts:
            result = self.classify(post)
            results.append(result)
        return results
    
    def get_rumor_info(self, rumor_type: int) -> Optional[str]:
        """Get the description of a rumor type"""
        return RUMORS.get(rumor_type)
    
    def get_rumor_category(self, rumor_type: int) -> Optional[str]:
        return RUMOR_INT_TO_CLASS.get(rumor_type)
    
    def classify_csv(self, csv_path: str = None, verbose: bool = False, max_posts: int = 2000) -> Dict:
        """
        Process a CSV file of posts and classify each one
        verbose: If true, print details for each post. If false, only print summary.
        max_posts: Maximum number of posts to process (default: 2000)
        note: results is returned with the text in lowercase form - TODO: potentially improve returning format
        """
        # default to the random posts CSV
        if csv_path is None:
            csv_path = os.path.join("example_posts", "random_posts.csv")
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        posts = []
        results = []
        
        print(f"Reading posts from: {csv_path}")
        with open(csv_path, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0].strip():
                    post_text = row[0].strip()
                    posts.append(post_text)
        
        # limit to max_posts
        if len(posts) > max_posts:
            posts = posts[:max_posts]
            print(f"Limited to first {max_posts} posts")
        else:
            total_posts = len(posts)
            print(f"Total posts to classify: {total_posts}")
        print("=" * 30)

        misinformation_count = 0
        category_counts = {}
        self.false_positives = 0
        
        for i, post in enumerate(posts, 1):
            is_rumor, rumor_type = self.classify(post)
            results.append((post, is_rumor, rumor_type))
            
            if is_rumor and rumor_type:
                misinformation_count += 1
                category = self.get_rumor_category(rumor_type)
                if category:
                    category_counts[category] = category_counts.get(category, 0) + 1
                
                if verbose:
                    rumor_description = self.get_rumor_info(rumor_type)
                    print(f"\n\n ------ MISINFORMATION DETECTED (Post {i})")
                    print(f"   Type: {rumor_type} - {category}")
                    print(f"   Description: {rumor_description}")
                    print(f"   Post: {post[:100]}{'...' if len(post) > 100 else ''}")
                    print("-" * 30)
            if i % 100 == 0:
                print(f"Processed {i}/{total_posts} posts...")
        
        print("\n" + "-" * 30)
        print("SUMMARY")
        print("-" * 30)
        print(f"Total posts processed: {total_posts}")
        print(f"Misinformation detected: {misinformation_count}")
        print(f"Clean posts: {total_posts - misinformation_count}")
        print(f"False positives: {self.false_positives}")
        print(f"Misinformation rate: {(misinformation_count/total_posts*100):.2f}%")
        
        if category_counts:
            print("\nMisinformation by category:")
            for category, count in sorted(category_counts.items()):
                print(f"{category}: {count}")
        
        return {
            'total_posts': total_posts,
            'misinformation_count': misinformation_count,
            'clean_posts': total_posts - misinformation_count,
            'false_positives': self.false_positives,
            'misinformation_rate': misinformation_count/total_posts if total_posts > 0 else 0,
            'category_counts': category_counts,
            'results': results
        }