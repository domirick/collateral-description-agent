import sys

from smolagents import CodeAgent, OpenAIServerModel, ToolCallingAgent
from smolagents import WebSearchTool, VisitWebpageTool, FinalAnswerTool

import tools

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


# Descriptors

# This agent is deprecated, use tools.describe_image function instead
#image_descriptor_agent = ToolCallingAgent(
#    name="image_descriptor_agent",
#    description="This agent describes the asset in a single image, including its condition and accessories by getting the image's ID.",
#    tools=[tools.get_image_by_id],
#    model=light_model,
#)

information_aggregator = CodeAgent(
    name="information_aggregator",
    description="This agent aggregates informations.",
    tools=[],
    model=heavy_model,
)

description_manager = CodeAgent(
    name="description_manager",
    description="This agent manages can describe images and manages the information aggregator agent. The main objective is to create a description of the asset based on the images, but also can retrieve unique information from the images.",
    tools=[tools.describe_image],
    model=light_model,
    managed_agents=[information_aggregator],
)


# Deep research

web_search_agent = CodeAgent(
    name="web_search_agent",
    description="This agent performs web searches to gather information about assets.",
    tools=[
        WebSearchTool(), # may disable, because of the limited use
        VisitWebpageTool(),
        FinalAnswerTool(),
        tools.advanced_web_search,
    ],
    model=light_model,
)

research_planner = CodeAgent(
    name="research_planner",
    description="Plans an asset research based on the given information.",
    tools=[],
    model=light_model,
)

research_critic = CodeAgent(
    name="research_critic",
    description="Checks whether the information got from the web research is accurate based on the original request.",
    tools=[],
    model=reasoning_model,
)

research_manager = CodeAgent(
    name="research_manager",
    description="Manages the web search agent, research planner and research critic. The main objective estimate the value of an asset by its description with comparing similar items and its prices found online.",
    tools=[],
    model=light_model,
    managed_agents=[web_search_agent, research_planner, research_critic],
)


# Value estimator

manager_agent = CodeAgent(
    name="manager_agent",
    description="The big boss, manages the research manager agent and the description manager agent. The main objective is to estimate the value of an asset properly. Will get a list of images (as IDs) about the asset, and need to describe those images, then research similar items online. Finally, it will estimate the value of the asset based on the description and the research.",
    tools=[],
    model=heavy_model,
    managed_agents=[research_manager, description_manager],
    add_base_tools=True,
)