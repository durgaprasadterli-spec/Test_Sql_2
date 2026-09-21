# sql_agent.py

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from mysql_utils import (
    get_schema_text,
    execute_agent_query
)

# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found. Please add it to your .env file."
    )

# ==========================================================
# LLM
# ==========================================================



llm = ChatOpenAI(
    model="gpt-4o-mini",
    base_url="https://api.ai-gateway.tigeranalytics.com",
    temperature=0,
    api_key=OPENAI_API_KEY
)

# ==========================================================
# SQL GENERATION PROMPT
# ==========================================================

SQL_PROMPT = """
You are an expert MySQL analyst.

Convert the user's business question into a valid MySQL SELECT query.

Rules:
1. Generate ONLY SQL.
2. Use ONLY tables and columns available in the schema.
3. Do NOT invent columns or tables.
4. Do NOT use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE.
5. Return only executable MySQL SELECT statements.
6. Do not wrap SQL in markdown.
7. Use joins when required.
8. Add LIMIT 1 when the question asks for:
   - "highest"
   - "top 1"
   - "most"
   - "best"
Otherwise use LIMIT 100 for lists.
9.If the question contains "highest", "top 1", "maximum", "best", return ONLY ONE ROW using LIMIT 1.

Database Schema:
{schema}

User Question:
{question}
"""

prompt = ChatPromptTemplate.from_template(SQL_PROMPT)

# ==========================================================
# GENERATE SQL
# ==========================================================

def generate_sql(question: str) -> str:
    """
    Convert natural language question into SQL.
    """

    schema = get_schema_text()

    chain = prompt | llm

    response = chain.invoke(
        {
            "schema": schema,
            "question": question
        }
    )

    sql_query = response.content.strip()

    # Remove markdown if LLM accidentally returns it
    sql_query = sql_query.replace("```sql", "")
    sql_query = sql_query.replace("```", "")
    sql_query = sql_query.strip()
    if any(word in question.lower() for word in ["highest", "top 1", "maximum", "best"]):
        if "limit" not in sql_query.lower():
            sql_query += " LIMIT 1"

    return sql_query


# ==========================================================
# EXECUTE SQL
# ==========================================================
def execute_question(question: str):

    forbidden_keywords = [
        "delete",
        "drop",
        "truncate",
        "update",
        "insert",
        "alter",
        "create"
    ]

    if any(keyword in question.lower() for keyword in forbidden_keywords):
        return {
            "question": question,
            "error": (
                "Request Denied. This system only supports read-only "
                "data analysis. DELETE, UPDATE, INSERT, DROP, ALTER, "
                "and CREATE operations are not allowed."
            )
        }

    try:
        sql_query = generate_sql(question)
        results = execute_agent_query(sql_query)

        return {
            "question": question,
            "sql_query": sql_query,
            "results": results
        }

    except Exception as e:
        return {
            "question": question,
            "error": str(e)
        }
# def execute_question(question: str) -> dict:
#     """
#     Generate SQL and execute it.
#     """

#     try:

#         sql_query = generate_sql(question)

#         results = execute_agent_query(sql_query)

#         return {
#             "success": True,
#             "question": question,
#             "sql_query": sql_query,
#             "results": results
#         }

#     except Exception as e:

#         return {
#             "success": False,
#             "question": question,
#             "error": str(e)
#         }


# ==========================================================
# GENERATE FINAL ANSWER
# ==========================================================

def generate_answer(question: str) -> dict:
    """
    Wrapper used by LangGraph.
    """

    return execute_question(question)


# ==========================================================
# TESTING
# ==========================================================

if __name__ == "__main__":

    sample_question = "What are the top 10 products by revenue?"

    response = generate_answer(sample_question)

    print("\nQUESTION")
    print("=" * 60)
    print(response["question"])

    if response["success"]:

        print("\nGENERATED SQL")
        print("=" * 60)
        print(response["sql_query"])

        print("\nRESULTS")
        print("=" * 60)

        for row in response["results"]:
            print(row)

    else:

        print("\nERROR")
        print("=" * 60)
        print(response["error"])