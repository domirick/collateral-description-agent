import os

from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from PIL import Image

import agents

# Set up telemetry
register()
SmolagentsInstrumentor().instrument()

# Load images
files = os.listdir("data") # TODO: set to arg

images = [Image.open(os.path.join("data",img_path)) for img_path in files if img_path.endswith(('.png', '.jpg', '.jpeg'))]

# Start agentic workflow

# Prepare few-shot
with open("annotations_trimmed.md", "r") as f:
    annotations_md = f.read()

img_descriptions = []

for image in images:
    img_desc = agents.image_descriptor_agent.run(
        "You are a descriptor agent. Please describe the asset you see on the image, and its condition as precise as you can for further value estimation. You can also include the asset's accessories and documentation.\n",
        images=[image]
    )
    img_descriptions.append(img_desc)

# Save descriptions to file
with open("descriptions.txt", "w", encoding="utf-8") as f:
    for desc in img_descriptions:
        f.write(desc + "\n")

aggragated_description = agents.information_aggregator.run(
    "You are an information aggregator agent. You get descriptions about an asset. Please summarize the descriptions focusing on the asset's main properties and its condition. This information would be used for value estimation. \n"
    + "Here are some examples for the output: \n" + annotations_md
    + "\nHere are the descriptions to aggregate: \n" + "\n".join(img_descriptions)
)

final_estimation = agents.manager_agent.run(
    "You are a value estimation agent. Estimate the asset's value based on the description. You can run the web_search_agent, if you want to search for similar items.\n"
    + "Here is the description of the asset:\n" + aggragated_description,
)