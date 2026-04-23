#mock search implementation 
#fake search engine
#No API calls , just a search using if-else statements 

from langchain_core.tools import tool

@tool
def mock_searxng_search(query: str) -> str:
    """Return mock news headlines based on query keywords."""

    query = query.lower()

    if "crypto" in query or "bitcoin" in query:
        return "Bitcoin hits new all-time high amid regulatory ETF approvals."

    elif "ai" in query or "openai" in query:
        return "OpenAI released a new model that may replace junior developers."

    elif "market" in query or "stocks" in query:
        return "Stock markets surge as interest rates stabilize."

    return "Tech stocks rally as investors move into growth sectors."
