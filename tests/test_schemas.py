from contextlib import nullcontext as does_not_raise

import pytest
from pydantic import ValidationError

from src.schemas import CreatePromtSchema, PromtSchema


def test_create_prompt_schema():
    data = {"prompt": "Hello, world!"}
    schema = CreatePromtSchema(**data)
    assert schema.prompt == "Hello, world!"


@pytest.mark.parametrize(
    "data, exc",
    [
        ({"prompt": "Hello, world!"}, pytest.raises(ValidationError)),
        (
            {
                "id": 1,
                "prompt": "Hello, world!",
                "response": "Hello, world!",
                "created_at": "2020-01-01T00:00:00Z",
            },
            does_not_raise(),
        ),
    ],
)
def test_prompt_schema(data, exc):
    with exc:
        PromtSchema(**data)
