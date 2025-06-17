from pydantic import BaseModel, Field

class Asset(BaseModel):
    """Represents an asset with a name and description."""
    name: str = Field(..., description="The name of the asset.")
    description: str = Field(..., description="A brief description of the asset.")
    condition: str = Field(..., description="A brief description of the condition of the asset.")
    category: str = Field(..., description="The big category of the asset.")