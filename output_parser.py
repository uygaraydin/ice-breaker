# Import List and Dict types for type hints, Any for flexible typing
from typing import List, Dict, Any
# Import PydanticOutputParser from LangChain for structured output parsing
from langchain_core.output_parsers import PydanticOutputParser
# Import BaseModel and Field from Pydantic for data validation and modeling
from pydantic import BaseModel, Field

# Define Summary class as a Pydantic model for structured data
class Summary(BaseModel):
    # Summary field to store the main summary text
    summary: str = Field(description="summary")
    # Facts field to store a list of interesting facts
    facts: List[str] = Field(description="facts about the text")


    # Convert the Summary object to a dictionary format
    def to_dict(self) -> Dict[str, Any]:        
        return {"summary": self.summary, "facts": self.facts}
    

# Create a PydanticOutputParser instance using the Summary model
summary_parser = PydanticOutputParser(pydantic_object=Summary)






