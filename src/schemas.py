from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CheckRequestSchema(BaseModel):
    ip_address: str
    prompt: str
    response: str


class PromtSchema(BaseModel):
    id: int = Field(description="The id of the request", ge=1)
    prompt: str = Field(description="The prompt to generate text from", min_length=1)
    response: str = Field(description="The response to the request", min_length=1)
    created_at: datetime = Field(
        description="The date and time the request was created"
    )

    model_config = ConfigDict(from_attributes=True)


class CreatePromtSchema(BaseModel):
    prompt: str = Field(
        description="The prompt to generate text from",
        example="What is the capital of France?",
        min_length=1,
    )
