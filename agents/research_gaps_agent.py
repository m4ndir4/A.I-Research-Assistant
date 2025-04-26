from typing import Dict, Any
from openai import OpenAI

class ResearchGapsAgent:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """Initialize the Research Gaps Agent with OpenAI API key"""
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def identify_research_gaps(self, literature_review: str):
        """Identify research gaps based on the literature review."""
        try:
            if not literature_review:
                return {
                    "success": False,
                    "error": "No literature review provided for gap analysis."
                }
            
            prompt = (
                "You are a Research Gaps Analysis Agent.\n"
                "Based on the following literature review, identify and analyze research gaps:\n\n"
                f"{literature_review}\n\n"
                "Your analysis should:\n"
                "1. Identify areas where research is lacking or insufficient\n"
                "2. Highlight methodological limitations in existing studies\n"
                "3. Suggest promising directions for future research\n"
                "4. Prioritize gaps by importance and feasibility\n"
                "5. Consider interdisciplinary connections and opportunities\n\n"
                "Format your response with clear sections and bullet points for each gap."
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                "success": True,
                "research_gaps": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 