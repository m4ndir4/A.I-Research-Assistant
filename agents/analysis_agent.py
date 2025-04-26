from openai import OpenAI
import os
from typing import List, Dict, Any, Optional
import json
import re
from datetime import datetime

class AnalysisAgent:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def analyze(self, search_results):
        """Analyze and organize search results"""
        try:
            prompt = (
                "You are an Analysis Agent that organizes research information.\n"
                "Analyze the following search results and organize them into "
                "coherent themes and key points.\n\n"
                f"Search results:\n{search_results}\n\n"
                "Provide a structured analysis that can be used for drafting a comprehensive answer."
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                "success": True,
                "analysis": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def analyze_paper(self, paper_text: str, paper_name: str):
        """Extract key information from a research paper."""
        try:
            prompt = (
                "You are a Research Paper Analysis Agent.\n"
                "Analyze the following research paper and extract these key elements:\n"
                "1. Title\n"
                "2. Authors\n"
                "3. Publication year and journal/conference\n"
                "4. Abstract summary (100 words)\n"
                "5. Key findings (bullet points)\n"
                "6. Methodology\n"
                "7. Main topics/themes\n\n"
                f"Paper name: {paper_name}\n"
                f"Paper content: {paper_text[:4000]}...\n\n"
                "Format your response as a JSON object."
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.choices[0].message.content
            
            # Extract JSON from response
            try:
                # Find JSON in response
                json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    json_str = content
                    
                result = json.loads(json_str)
                return {
                    "success": True,
                    "paper_analysis": result
                }
            except:
                # Fallback if JSON parsing fails
                return {
                    "success": True,
                    "paper_analysis": {
                        "title": paper_name,
                        "authors": "Extraction failed",
                        "publication": "Unknown",
                        "abstract": "Could not parse paper content properly.",
                        "key_findings": ["Extraction failed"],
                        "methodology": "Extraction failed",
                        "topics": ["Unknown"]
                    }
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    def format_citation(self, source: Dict[str, Any], style: str = "APA"):
        """Format a citation based on the chosen style."""
        try:
            prompt = (
                f"Format the following source information into a {style} citation:\n"
                f"{json.dumps(source)}"
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                "success": True,
                "citation": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_literature_review(self, papers: List[Dict[str, Any]], style: str = "thematic"):
        """Generate a literature review based on the uploaded papers and search results."""
        try:
            if not papers:
                return {
                    "success": False,
                    "error": "No papers provided for review."
                }
            
            # Prepare the content for the literature review
            paper_data = []
            for paper in papers:
                paper_data.append(
                    f"Title: {paper.get('title', '')}\n"
                    f"Authors: {paper.get('authors', '')}\n"
                    f"Publication: {paper.get('publication', '')}\n"
                    f"Abstract: {paper.get('abstract', '')}\n"
                    f"Key findings: {', '.join(paper.get('key_findings', []))}"
                )
            
            prompt = (
                "You are a Literature Review Agent.\n"
                f"Generate a comprehensive literature review based on the following research papers.\n"
                f"Organization style: {style} (thematic means organized by topics/themes, "
                "chronological means by publication date)\n\n"
                f"Papers:\n{json.dumps(paper_data)}\n\n"
                "Your literature review should:\n"
                "1. Identify major themes and patterns across the literature\n"
                "2. Discuss methodological approaches used\n"
                "3. Highlight key findings and their significance\n"
                "4. Note any contradictions or debates in the field\n"
                "5. Be well-structured with clear sections\n\n"
                "Format your response with markdown headings and proper citations."
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
    
    def identify_research_gaps(self, literature_review: str):
        """Identify research gaps based on the literature review."""
        try:
            prompt = (
                "You are a Research Gap Analysis Agent.\n"
                "Based on the following literature review, identify key research gaps in the field:\n\n"
                f"{literature_review[:4000]}...\n\n"
                "Your response should:\n"
                "1. Identify specific areas where research is lacking\n"
                "2. Explain why these gaps are significant\n"
                "3. Suggest potential research questions to address these gaps\n"
                "4. Note any methodological limitations in existing studies\n\n"
                "Format your response in markdown with clear sections."
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