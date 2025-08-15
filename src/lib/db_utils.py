import sqlalchemy
from datetime import datetime
from langchain_community.chat_message_histories import SQLChatMessageHistory

DB_FILE = "data/competency_history.sqlite"

def setup_database():
    """Creates the SQLite database and table if they don't exist."""
    engine = sqlalchemy.create_engine(f"sqlite:///{DB_FILE}")
    metadata = sqlalchemy.MetaData()
    
    if not sqlalchemy.inspect(engine).has_table("competency_history"):
        competency_history = sqlalchemy.Table('competency_history', metadata,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True),
            sqlalchemy.Column('skill', sqlalchemy.String),
            sqlalchemy.Column('level', sqlalchemy.Integer),
            sqlalchemy.Column('justification', sqlalchemy.String),
            sqlalchemy.Column('timestamp', sqlalchemy.DateTime, default=datetime.now)
        )
        metadata.create_all(engine)
        print("Database and table created.")
    
    # The message_history table will be created automatically by LangChain if it doesn't exist.
    return engine

def get_chat_history(session_id):
    """
    Creates and returns a SQLChatMessageHistory object backed by the SQLite database.
    Each skill will have its own session_id, creating a separate history for each.
    """
    connection_string = f"sqlite:///{DB_FILE}"
    
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string=connection_string,
        table_name="message_history"
    )

def save_analysis_to_db(engine, skill, level, justification):
    """Saves the new analysis result to the database."""
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            query = sqlalchemy.text("INSERT INTO competency_history (skill, level, justification, timestamp) VALUES (:skill, :level, :justification, :timestamp)")
            connection.execute(query, {"skill": skill, "level": level, "justification": justification, "timestamp": datetime.now()})
            trans.commit()
        except:
            trans.rollback()
            raise
