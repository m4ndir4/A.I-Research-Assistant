from typing import List, Dict, Any
import json
from openai import OpenAI

class LiteratureReviewAgent:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """Initialize the Literature Review Agent with OpenAI API key"""
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def generate_literature_review(self, sources: List[Dict[str, Any]], style: str = "thematic"):
        """Generate a literature review based on the provided sources"""
        try:
            prompt = (
                "You are a Literature Review Agent.\n"
                f"Create a comprehensive literature review in {style} style based on the following sources:\n\n"
                f"{str(sources)}\n\n"
                "Your literature review should:\n"
                "1. Provide a comprehensive overview of the research field\n"
                "2. Synthesize findings from multiple sources\n"
                "3. Identify patterns, trends, and contradictions in the literature\n"
                "4. Be well-structured with clear sections and transitions\n"
                "5. Include proper citations to sources\n\n"
                "Format the review in markdown with appropriate headings, bullet points, and emphasis."
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                "success": True,
                "literature_review": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_paper_summary_table(self, papers: List[Dict[str, Any]]):
        """Create a formatted summary table for research papers"""
        try:
            prompt = (
                "You are a Research Summary Agent.\n"
                "Create a well-formatted markdown table summarizing the following research papers:\n\n"
                f"{str(papers)}\n\n"
                "The table should include columns for:\n"
                "1. Title\n"
                "2. Authors\n"
                "3. Publication\n"
                "4. Brief summary (2-3 sentences)\n"
                "5. Key contribution\n\n"
                "Make the table readable and well-formatted in markdown."
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                "success": True,
                "summary_table": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 