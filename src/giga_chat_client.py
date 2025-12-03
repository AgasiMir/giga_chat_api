from gigachat import GigaChat
from environs import Env

env = Env()
env.read_env(".env")

giga_key = env("GIGACHAT_API_KEY")

giga = GigaChat(
   credentials=giga_key,
   scope="GIGACHAT_API_PERS",
   model="GigaChat",
)

promt: str = "What is the capital of France?"

def get_giga_response(prompt):
    messages = []
    for chunk in giga.stream(prompt):
        resp = chunk.choices[0].delta.content
        messages.append(resp)
        yield messages


if __name__ == "__main__":
    print(*get_giga_response("Расскажи о себе подробно"))
    # print('-' * 80)
    # res= list(get_giga_response("Расскажи о себе подробно"))
    # print(f"Messages: {res}")

