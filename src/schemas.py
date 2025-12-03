from pydantic import BaseModel, Field


class PromtSchema(BaseModel):
    id: int
    asnwer: str


class CreatePromtSchema(BaseModel):
    promt: str = Field(
        description="The prompt to generate text from",
        example="What is the capital of France?",
        min_length=1,
    )
