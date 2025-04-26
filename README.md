
# AI Research Assistant - Project Documentation

## 1. Project Overview
The AI Research Assistant is an AI-powered tool designed to automate key aspects of the research process, such as finding research papers, generating literature reviews, identifying research gaps, and formatting citations. This tool integrates OpenAI API and Tavily API to enhance the efficiency and productivity of researchers. It streamlines the research workflow, allowing researchers to focus on critical tasks while AI handles the repetitive and time-consuming processes.

## 2. Key Features

### Research Paper Search:
**How it works:** The application uses Tavily API to fetch research papers based on user input. The papers are retrieved from a variety of academic sources and are tailored to match the user’s query.  
Traditional paper searches require manual filtering and reading. This tool automates the retrieval process, curating the most relevant and impactful research papers, saving time, and increasing the efficiency of literature searches.

### Literature Review Generation:
**How it works:** The AI analyzes the content of the fetched research papers and creates a structured literature review, categorizing the papers into relevant themes and summarizing key insights.  
Literature reviews are a critical yet time-consuming part of the research process. This feature automates it, organizing research into digestible sections, allowing researchers to focus on analysis rather than content summarization.

### Research Gap Identification:
**How it works:** By analyzing the generated literature review, the system identifies unexplored areas in the field. These research gaps are presented clearly for the user.  
Identifying research gaps can be subjective and difficult. This tool uses AI to automatically flag gaps in the literature, providing clear direction for future research.

### Citation Style Formatting:
**How it works:** The tool formats references according to multiple citation styles such as APA, MLA, and Chicago.  
Citation formatting is automated, ensuring that references are consistent and error-free. This is particularly useful for large projects with numerous citations, eliminating the need for manual formatting.

## 3. Technologies Used

The application utilizes various advanced technologies to achieve its functionality:

**Backend AI:**
- **OpenAI API:** Powers the text analysis and generation aspects of the project. It enables the drafting of summaries, identification of research gaps, and citation formatting.
- **Tavily API:** Fetches research papers based on the user’s query. Tavily allows for academic-grade results that are curated and relevant to the user’s input.

**Libraries:**
- **requests:** Used for making API calls to external services.
- **pandas:** For data management, organizing and processing the fetched papers and generating reports.
- **dotenv:** Securely handles environment variables, ensuring that sensitive API keys remain protected.

## 4. Installation Guide

Here’s how you can set up the AI Research Assistant locally:

1. Clone the Repository:
   ```bash
   git clone https://github.com/yourusername/ai-research-assistant.git
   cd ai-research-assistant
   ```

2. Set up Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up Environment Variables:
   - Create a `.env` file in the root directory and add your API keys:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

5. Run the Application:
   ```bash
   python app.py
   ```

## 5. Project Structure

Here’s the structure of the project and an overview of key files:

- `app.py`: Main application logic that coordinates the research process and handles user inputs.
- `agents.py`: Contains agent classes responsible for different functionalities such as fetching papers, generating summaries, and formatting citations.
- `utils.py`: Utility functions for managing data and assisting with background tasks.
- `.env`: Stores API keys securely.
- `requirements.txt`: Lists dependencies needed for the project.
- `assets/`: Folder containing static assets, such as images or data files.

## 6. Application Workflow

The AI Research Assistant operates through a straightforward workflow that automates essential research tasks:

1. **Search for Research Papers:** The user inputs a query, and the system fetches relevant academic papers using the Tavily API.

2. **Generate Literature Review:** The AI analyzes the fetched papers and organizes them into a structured literature review, summarizing key insights and categorizing the information into thematic sections.

3. **Identify Research Gaps:** The system scans the generated review to identify unexplored research areas, providing clear suggestions for new research directions.

4. **Citation Style Formatting:** The references in the literature review are formatted according to the selected citation style (APA, MLA, Chicago, etc.).

5. **Download References:** The references can be exported as a `.txt` file for easy use in research papers.

## 7. Code Explanation

### Environment Setup:
The application uses dotenv to manage sensitive information like API keys securely:
```python
load_dotenv()
if not os.getenv('OPENAI_API_KEY'):
    raise ValueError('OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.')
if not os.getenv('TAVILY_API_KEY'):
    raise ValueError('Tavily API key not found. Please set TAVILY_API_KEY in your .env file.')
```

### Session Management:
Streamlit's session state is used to manage user data across different steps in the research process:
```python
if 'sources' not in st.session_state:
    st.session_state.sources = []
if 'citation_style' not in st.session_state:
    st.session_state.citation_style = 'APA'
```

### Agent Classes:
The system uses different agent classes for specific tasks:
- `ResearchAgent`: Fetches relevant research papers.
- `AnalysisAgent`: Analyzes the content of the papers.
- `DraftingAgent`: Assists in drafting the literature review sections.
- `ResearchGapsAgent`: Identifies unexplored research areas.

## 8. Conclusion

The AI Research Assistant simplifies and accelerates the research process through automation. With AI-driven features like paper search, literature review generation, research gap identification, and citation formatting, the tool allows researchers to focus on higher-level thinking while the application handles time-consuming tasks. This not only improves efficiency but also ensures consistency and accuracy throughout the research lifecycle. With this project, you can demonstrate technical capabilities in integrating AI models, APIs, and data processing to create an impactful research tool.
