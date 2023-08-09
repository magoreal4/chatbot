from dotenv import load_dotenv, find_dotenv
import openai, os

from tenacity import retry, wait_random_exponential, stop_after_attempt

class MyEmbedding:
    def __init__(self):
        _ = load_dotenv(find_dotenv())
        openai.api_key = os.getenv('OPENAI_API_KEY')

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def get_embedding(self, text: str, model="text-embedding-ada-002") -> list[float]:
        create_embedding = openai.Embedding.create(
            input=[text], 
            model=model
            )
        embedding = create_embedding["data"][0]["embedding"]
        # p_token = create_embedding["usage"]["prompt_tokens"] 
        t_token = create_embedding["usage"]["total_tokens"] 
        return embedding, t_token

    def get_list_embeddings(self, textos: list[str]):
        t_token = 0
        embeddings = []
        for text in textos:
            embedding, total_token = self.get_embedding(text)
            embeddings.append(embedding)
            t_token = t_token + total_token
        return embeddings, t_token



