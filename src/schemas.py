from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class PromtSchema(BaseModel):
    id: int
    response: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CreatePromtSchema(BaseModel):
    promt: str = Field(
        description="The prompt to generate text from",
        example="What is the capital of France?",
        min_length=1,
    )
