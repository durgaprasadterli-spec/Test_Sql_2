# graph.py

from typing import TypedDict

from langgraph.graph import StateGraph, END

from sql_agent import generate_answer


# ==========================================================
# STATE
# ==========================================================

class AgentState(TypedDict):
    question: str
    result: dict


# ==========================================================
# NODE
# ==========================================================

def sql_agent_node(state: AgentState):

    question = state["question"]

    response = generate_answer(question)

    return {
        "result": response
    }


# ==========================================================
# BUILD GRAPH
# ==========================================================

builder = StateGraph(AgentState)

builder.add_node(
    "sql_agent",
    sql_agent_node
)

builder.set_entry_point("sql_agent")

builder.add_edge(
    "sql_agent",
    END
)

graph = builder.compile()


# ==========================================================
# TESTING
# ==========================================================

if __name__ == "__main__":

    question = "What are the top 10 products by revenue?"

    response = graph.invoke(
        {
            "question": question
        }
    )

    print("\nQUESTION")
    print("=" * 60)
    print(question)

    print("\nRESULT")
    print("=" * 60)

    result = response["result"]

    if result["success"]:

        print("\nSQL QUERY")
        print("-" * 60)
        print(result["sql_query"])

        print("\nDATA")
        print("-" * 60)

        for row in result["results"]:
            print(row)

    else:

        print("\nERROR")
        print("-" * 60)
        print(result["error"])