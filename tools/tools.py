# Import TavilySearchResults from LangChain community tools
from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(name: str) -> str:
    """Search linkedin or twitter profile page"""
    # Create a TavilySearchResults instance for web searching
    search = TavilySearchResults()
    # Search for the person's name specifically on LinkedIn using site: operator
    result =search.run(f"{name} site:linkedin.com")
    # Return the search results
    return result