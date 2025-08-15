# Competency Matrix Automation Agent

This project provides a Python-based agent that automates the evaluation of professional competencies by analyzing Jira tickets using a Large Language Model (LLM). It's designed to provide continuous, data-driven feedback on skill development.

## Features

- **Automated Competency Analysis**: Connects to Jira to fetch tickets and analyzes them against a predefined competency matrix.
- **LLM-Powered Evaluation**: Utilizes LangChain and Google's Gemini Pro model to perform nuanced analysis of ticket descriptions.
- **Historical Tracking**: Stores all analysis results in a SQLite database to track competency development over time.
- **Customizable Framework**: The competency matrix and analysis parameters are fully configurable through simple CSV and YAML files.
- **Markdown Reporting**: Generates a clean, easy-to-read markdown report after each run, summarizing the latest competency levels.

## Project Structure

-   **`src/`**: Contains the core Python source code.
    -   `competency_agent.py`: The main executable script.
    -   `lib/`: A module containing helper functions for analysis, database interactions, and Jira communication.
-   **`config/`**: Holds the configuration files.
    -   `config.yaml`: Main configuration for setting the Jira JQL query filter.
    -   `Competency_matrix.csv`: The competency framework, defining skills and proficiency levels.
-   **`data/`**: Stores the output data.
    -   `competency_history.sqlite`: The SQLite database for historical analysis data.
    -   `competency_report_langchain.md`: The generated markdown report.
-   **`.env`**: Stores secret credentials (Jira, Google Cloud). **This file is ignored by Git.**
-   **`requirements.txt`**: A list of all the Python dependencies required to run the project.
-   **`.gitignore`**: Specifies which files and directories to exclude from version control.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/peppoSVII/competencies-agent.git
    cd competencies-agent
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure your credentials:**
    -   Create a `.env` file in the project root. You can copy `config/config.yaml.example` to get started.
    -   Add your Jira and Google Cloud credentials to the `.env` file:
        ```env
        JIRA_SERVER="https://your-domain.atlassian.net"
        JIRA_USERNAME="your-email@example.com"
        JIRA_API_TOKEN="your_jira_api_token"
        
        # Path to your Google Cloud service account key file
        GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
        ```

4.  **Customize Configuration:**
    -   Open `config/config.yaml` and set the `jql_query` to filter the Jira tickets you want to analyze.
    -   Review and customize `config/Competency_matrix.csv` to match your team's competency framework.

## Usage

To run the agent, execute the main script from the root directory:

```bash
python src/competency_agent.py
```

The script will perform the following actions:
1.  Connect to Jira and fetch tickets based on your JQL query.
2.  Load the competency matrix from `config/Competency_matrix.csv`.
3.  Analyze the tickets using the LLM.
4.  Save the new analysis to the `data/competency_history.sqlite` database.
5.  Generate an updated summary report at `data/competency_report_langchain.md`.

## Contributing

Contributions are welcome! If you have ideas for improvements or find any issues, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
