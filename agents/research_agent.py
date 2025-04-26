from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from dotenv import load_dotenv
import os
import PyPDF2
import tempfile
from datetime import datetime
from typing import List, Dict, Any, Optional
import json

# Load environment variables
load_dotenv()

class ResearchAgent:
    def __init__(self):
        # Debug: Print Tavily API key status
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        print(f"ResearchAgent: Tavily API key {'is set' if tavily_api_key else 'is not set'}")
        
        # Initialize the Tavily search tool
        self.search_tool = TavilySearchResults(
            tavily_api_key=tavily_api_key,
            max_results=5,
            search_depth="advanced"  # Use advanced search for better results
        )
        
        # Initialize sources storage
        self.sources = []
        
        # Academic domains to prioritize
        self.academic_domains = [
            "scholar.google.com", "researchgate.net", "sciencedirect.com", 
            "jstor.org", "springer.com", "wiley.com", "ieee.org", 
            "academia.edu", "arxiv.org", "doi.org", "ncbi.nlm.nih.gov",
            "pubmed.ncbi.nlm.nih.gov", "plos.org", "nature.com", 
            "science.org", "cell.com", "thelancet.com", "nejm.org",
            "bmj.com", "tandfonline.com", "sagepub.com", "cambridge.org",
            "oxfordjournals.org", "pnas.org", "royalsocietypublishing.org",
            "frontiersin.org", "mdpi.com", "hindawi.com", "scirp.org",
            "scirp.org", "scirp.org", "scirp.org", "scirp.org", "scirp.org"
        ]
    
    def research(self, query, paper_only=False):
        """Perform web research on a given query, optionally focusing only on research papers"""
        print(f"ResearchAgent: Starting research for query: {query}")
        try:
            # Modify query to focus on research papers if requested
            if paper_only:
                query = f"{query} research paper academic journal"
            
            # Use the search tool with academic domains
            search_results = self.search_tool.invoke(
                query,
                include_domains=self.academic_domains if paper_only else None
            )
            
            print(f"ResearchAgent: Search successful, found {len(search_results)} results")
            
            # Process and store sources
            for result in search_results:
                source = {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "score": result.get("score", 0),
                    "date_accessed": datetime.now().strftime("%Y-%m-%d")
                }
                self._add_source(source)
                
            return {
                "success": True,
                "results": search_results,
                "query": query
            }
        except Exception as e:
            print(f"ResearchAgent: Search failed with error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }
    
    
    
    def get_sources(self):
        """Get all collected sources"""
        return self.sources
    
    
    def clear_sources(self):
        """Clear all sources"""
        self.sources = []
        return True
    
    def remove_source(self, index):
        """Remove a specific source by index"""
        if 0 <= index < len(self.sources):
            self.sources.pop(index)
            return True
        return False
    
    def _add_source(self, source):
        """Add a source if not already present"""
        # Check if source is already in the list by URL
        for existing_source in self.sources:
            if existing_source.get("url") == source.get("url"):
                return False
        
        self.sources.append(source)
        return True
    

    def search_by_topics(self, topics):
        """Perform targeted research on specific topics"""
        print(f"ResearchAgent: Researching specific topics: {topics}")
        results = {}
        
        for topic in topics:
            query = f"{topic} research paper recent findings"
            topic_results = self.research(query, paper_only=True)
            results[topic] = topic_results
            
        return {
            "success": True,
            "topic_results": results
        }