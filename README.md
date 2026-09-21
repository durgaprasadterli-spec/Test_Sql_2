# Retail Sales SQL Agent using LangGraph and MySQL

## Project Overview

This project implements an AI-powered SQL Agent that converts natural language business questions into SQL queries, executes them against a MySQL database, and returns results.

The solution uses:

* Python
* MySQL
* LangChain
* LangGraph
* OpenAI GPT Models
* Pandas

The project demonstrates how Large Language Models (LLMs) can be used for natural language analytics over structured retail sales data.

---

## Dataset

The project uses the following datasets:

### Customers

Contains customer information.

### Products

Contains product catalog information.

### Stores

Contains store details including region and city.

### Sales Transactions

Contains sales orders, quantities, prices, discounts, payment status, and delivery status.

### Returns

Contains returned orders and return reasons.

---

## Project Structure

```text
project/
│
├── data/
│   ├── customers.csv
│   ├── products.csv
│   ├── stores.csv
│   ├── sales_transactions.csv
│   └── returns.csv
│
├── load_data.py
├── mysql_utils.py
├── sql_agent.py
├── graph.py
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---

## Installation

### 1. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

```env
OPENAI_API_KEY="sk-LxgNGxB-mLjUDGzblqlIsw"
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=Root@123
MYSQL_DATABASE=retail_ai_agent
```

---

## Create MySQL Database

```sql
CREATE DATABASE retail_ai_agent;
```

Create tables:

```sql
customers
products
stores
sales_transactions
returns
```

---

## Load Data

Run:

```bash
python load_data.py
```

This script:

* Reads CSV files
* Loads data into MySQL tables
* Verifies row counts

---

## Run SQL Agent

### Generate SQL

```bash
python sql_agent.py
```

Example Question:

```text
What are the top 10 products by revenue?
```

---

## Run LangGraph Workflow

```bash
python graph.py
```

Workflow:

1. User Question
2. SQL Generation
3. Query Execution
4. Result Formatting

---

## Run Interactive Application

```bash
python app.py
```

Example:

```text
Question:
Show total revenue by region.
```

Output:

```text
Generated SQL:
SELECT ...

Results:
...
```

---

## Output ScreenShot

Under the Output_Screenshot contains the agent answering business questions.

## Example Business Questions

* What are the top 10 products by revenue?
* Which store generated the highest sales?
* Show monthly revenue trends.
* Which products have the highest return rates?
* Show revenue by region.
* Which sales channel generates the most revenue?
* What are the top 5 customers by spending?
* Show payment status distribution.
* Which stores have the most returned orders?
* Show revenue by product category.

---

## Technology Stack

| Component              | Technology    |
| ---------------------- | ------------- |
| Programming Language   | Python        |
| Database               | MySQL         |
| Data Processing        | Pandas        |
| LLM Framework          | LangChain     |
| Workflow Engine        | LangGraph     |
| AI Model               | OpenAI GPT    |
| Environment Management | python-dotenv |

---

## Future Enhancements

* Streamlit Web Interface
* SQL Validation Layer
* Query History
* User Authentication
* Dashboard Integration
* Multi-Database Support
* Local LLM Support (Ollama)

---

## Author

Durga Prasad

StackAI Foundation – Agentic AI Explorer Assignment Level 2
