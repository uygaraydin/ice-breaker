# Import system libraries
import sys
import os
# Add parent directory to Python path (to import our custom modules)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import LangChain libraries
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

# Import dotenv to load environment variables
from dotenv import load_dotenv

# Import profile URL finder function from our custom tools
from tools.tools import get_profile_url_tavily

# Load environment variables from .env file (API keys, etc.)
load_dotenv()


def lookup(name: str) -> str:
    # Create ChatOpenAI object using GPT-4o-mini model (temperature=0 for deterministic results)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Create prompt template for searching LinkedIn profile URLs
    template="""given the full name {name} I want you get it me a link to their Linkedin profile page.
    Your answer contain only the url."""

    # Create the prompt template with name parameter
    prompt_template=PromptTemplate(template=template,input_variables=["name"])

    # Define Tavily tool for finding LinkedIn profile URLs
    tavily_tool= Tool(
            name="Crawl Google 4 linkedin profile page",
            description="useful for when you need to get the LinkedIn url of a person",
            func=get_profile_url_tavily
        )

    # List of tools to be used by the agent
    tools_for_agent=[tavily_tool]
    
    # Pull pre-built ReAct prompt from the hub
    react_prompt=hub.pull("hwchase17/react")
    
    # Create ReAct agent with LLM, tools, and prompt
    agent=create_react_agent(llm=llm,tools=tools_for_agent, prompt=react_prompt)
    
    # Create agent executor to run the agent (verbose=True for detailed logging)
    agent_executor=AgentExecutor(agent=agent,tools=tools_for_agent, verbose=True)

    # Execute the agent and get result with formatted prompt containing the name
    result=agent_executor.invoke({"input":prompt_template.format_prompt(name=name)})
    
    # Extract LinkedIn profile URL from the result
    linkedin_profile_url=result["output"]
    
    # Return the found LinkedIn URL
    return linkedin_profile_url