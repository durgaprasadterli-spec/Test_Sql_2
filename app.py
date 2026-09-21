# app.py

from sql_agent import execute_question

def main():

    print("=" * 60)
    print("Retail Sales SQL Agent")
    print("=" * 60)
    print("Type your business question.")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:

        question = input("\nQuestion: ").strip()

        if question.lower() in ["exit", "quit", "q"]:
            print("\nGoodbye!")
            break

        if not question:
            print("Please enter a valid question.")
            continue

        try:

            response = execute_question(question)

            if "error" in response:

                print("\nERROR")
                print("-" * 50)
                print(response["error"])

            else:

                print("\nGENERATED SQL")
                print("-" * 50)
                print(response["sql_query"])

                print("\nRESULTS")
                print("-" * 50)

                results = response["results"]

                if results is not None and not results.empty:
                    print("\nRESULTS")
                    print("-" * 50)
                    print(results)
                else:
                    print("\nRESULTS")
                    print("-" * 50)
                print("No records found.")

        except Exception as e:

            print(f"\nUnexpected Error: {e}")



if __name__ == "__main__":
    main()