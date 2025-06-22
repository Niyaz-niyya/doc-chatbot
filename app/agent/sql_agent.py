from langchain_core.messages import HumanMessage
from app.config.llm import get_llm_client
from app.db.database import execute_sql_query

class SQLAgent:
    def __init__(self):
        self.llm = get_llm_client()

    def generate_sql(self, question: str, table_name: str) -> str:
        schema = self._get_table_schema(table_name)
        samples = self._get_column_samples(table_name)
        # Extract column names
        column_names = [line.split(':')[0].strip() for line in schema.split('\n')]
        prompt = f"""You are an expert SQL assistant.
    Given this database schema for table "{table_name}":
    {schema}

    Here are some sample values for each column:
    {samples}

    Generate a SQL query to answer this question: {question}
    - Use the exact table name "{table_name}" (with double quotes) in your query.
    - Only use column names exactly as shown in the schema above. Do NOT invent or guess column names.
    - If you cannot answer with the available columns, say so.
    - Do not include markdown formatting or backticks.
    Return ONLY the SQL query, nothing else."""
        messages = [HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)
        sql = response.content.strip()
        sql = sql.replace('```sql', '').replace('```', '').strip()
        print(f"Generated SQL: {sql}")
        return sql

    def execute_query(self, question: str, table_name: str) -> str:
        """Execute SQL query and return natural language response"""
        try:
            sql_query = self.generate_sql(question, table_name)
            results = execute_sql_query(sql_query)
            if not results:
                return f"No information found for your query in table {table_name}."
            formatted_results = self._format_results(results)
            response_prompt = f"""Based on this database query result, provide a natural language response.

                Question: {question}
                Table: {table_name}

                Results:
                {formatted_results}

                Provide a clear, detailed answer that describes all relevant information found in the results.
                Format important values like numbers, dates, and IDs in a readable way."""
            messages = [HumanMessage(content=response_prompt)]
            final_response = self.llm.invoke(messages)
            return final_response.content
        except Exception as e:
            print(f"Error details: {str(e)}")
            return f"Error executing query: {str(e)}"

    def _get_table_schema(self, table_name: str) -> str:
        query = """
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = :table_name
        """
        schema = execute_sql_query(query, {"table_name": table_name})
        return "\n".join([f"{col['column_name']}: {col['data_type']}" for col in schema])

    def _get_column_samples(self, table_name: str, limit: int = 5) -> str:
        """Get sample values for each column to help LLM map user-friendly names to codes."""
        # Get column names
        columns_query = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = :table_name
        """
        columns = execute_sql_query(columns_query, {"table_name": table_name})
        column_names = [col['column_name'] for col in columns]
        # Get sample rows
        sample_query = f'SELECT * FROM "{table_name}" LIMIT {limit}'
        samples = execute_sql_query(sample_query)
        # Format samples
        sample_lines = []
        for col in column_names:
            values = [str(row[col]) for row in samples if row[col] is not None]
            unique_values = list(dict.fromkeys(values))[:3]  # up to 3 unique non-null samples
            sample_lines.append(f"{col}: {', '.join(unique_values) if unique_values else 'N/A'}")
        return "\n".join(sample_lines)

    def _format_results(self, results: list) -> str:
        if not results:
            return "No results found."
        keys = results[0].keys()
        header = " | ".join(keys)
        separator = "-|-".join(['-' * len(k) for k in keys])
        rows = [" | ".join(str(row[k]) for k in keys) for row in results]
        return f"{header}\n{separator}\n" + "\n".join(rows)