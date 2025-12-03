from environs import Env
from google import genai

env = Env()
env.read_env(".env")

key = env("GEMINI_API_KEY")

client: genai.Client = genai.Client(api_key=key)


def get_answer_from_gemini(promt: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=promt,
    )
    return response.text


if __name__ == "__main__":
    print(get_answer_from_gemini("What is the capital of France?"))
