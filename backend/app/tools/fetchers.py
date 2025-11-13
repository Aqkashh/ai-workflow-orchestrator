from langchain.tools import tool
import pandas as pd

@tool
def fetch_csv(path: str) -> str:
    """
    Purpose:
        Load and read a CSV file from the given file path.

    Use when:
        The user wants to inspect, summarize, or analyze a CSV file.

    Returns:
        A JSON-like string containing number of rows, columns,
        column names, and first 5 sample rows.
    """
    df = pd.read_csv(path)

    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "head": df.head(5).to_dict(orient="records")
    }
    return str(summary)
