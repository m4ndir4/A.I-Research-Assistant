import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.drafting_agent import DraftingAgent
from agents.literature_review_agent import LiteratureReviewAgent
from agents.research_gaps_agent import ResearchGapsAgent
from workflows.research_graph import create_research_workflow

# Load environment variables
load_dotenv()

# Check API keys
if not os.getenv("OPENAI_API_KEY"):
    st.error("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
    st.stop()

if not os.getenv("TAVILY_API_KEY"):
    st.error("Tavily API key not found. Please set TAVILY_API_KEY in your .env file.")
    st.stop()

# Initialize session state
if 'sources' not in st.session_state:
    st.session_state.sources = []
if 'citation_style' not in st.session_state:
    st.session_state.citation_style = "APA"
if 'literature_review' not in st.session_state:
    st.session_state.literature_review = ""
if 'research_gaps' not in st.session_state:
    st.session_state.research_gaps = ""
if 'references_list' not in st.session_state:
    st.session_state.references_list = ""
if 'search_completed' not in st.session_state:
    st.session_state.search_completed = False
if 'paper_summary_table' not in st.session_state:
    st.session_state.paper_summary_table = ""

# Initialize agents
research_agent = ResearchAgent()
analysis_agent = AnalysisAgent(api_key=os.getenv('OPENAI_API_KEY'))
drafting_agent = DraftingAgent(api_key=os.getenv('OPENAI_API_KEY'))
literature_review_agent = LiteratureReviewAgent(api_key=os.getenv('OPENAI_API_KEY'))
research_gaps_agent = ResearchGapsAgent(api_key=os.getenv('OPENAI_API_KEY'))

# Create workflow
research_workflow = create_research_workflow(
    research_agent_instance=research_agent,
    analysis_agent_instance=analysis_agent,
    drafting_agent_instance=drafting_agent,
    literature_review_agent_instance=literature_review_agent,
    research_gaps_agent_instance=research_gaps_agent
)

# Set page config
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar for source management
with st.sidebar:
    st.title("Source Management")
    
    # Display sources
    st.subheader("Sources")
    if st.session_state.sources:
        for i, source in enumerate(st.session_state.sources):
            st.write(f"{i+1}. {source.get('title', 'Untitled')}")
    else:
        st.info("No sources added yet.")
    
    # Display references list in sidebar
    if st.session_state.references_list:
        st.subheader("References")
        st.markdown(st.session_state.references_list)
    elif st.session_state.sources:
        st.info("References will appear here after selecting a citation style.")

# Main content
st.title("AI Research Assistant")

# Create tabs for different functionalities
tab1, tab2, tab3, tab4 = st.tabs([
    "Research Papers", 
    "Literature Review", 
    "Research Gaps",
    "References"
])

# Research Papers Tab
with tab1:
    st.header("Research Papers")
    
    # Search input
    search_query = st.text_area("Enter your research question:", height=100)
    
    if st.button("Search Research Papers"):
        if search_query:
            with st.spinner("Searching for research papers..."):
                # Initialize state for research
                initial_state = {
                    "question": search_query,
                    "search_results": [],
                    "analysis": "",
                    "answer": "",
                    "needs_more_research": False,
                    "status": "started",
                    "paper_only": True  # Flag to indicate we only want research papers
                }
                
                # Execute research workflow
                result = research_workflow["execute_workflow"](initial_state)
                
                # Update sources - append new sources instead of replacing
                if "sources" in result:
                    # Add new sources to existing ones
                    new_sources = result["sources"]
                    existing_titles = [s.get('title') for s in st.session_state.sources]
                    
                    # Only add sources that don't already exist
                    for source in new_sources:
                        if source.get('title') not in existing_titles:
                            st.session_state.sources.append(source)
                    
                    # Automatically generate references list when sources are updated
                    if st.session_state.sources:
                        st.session_state.references_list = research_workflow["generate_references_list"]({
                            "sources": st.session_state.sources,
                            "citation_style": st.session_state.citation_style
                        })["references_list"]
                
                # Display results
                st.subheader("Research Results")
                st.write(result["answer"])
                
                # Display search results
                with st.expander("View Research Papers"):
                    for i, result in enumerate(result.get("search_results", [])):
                        st.write(f"**Paper {i+1}:**")
                        st.write(f"**Title:** {result.get('title', 'No title')}")
                        st.write(f"**URL:** {result.get('url', 'No URL')}")
                        st.write(f"**Content:** {result.get('content', 'No content')}")
                        st.write("---")
                
                # Automatically generate literature review
                with st.spinner("Generating literature review..."):
                    review_result = literature_review_agent.generate_literature_review(
                        st.session_state.sources, 
                        style="thematic"
                    )
                    
                    if review_result["success"]:
                        st.session_state.literature_review = review_result["literature_review"]
                    else:
                        st.warning(f"Failed to generate literature review: {review_result.get('error', 'Unknown error')}")
                
                # Automatically identify research gaps
                with st.spinner("Identifying research gaps..."):
                    gaps_result = research_gaps_agent.identify_research_gaps(
                        st.session_state.literature_review
                    )
                    
                    if gaps_result["success"]:
                        st.session_state.research_gaps = gaps_result["research_gaps"]
                    else:
                        st.warning(f"Failed to identify research gaps: {gaps_result.get('error', 'Unknown error')}")
                
                # Generate paper summary table
                with st.spinner("Generating paper summary table..."):
                    summary_result = literature_review_agent.create_paper_summary_table(
                        st.session_state.sources
                    )
                    
                    if summary_result["success"]:
                        st.session_state.paper_summary_table = summary_result["summary_table"]
                    else:
                        st.warning(f"Failed to generate paper summary table: {summary_result.get('error', 'Unknown error')}")
                
                # Set search completed flag
                st.session_state.search_completed = True
                
                # Show success message
                st.success("Research completed! Literature review and research gaps have been automatically generated.")
        else:
            st.warning("Please enter a research question.")

# Literature Review Tab
with tab2:
    st.header("Literature Review")
    
    if st.button("Generate Literature Review"):
        if st.session_state.sources:
            with st.spinner("Generating literature review..."):
                # Generate literature review using the literature review agent
                review_result = literature_review_agent.generate_literature_review(
                    st.session_state.sources, 
                    style="thematic"  # Always use thematic style
                )
                
                if review_result["success"]:
                    st.session_state.literature_review = review_result["literature_review"]
                    
                    # Generate paper summary table
                    summary_result = literature_review_agent.create_paper_summary_table(
                        st.session_state.sources
                    )
                    
                    if summary_result["success"]:
                        st.session_state.paper_summary_table = summary_result["summary_table"]
                    else:
                        st.warning(f"Failed to generate paper summary table: {summary_result.get('error', 'Unknown error')}")
                else:
                    st.warning(f"Failed to generate literature review: {review_result.get('error', 'Unknown error')}")
        else:
            st.warning("No sources available for literature review.")
    
    # Display literature review as a table
    if st.session_state.paper_summary_table:
        st.markdown(st.session_state.paper_summary_table)
    elif st.session_state.search_completed:
        st.info("No literature review generated yet. Please try searching for research papers first.")

# Research Gaps Tab
with tab3:
    st.header("Research Gaps")
    
    if st.button("Regenerate Research Gaps"):
        if st.session_state.literature_review:
            with st.spinner("Identifying research gaps..."):
                gaps_result = research_gaps_agent.identify_research_gaps(
                    st.session_state.literature_review
                )
                
                if gaps_result["success"]:
                    st.session_state.research_gaps = gaps_result["research_gaps"]
                    st.write(st.session_state.research_gaps)
                else:
                    st.warning(f"Failed to identify research gaps: {gaps_result.get('error', 'Unknown error')}")
        else:
            st.warning("No literature review available for gap analysis.")
    
    # Display existing research gaps
    if st.session_state.research_gaps:
        st.write(st.session_state.research_gaps)
    elif st.session_state.search_completed:
        st.info("No research gaps identified yet. Please try searching for research papers first.")

# References Tab
with tab4:
    st.header("References")
    
    # Citation style selection moved to References tab
    citation_style = st.selectbox(
        "Citation Style",
        ["APA", "MLA", "Chicago", "Harvard", "IEEE"],
        index=["APA", "MLA", "Chicago", "Harvard", "IEEE"].index(st.session_state.citation_style)
    )
    
    # Update citation style and regenerate references if changed
    if citation_style != st.session_state.citation_style:
        st.session_state.citation_style = citation_style
        # Update references list with new citation style
        if st.session_state.sources:
            st.session_state.references_list = research_workflow["generate_references_list"]({
                "sources": st.session_state.sources,
                "citation_style": citation_style
            })["references_list"]
    
    # Display sources with links
    if st.session_state.sources:
        st.subheader("Sources")
        for i, source in enumerate(st.session_state.sources):
            with st.expander(f"{i+1}. {source.get('title', 'Untitled')}"):
                if source.get('url'):
                    st.markdown(f"**Link:** [{source.get('url')}]({source.get('url')})")
                if source.get('authors'):
                    st.markdown(f"**Authors:** {source.get('authors')}")
                if source.get('publication'):
                    st.markdown(f"**Publication:** {source.get('publication')}")
                if source.get('year'):
                    st.markdown(f"**Year:** {source.get('year')}")
                if source.get('abstract'):
                    st.markdown("**Abstract:**")
                    st.markdown(source.get('abstract'))
                if source.get('keywords'):
                    st.markdown(f"**Keywords:** {', '.join(source.get('keywords', []))}")
    else:
        st.info("No sources available. Please search for research papers first.")
    
    # Display references list
    if st.session_state.references_list:
        st.subheader("Formatted References List")
        st.markdown(st.session_state.references_list)
    else:
        st.info("No references list generated yet. Select a citation style to generate references.")
    
    # Export button
    if st.session_state.references_list:
        st.download_button(
            label="Download References",
            data=st.session_state.references_list,
            file_name=f"references_{st.session_state.citation_style.lower()}.txt",
            mime="text/plain"
        )

# Footer
st.markdown("---")
