# Import operating system interface module
import os
# Import dotenv to load environment variables from .env file
from dotenv import load_dotenv
# Import requests library for making HTTP requests
import requests
# Load environment variables from .env file
load_dotenv()

def scrap_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    Scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile
    """
    # Check if mock mode is enabled (for testing with sample data)
    if mock:
        # Use a mock LinkedIn profile URL from GitHub gist for testing
        linkedin_profile_url = "https://gist.githubusercontent.com/uygaraydin/812b7bbc2c8f13a6f832d91b484220f7/raw/3aef6d651c0c6cc3a81798d383f2132280481c69/uygar-linkedin-scraping.json"
        # Make HTTP GET request to the mock URL with 10 second timeout
        response = requests.get(
            linkedin_profile_url,
            timeout=10
        )

    else:
        # Use the real Scrapin.io API endpoint for LinkedIn profile scraping
        api_endpoint ="https://api.scrapin.io/enrichment/profile"
        # Set up parameters for the API request
        params = {
            "linkedInUrl": linkedin_profile_url,
            "apikey": os.getenv("SCRAPIN_API_KEY")
        }
        # Make HTTP GET request to the API with parameters and 10 second timeout
        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10
        )
    
    # Extract the 'person' data from the JSON response
    data=response.json().get("person")


    # Filter out empty values and unwanted fields from the data
    data = {
        k: v
        for k, v in data.items()
        if v not in([], "", "", None) and k not in ["testScores"]
    }

    # Return the cleaned and filtered profile data
    return data