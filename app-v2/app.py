import os

from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

import agents, models

# Set up telemetry
register()
SmolagentsInstrumentor().instrument()

# Load images
files = os.listdir("data") # TODO: set to arg

# Prepare few-shot
with open("annotations_trimmed.md", "r") as f:
    annotations_md = f.read()

# Start agentic workflow
agents.manager_agent.run(
    "You are value estimator agent. You should describe an image (like examples found bellow), and estimate its value. You can also run the research_manager agent for online research and description_manager agent for describing images.\n"
    "Here is the list of IDs of the images about the asset:\n"
    + "\n".join(files) + "\n"
    "Also, here is some example descriptions, what an asset description should look like:\n" + annotations_md
)