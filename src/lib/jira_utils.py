import os
import re
from datetime import datetime, timedelta
from jira import JIRA
from dotenv import load_dotenv

def get_jira_client():
    """Initializes and returns a Jira client."""
    load_dotenv()
    server = os.getenv("JIRA_SERVER")
    user = os.getenv("JIRA_USERNAME")
    password = os.getenv("JIRA_PASSWORD")
    token = os.getenv("JIRA_API_TOKEN")

    if not all([server, user]):
        raise ValueError("Jira server and username environment variables not set.")

    if token:
        return JIRA(server=server, basic_auth=(user, token))
    elif password:
        return JIRA(server=server, basic_auth=(user, password))
    else:
        raise ValueError("Jira API token or password not set in environment variables.")

def get_jira_issues(jira_client, config):
    """Fetches Jira issues based on the start date in the config."""
    start_date_str = config.get("start_date")
    if start_date_str:
        start_date = start_date_str
    else:
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    jql_query = f'assignee = currentUser() AND created >= "{start_date}"'
    
    try:
        print(f"Fetching Jira issues with JQL: {jql_query}")
        issues = jira_client.search_issues(jql_query, maxResults=100)
        return issues
    except Exception as e:
        print(f"Error fetching Jira issues: {e}")
        return []

def clean_jira_text(text):
    """Cleans Jira's special formatting from text."""
    if not text:
        return ""
    text = re.sub(r'\{[^{}]+\}', '', text)
    text = re.sub(r'\[[^\[\]]+\]', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
