# Import dotenv to load environment variables
from dotenv import load_dotenv
# Import PromptTemplate from LangChain core prompts
from langchain_core.prompts import PromptTemplate
# Import ChatOpenAI for OpenAI language model integration
from langchain_openai import ChatOpenAI
# Import custom output parser and Summary class
from output_parser import summary_parser,Summary
# Import LinkedIn scraping function from third party modules
from third_parties.linkedin import scrap_linkedin_profile
# Import LinkedIn lookup agent from our custom agent module
from agent.linkedin_lookup_agent import lookup as linkedin_lookup_agent
# Import Tuple type for return type annotation
from typing import Tuple

def ice_break_with(name: str) -> Tuple[Summary,str]:
    # Find the LinkedIn profile URL using the lookup agent
    linkedin_username=linkedin_lookup_agent(name=name)
    # Scrape LinkedIn profile data using the found URL
    linkedin_data=scrap_linkedin_profile(linkedin_profile_url=linkedin_username)

    # Create template for generating summary and interesting facts
    summary_template="""
         given the linkedin information {information} about a person from I want you to create:
         1. A short summary
         2. two interesting facts about them

         Use the following format: {format_instructions}
        """

    # Create prompt template with input variables and format instructions
    summary_prompt_template=PromptTemplate(
        template=summary_template,
        input_variables=["information"],
        partial_variables={"format_instructions":summary_parser.get_format_instructions()}
        )

    # Initialize ChatOpenAI with GPT-4o-mini model (temperature=0 for consistent output)
    llm=ChatOpenAI(model="gpt-4o-mini",temperature=0)

    # Create processing chain: prompt template -> LLM -> parser
    chain=summary_prompt_template|llm|summary_parser

    # Execute the chain with LinkedIn data and get parsed Summary object
    res:Summary=chain.invoke({"information":linkedin_data})
    
    # Return the summary object and profile photo URL
    return res, linkedin_data.get("photoUrl")


# Main execution block (only runs when script is executed directly)
if __name__=="__main__":
    # Load environment variables
    load_dotenv()
    # Test the function with a specific name
    ice_break_with(name="Uygar Aydın")