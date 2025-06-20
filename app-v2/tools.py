import base64
import os
from openai import OpenAI
from smolagents import tool, Tool
from tavily import TavilyClient

VISION_MODEL = "gpt-4.1-mini"

@tool
def describe_image(image_id: str, prompt: str) -> str:
    """
    Describe an image using Vision Language Model.

    Args:
        image_id (str): ID of the image.
        prompt (str): Description prompt for the image.

    Returns:
        str: The description of the image.
    """
    image_path = os.path.join("data",image_id)

    with open(image_path, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode("utf-8")

    data_url = f"data:image/png;base64,{base64_image}"

    client = OpenAI()

    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": data_url
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content

@tool
def advanced_web_search(search_string: str) -> dict:
    """
    Perform an advanced web search using Tavily.
    Args:
        search_string (str): The search query string.
    Returns:
        dict: The response from the Tavily search.
    """
    # Step 1. Instantiating your TavilyClient
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY", ""))

    # Step 2. Executing a simple search query
    response = tavily_client.search(search_string)

    # Step 3. That's it! You've done a Tavily Search!
    return response
    
class AdvancedWebSearchTool(Tool):
    """
    Tool to perform an advanced web search using Tavily.
    """    
    name = "advanced_web_search"
    description = "Performs a web search for a query and returns a string of the top search results."
    inputs = {"query": {"type": "string", "description": "The search query to perform."}}
    output_type = "string"

    def __init__(
        self
    ):
        super().__init__()
        from tavily import TavilyClient
        self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY", ""))

    def forward(self, query: str) -> dict:
        response = self.tavily_client.search(query)
        return response