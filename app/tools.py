import base64
from openai import OpenAI
from smolagents import tool

VISION_MODEL = "gpt-4.1-mini"

@tool
def describe_image(image_path: str, prompt: str) -> str:
    """
    Describe an image using Vision Language Model.

    Args:
        image_path (str): Path to the image file.
        prompt (str): Description prompt for the image.
    """

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