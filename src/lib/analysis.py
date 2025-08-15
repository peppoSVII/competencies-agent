import re
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_vertexai import VertexAI
from .jira_utils import clean_jira_text
from .db_utils import setup_database, save_analysis_to_db  # DB functions

def parse_llm_response(response_text):
    """Parses the Level and Justification from the LLM's response."""
    level_match = re.search(r"Level:\s*(\d)", response_text)
    justification_match = re.search(r"Justification:\s*(.*)", response_text, re.DOTALL)
    
    level = int(level_match.group(1)) if level_match else 0
    justification = justification_match.group(1).strip() if justification_match else "No justification provided."
    
    return level, justification

def analyze_competencies_with_langchain(competency_matrix, issues):
    """Analyzes competencies and saves results to the database."""
    load_dotenv()
    llm = VertexAI(model_name="gemini-2.5-pro", location="europe-west1")

    # Setup the database
    engine = setup_database()

    # Prepare the Jira ticket text
    jira_text_full = "\n".join([
        f"Ticket: {issue.key}\nSummary: {issue.fields.summary}\nDescription: {clean_jira_text(issue.fields.description)}\n"
        for issue in issues
    ])

    results = {}
    for index, row in competency_matrix.iterrows():
        skill_name = row['Skill']
        print(f"Analyzing skill: {skill_name}")

        input_text = f"""
You are an expert in evaluating professional competencies based on evidence from Jira tickets.
Your goal is to evaluate the user's skill level for a specific competency.

Skill: {skill_name}
Competency levels:
Level 1: {row['1']}
Level 2: {row['2']}
Level 3: {row['3']}
Level 4: {row['4']}
Level 5: {row['5']}

New Jira ticket descriptions:
{jira_text_full}

Considering the tickets, what is the user's current competency level (1-5) for '{skill_name}'?
Provide a single number as the level and a brief justification based on the evidence from the new tickets.

Format your answer as:
Level: [1-5]
Justification: [Your justification, highlighting evidence]
"""

        response = llm.invoke(input_text)
        
        # Handle both string and object responses
        if hasattr(response, 'content'):
            response_text = response.content
        else:
            response_text = response
            
        level, justification = parse_llm_response(response_text)

        # Save the result directly into the DB
        save_analysis_to_db(engine, skill_name, level, justification)

        # Update local results
        results[skill_name] = {
            "level": level,
            "justification": justification
        }

    return results

def generate_report(results):
    """Generates a markdown report from the analysis results."""
    report = "# Competency Matrix Report (LangChain Analysis)\n\n"
    report += f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    for skill, analysis in results.items():
        report += f"## {skill}\n\n"
        report += f"Level: {analysis['level']}\n"
        report += f"Justification: {analysis['justification']}\n\n"

    with open("data/competency_report_langchain.md", "w") as f:
        f.write(report)
    print("Report generated: data/competency_report_langchain.md")
