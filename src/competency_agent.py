import os
import pandas as pd
import yaml
from lib.jira_utils import get_jira_client, get_jira_issues
from lib.db_utils import setup_database
from lib.analysis import analyze_competencies_with_langchain, generate_report

def load_config(path="config/config.yaml"):
    """Loads the configuration from a YAML file."""
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def load_competency_matrix(path="config/Competency_matrix.csv"):
    """Loads the competency matrix from a CSV file."""
    return pd.read_csv(path)

def main():
    """Main function to run the competency agent."""
    engine = setup_database()
    config = load_config()
    competency_matrix = load_competency_matrix()
    jira_client = get_jira_client()
    issues = get_jira_issues(jira_client, config)

    if not issues:
        print("No Jira issues found for the specified period.")
        return

    results = analyze_competencies_with_langchain(competency_matrix, issues)
    
    # Generate the report from the results
    generate_report(results)

if __name__ == "__main__":
    main()
