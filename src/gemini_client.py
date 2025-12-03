from src.main_config import config
from google import genai

client: genai.Client = genai.Client(api_key=config.gimini_api_key)


def get_answer_from_gemini(promt: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=promt,
    )
    return response.text


if __name__ == "__main__":
    print(get_answer_from_gemini("What is the capital of France?"))
