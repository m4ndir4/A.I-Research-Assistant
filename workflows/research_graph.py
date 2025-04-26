from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime

# Define state structure with additional fields for research capabilities
class ResearchState(TypedDict):
    question: str
    search_results: List[Dict[str, Any]]
    analysis: str
    answer: str
    needs_more_research: bool
    status: str
    # New fields for research paper functionality
    sources: List[Dict[str, Any]]
    citation_style: str
    literature_review: str
    research_gaps: str
    paper_summary_table: str
    references_list: str

# Store agents globally for the workflow functions to access
research_agent = None
analysis_agent = None
drafting_agent = None
literature_review_agent = None
research_gaps_agent = None

def run_research(state):
    """Use the research agent to gather information from the web"""
    try:
        # Get the question from the state
        question = state["question"]
        
        # Check if we should focus only on research papers
        paper_only = state.get("paper_only", False)
        
        # Use the research agent to search for information
        search_response = research_agent.research(question, paper_only=paper_only)
        
        if search_response["success"]:
            # Store the search results in the state
            state["search_results"] = search_response["results"]
            state["status"] = "research_complete"
            
            # Update sources from research agent if available
            if hasattr(research_agent, "get_sources"):
                state["sources"] = research_agent.get_sources()
        else:
            # Handle error
            state["status"] = "research_failed"
            state["error"] = search_response.get("error", "Unknown error during research")
            
    except Exception as e:
        # Handle any unexpected errors
        state["status"] = "research_error"
        state["error"] = str(e)
    
    return state

def run_analysis(state):
    """Use the analysis agent to organize and synthesize the research information"""
    try:
        # Get the search results from the state
        search_results = state["search_results"]
        
        # Skip analysis if research failed
        if state["status"] in ["research_failed", "research_error"]:
            state["status"] = "analysis_skipped"
            return state
        
        # Use the analysis agent to analyze the search results
        analysis_response = analysis_agent.analyze(search_results)
        
        if analysis_response["success"]:
            # Store the analysis in the state
            state["analysis"] = analysis_response["analysis"]
            state["status"] = "analysis_complete"
        else:
            # Handle error
            state["status"] = "analysis_failed"
            state["error"] = analysis_response.get("error", "Unknown error during analysis")
            
    except Exception as e:
        # Handle any unexpected errors
        state["status"] = "analysis_error"
        state["error"] = str(e)
    
    return state

def run_drafting(state):
    """Use the drafting agent to create a comprehensive answer"""
    try:
        # Get the question and analysis from the state
        question = state["question"]
        analysis = state["analysis"]
        
        # Skip drafting if previous steps failed
        if state["status"] in ["research_failed", "research_error", "analysis_failed", "analysis_error"]:
            state["status"] = "drafting_skipped"
            state["answer"] = "Unable to generate answer due to errors in previous steps."
            return state
        
        # Use the drafting agent to create an answer
        drafting_response = drafting_agent.draft_answer(question, analysis)
        
        if drafting_response["success"]:
            # Store the answer in the state
            state["answer"] = drafting_response["answer"]
            state["status"] = "drafting_complete"
            
            # Check if more research is needed (this could be determined by the drafting agent)
            state["needs_more_research"] = False  # For now, assume no more research is needed
        else:
            # Handle error
            state["status"] = "drafting_failed"
            state["error"] = drafting_response.get("error", "Unknown error during drafting")
            
    except Exception as e:
        # Handle any unexpected errors
        state["status"] = "drafting_error"
        state["error"] = str(e)
    
    return state

# New functions for research paper functionality


def generate_paper_summary_table(state):
    """Generate a summary table of all research papers"""
    try:
        if not state.get("sources"):
            state["status"] = "no_papers_available"
            state["paper_summary_table"] = "No papers available for summary."
            return state
            
        # Use the literature review agent to create a summary table
        summary_response = literature_review_agent.create_paper_summary_table(state["sources"])
        
        if summary_response["success"]:
            state["paper_summary_table"] = summary_response["summary_table"]
            state["status"] = "summary_table_generated"
        else:
            state["status"] = "summary_table_failed"
            state["error"] = summary_response.get("error", "Unknown error generating summary table")
            
    except Exception as e:
        state["status"] = "summary_table_error"
        state["error"] = str(e)
        
    return state

def generate_literature_review(state, style="thematic"):
    """Generate a literature review based on sources"""
    try:
        if not state.get("sources"):
            state["status"] = "no_sources_available"
            state["literature_review"] = "No sources available for literature review."
            return state
            
        # Use the literature review agent to generate a literature review
        review_response = literature_review_agent.generate_literature_review(state["sources"], style)
        
        if review_response["success"]:
            state["literature_review"] = review_response["literature_review"]
            state["status"] = "literature_review_generated"
        else:
            state["status"] = "literature_review_failed"
            state["error"] = review_response.get("error", "Unknown error generating literature review")
            
    except Exception as e:
        state["status"] = "literature_review_error"
        state["error"] = str(e)
        
    return state

def identify_research_gaps(state):
    """Identify research gaps based on the literature review"""
    try:
        if not state.get("literature_review"):
            state["status"] = "no_literature_review"
            state["research_gaps"] = "No literature review available for gap analysis."
            return state
            
        # Use the research gaps agent to identify research gaps
        gaps_response = research_gaps_agent.identify_research_gaps(state["literature_review"])
        
        if gaps_response["success"]:
            state["research_gaps"] = gaps_response["research_gaps"]
            state["status"] = "research_gaps_identified"
        else:
            state["status"] = "research_gaps_failed"
            state["error"] = gaps_response.get("error", "Unknown error identifying research gaps")
            
    except Exception as e:
        state["status"] = "research_gaps_error"
        state["error"] = str(e)
        
    return state

def generate_references_list(state):
    """Generate a formatted references list from all sources"""
    try:
        if not state.get("sources"):
            state["status"] = "no_sources_available"
            state["references_list"] = "No sources available for references list."
            return state
            
        # Get the citation style from state or use default
        citation_style = state.get("citation_style", "APA")
        
        # Use the drafting agent to generate references list
        refs_response = drafting_agent.generate_references_list(state["sources"], citation_style)
        
        if refs_response["success"]:
            state["references_list"] = refs_response["references_list"]
            state["status"] = "references_list_generated"
        else:
            state["status"] = "references_list_failed"
            state["error"] = refs_response.get("error", "Unknown error generating references list")
            
    except Exception as e:
        state["status"] = "references_list_error"
        state["error"] = str(e)
        
    return state

def update_citation_style(state, style):
    """Update the citation style used for references"""
    try:
        state["citation_style"] = style
        
        # If we already have sources, regenerate the references list
        if state.get("sources"):
            state = generate_references_list(state)
            
        return state
    except Exception as e:
        state["status"] = "citation_style_error"
        state["error"] = str(e)
        return state

def needs_more_research(state):
    """Condition to check if more research is needed"""
    return state["needs_more_research"]

def create_research_workflow(research_agent_instance=None, analysis_agent_instance=None, drafting_agent_instance=None, literature_review_agent_instance=None, research_gaps_agent_instance=None):
    """Create a research workflow that uses the provided agents"""
    # Set the global agent references
    global research_agent, analysis_agent, drafting_agent, literature_review_agent, research_gaps_agent
    research_agent = research_agent_instance
    analysis_agent = analysis_agent_instance
    drafting_agent = drafting_agent_instance
    literature_review_agent = literature_review_agent_instance
    research_gaps_agent = research_gaps_agent_instance
    
    def execute_workflow(initial_state):
        """Execute the research workflow with the given initial state"""
        state = initial_state.copy()
        
        # Initialize new state fields if they don't exist
        
        if "sources" not in state:
            state["sources"] = []
        if "citation_style" not in state:
            state["citation_style"] = "APA"
        if "literature_review" not in state:
            state["literature_review"] = ""
        if "research_gaps" not in state:
            state["research_gaps"] = ""
        if "paper_summary_table" not in state:
            state["paper_summary_table"] = ""
        if "references_list" not in state:
            state["references_list"] = ""
        
        # Run the research step
        state = run_research(state)
        
        # Run the analysis step
        state = run_analysis(state)
        
        # Run the drafting step
        state = run_drafting(state)
        
        # Handle the case where more research is needed
        iteration = 0
        max_iterations = 3  # Limit the number of iterations to prevent infinite loops
        
        while state["needs_more_research"] and iteration < max_iterations:
            # Add iteration information to the state
            state["iteration"] = iteration + 1
            
            # Run another round of research, analysis, and drafting
            state = run_research(state)
            state = run_analysis(state)
            state = run_drafting(state)
            
            iteration += 1
        
        # Add completion information
        if iteration >= max_iterations and state["needs_more_research"]:
            state["status"] = "max_iterations_reached"
        else:
            state["status"] = "workflow_complete"
            
        return state
    
    # Return a dictionary containing all workflow functions for access
    return {
        "execute_workflow": execute_workflow,
        "generate_paper_summary_table": generate_paper_summary_table,
        "generate_literature_review": generate_literature_review,
        "identify_research_gaps": identify_research_gaps,
        "generate_references_list": generate_references_list,
        "update_citation_style": update_citation_style
    }