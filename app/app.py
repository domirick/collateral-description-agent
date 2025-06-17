import os

from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from PIL import Image

import agents, models

# Set up telemetry
register()
SmolagentsInstrumentor().instrument()

# Load images
files = os.listdir("data") # TODO: set to arg

images = [Image.open(os.path.join("data",img_path)) for img_path in files if img_path.endswith(('.png', '.jpg', '.jpeg'))]

# Start agentic workflow

# TODO: make few-shot examples for the agents from training data

img_descriptions = []

for image in images:
    img_desc = agents.descriptor_agent.run(
        "You are a descriptor agent. Please describe what you see on the image, and its condition as precise as you can for further value estimation.\n",
        images=[image]
    )
    img_descriptions.append(img_desc)

aggragated_description = agents.aggregator.run(
    "You are an information aggregator agent. You get descriptions about an asset. Please summarize the descriptions focusing on the asset's main properties and its condition. This information would be used for value estimation. \n"
    + "\n".join(img_descriptions)
)

final_estimation = agents.manager_agent.run(
    "You are a value estimation agent. Estimate the asset's value based on the description. You can run the web_search_agent, if you want to search for similar items.\n"
    + "Here is the description of the asset:\n" + aggragated_description,
)