from openai import OpenAI
import os
from typing import List, Dict, Any, Optional

class DraftingAgent:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def draft_answer(self, question, analysis):
        """Draft a comprehensive answer"""
        try:
            prompt = (
                "You are a Drafting Agent that creates comprehensive answers based on research.\n\n"
                f"Original question:\n{question}\n\n"
                f"Organized research information:\n{analysis}\n\n"
                "Create a well-structured, informative answer that addresses the question comprehensively. "
                "Include proper citations to sources wherever applicable."
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                "success": True,
                "answer": response.choices[0].message.content
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
    
    def generate_references_list(self, sources: List[Dict[str, Any]], citation_style: str = "APA"):
        """Generate a formatted references list from sources"""
        try:
            # Create a more detailed prompt with specific formatting instructions
            prompt = (
                "You are a Citation Agent specializing in academic citation formatting.\n"
                f"Create a references list in {citation_style} style for the following sources:\n\n"
                f"{str(sources)}\n\n"
                f"Follow these specific {citation_style} style guidelines:\n"
            )
            
            # Add style-specific instructions
            if citation_style.upper() == "APA":
                prompt += (
                    "APA Style:\n"
                    "- Author, A. A., Author, B. B., & Author, C. C. (Year). Title of article. Title of Journal, Volume(Issue), pp-pp.\n"
                    "- For books: Author, A. A. (Year). Title of book. Publisher.\n"
                    "- For websites: Author, A. A. (Year, Month Day). Title of webpage. Website Name. URL\n"
                    "- For PDFs: Author, A. A. (Year). Title of document. Source. URL\n"
                )
            elif citation_style.upper() == "MLA":
                prompt += (
                    "MLA Style:\n"
                    "- Author, First Name, and Second Author. \"Title of Article.\" Title of Journal, vol. Volume, no. Issue, Year, pp. pp-pp.\n"
                    "- For books: Author, First Name. Title of Book. Publisher, Year.\n"
                    "- For websites: Author, First Name. \"Title of Webpage.\" Website Name, Publisher, Date, URL\n"
                    "- For PDFs: Author, First Name. \"Title of Document.\" Source, Year, URL\n"
                )
            elif citation_style.upper() == "CHICAGO":
                prompt += (
                    "Chicago Style:\n"
                    "- Author, First Name, and Second Author. \"Title of Article.\" Title of Journal Volume, no. Issue (Year): pp-pp.\n"
                    "- For books: Author, First Name. Title of Book. Place of Publication: Publisher, Year.\n"
                    "- For websites: Author, First Name. \"Title of Webpage.\" Website Name. Month Day, Year. URL\n"
                    "- For PDFs: Author, First Name. \"Title of Document.\" Source, Year. URL\n"
                )
            elif citation_style.upper() == "HARVARD":
                prompt += (
                    "Harvard Style:\n"
                    "- Author, A.A. and Author, B.B. (Year) 'Title of article', Title of Journal, Volume(Issue), pp. pp-pp.\n"
                    "- For books: Author, A.A. (Year) Title of Book, Place of Publication: Publisher.\n"
                    "- For websites: Author, A.A. (Year) 'Title of webpage', Website Name, [online] Available at: URL [Accessed Day Month Year]\n"
                    "- For PDFs: Author, A.A. (Year) 'Title of document', Source, [online] Available at: URL [Accessed Day Month Year]\n"
                )
            elif citation_style.upper() == "IEEE":
                prompt += (
                    "IEEE Style:\n"
                    "- A. Author, B. Author, and C. Author, \"Title of article,\" Title of Journal, vol. Volume, no. Issue, pp. pp-pp, Year.\n"
                    "- A. Author, Title of Book, ed. Edition. Place of Publication: Publisher, Year.\n"
                    "- A. Author, \"Title of webpage,\" Website Name, Year. [Online]. Available: URL\n"
                    "- A. Author, \"Title of document,\" Source, Year. [Online]. Available: URL\n"
                )
            else:
                prompt += (
                    f"Format the references according to standard {citation_style} style guidelines.\n"
                )
            
            prompt += (
                "\nOrder the references alphabetically by author surname.\n"
                "Ensure each reference is properly formatted with all required elements.\n"
                "For PDFs, include the source and URL if available.\n"
                "For websites, include the access date if available.\n"
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                "success": True,
                "references_list": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def draft_literature_review_section(self, topic: str, related_papers: List[Dict[str, Any]]):
        """Draft a section of a literature review focused on a specific topic"""
        try:
            prompt = (
                "You are a Literature Review Drafting Agent.\n"
                f"Create a well-structured literature review section on the topic: {topic}\n\n"
                f"Based on these papers:\n{str(related_papers)}\n\n"
                "Your literature review section should:\n"
                "1. Synthesize findings related to this specific topic\n"
                "2. Compare and contrast different approaches\n"
                "3. Highlight consensus and disagreements in the research\n"
                "4. Include proper in-text citations\n"
                "5. Be written in an academic style with clear organization"
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                "success": True,
                "section_draft": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }