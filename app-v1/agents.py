import sys

from smolagents import CodeAgent, OpenAIServerModel, ToolCallingAgent
from smolagents import WebSearchTool, VisitWebpageTool, FinalAnswerTool

# Load environment variables if specified
if len(sys.argv) > 1 and sys.argv[1] == "load_env":
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("Environment variables loaded successfully.")
    except Exception as e:
        print(f"Error loading environment variables: {e}")
        sys.exit(1)

# Models
heavy_model = OpenAIServerModel(model_id="gpt-4.1")
light_model = OpenAIServerModel(model_id="gpt-4.1-mini")
reasoning_model = OpenAIServerModel(model_id="o4-mini")

# Agents
image_descriptor_agent = ToolCallingAgent(
    tools=[],
    model=light_model,
)

web_search_agent = CodeAgent(
    name="web_search_agent",
    description="This agent performs web searches to gather information about assets.",
    tools=[
        WebSearchTool(),
        VisitWebpageTool(),
        FinalAnswerTool(),
    ],
    model=light_model,
)

information_aggregator = CodeAgent(
    tools=[],
    model=heavy_model,
)

manager_agent = CodeAgent(
    tools=[],
    model=light_model,
    managed_agents=[web_search_agent],
    add_base_tools=True,
)