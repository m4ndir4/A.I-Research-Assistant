# AI Research Assistant - 

## Overview

This application is an AI-powered research assistant built using Streamlit, designed to help users perform comprehensive research, generate literature reviews, identify research gaps, and format references in various citation styles. The application integrates multiple agents to assist with research tasks, leveraging OpenAI and Tavily APIs for intelligent analysis and drafting.

## Key Components

1. **Environment Setup**:
   - The application uses the `.env` file to store essential API keys (OpenAI and Tavily). These keys are required to interact with the APIs for research, analysis, and drafting tasks.
   - It ensures that both API keys are present before proceeding with the application.

2. **Session State**:
   - The application initializes session states to store and manage the user's progress across different research tasks:
     - `sources`: A list of research sources retrieved from the search results.
     - `citation_style`: Stores the selected citation style for formatting references (APA, MLA, Chicago, etc.).
     - `literature_review`: Holds the generated literature review.
     - `research_gaps`: Holds identified research gaps.
     - `references_list`: Stores the formatted list of references based on the selected citation style.
     - `search_completed`: Flag to track if the research process has been completed.
     - `paper_summary_table`: Stores a summary table of the papers reviewed.

3. **Agent Initialization**:
   - Multiple agents are initialized to handle different tasks:
     - `ResearchAgent`: Responsible for finding relevant research papers based on a search query.
     - `AnalysisAgent`: Performs in-depth analysis of the search results.
     - `DraftingAgent`: Helps with drafting and refining research content.
     - `LiteratureReviewAgent`: Creates a thematic literature review based on the sources.
     - `ResearchGapsAgent`: Identifies research gaps from the generated literature review.

4. **Research Workflow**:
   - The `create_research_workflow` function organizes these agents into a cohesive workflow that facilitates the automatic completion of tasks like research paper search, literature review generation, research gap identification, and reference formatting.

5. **Page Setup**:
   - **Streamlit Page Configuration**:
     - The application uses `st.set_page_config` to set the page title, icon, layout, and sidebar state.
   
   - **Sidebar**:
     - The sidebar displays the list of research sources, citation style selection, and a section for viewing and downloading the formatted references list.
   
   - **Main Content**:
     - The main content area features tabs for different functionalities:
       - **Research Papers Tab**: Allows users to search for research papers by entering a query. It automatically displays the search results, generates a literature review, and identifies research gaps.
       - **Literature Review Tab**: Displays the generated literature review based on the sources collected in the research tab. It also displays a paper summary table.
       - **Research Gaps Tab**: Identifies and displays the gaps in the current research from the literature review.
       - **References Tab**: Lets users select the citation style (APA, MLA, etc.) and view the formatted references list. It also provides an option to download the references list.

---

## Detailed Explanation of Functionalities

### 1. **Research Papers Tab**:

#### Search for Research Papers:
- Users can input a research question in a text box.
- Upon clicking "Search Research Papers," the `research_agent` is triggered to search for research papers related to the query. The search results are displayed in the form of paper titles, URLs, content, and other details.

#### Automatic Tasks:
- **Literature Review Generation**: After fetching the research papers, the `literature_review_agent` generates a thematic literature review using the sources retrieved.
- **Research Gaps Identification**: The `research_gaps_agent` identifies research gaps from the literature review.
- **Paper Summary Table**: The `literature_review_agent` also creates a summary table of the reviewed papers.

### 2. **Literature Review Tab**:
- **Generate Literature Review**: Users can click a button to regenerate the literature review based on the current sources. If the review generation is successful, it is displayed as a table with a summary of each paper.

### 3. **Research Gaps Tab**:
- **Identify Research Gaps**: Users can regenerate the research gaps by clicking a button. The system identifies gaps based on the literature review generated in the previous step.

### 4. **References Tab**:
- **Citation Style Selection**: Users can select a citation style (APA, MLA, Chicago, Harvard, IEEE). Upon selection, the application regenerates the formatted references list according to the new style.
- **Formatted References**: The references list is shown in the selected citation style. It can be downloaded as a `.txt` file.

---

## Code Explanation

### Environment Variables & API Keys
- The application relies on two API keys, OpenAI and Tavily. These keys are loaded from the `.env` file using `load_dotenv()`. If either of the keys is missing, an error is displayed, and the application stops.

```python
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    st.error("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
    st.stop()

if not os.getenv("TAVILY_API_KEY"):
    st.error("Tavily API key not found. Please set TAVILY_API_KEY in your .env file.")
    st.stop()
