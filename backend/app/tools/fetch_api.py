from langchain.tools import tool
import requests


@tool
def fetch_api(url: str,auth_token: str = None) -> str:
    """
         Purpose:
        Fetch JSON data from a public or authenticated API endpoint.

    Use when:
        The user requests data from a URL, API endpoint, or wants to inspect,
        summarize, or analyze JSON coming from an external source.

    Returns:
        A JSON-like string containing:
        - status code
        - first few keys
        - preview of the response data

    Notes:
        Uses GET request only. 
        Use this tool instead of trying to reason about API responses manually.
    """
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    try:
        data = response.json()
    except:
        return f"Non-JSON response: {response.text[:500]}"

    # Preview data
    if isinstance(data, list):
        preview = data[:3]
    else:
        preview = {k: str(v)[:200] for k, v in list(data.items())[:5]}

    return str({
        "status_code": response.status_code,
        "preview": preview
    })       