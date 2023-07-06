from dotenv import load_dotenv, find_dotenv
import openai
import os
import chromadb
from chromadb.config import Settings
from tenacity import retry, wait_random_exponential, stop_after_attempt

class MyEmbedding:
    def __init__(self, collection_name, persist_directory='dbChroma'):
        _ = load_dotenv(find_dotenv())
        openai.api_key = os.getenv('OPENAI_API_KEY')

        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            chroma_db_impl="duckdb+parquet",
        ))

        self.embedding_function = openai.Embedding()

        self.collection_name = collection_name

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def get_embedding(self, text: str, model="text-embedding-ada-002") -> list[float]:
        create_embedding = openai.Embedding.create(
            input=[text], 
            model=model
            )
        embedding = create_embedding["data"][0]["embedding"]
        p_token = create_embedding["usage"]["prompt_tokens"] 
        t_token = create_embedding["usage"]["total_tokens"] 
        return embedding, p_token, t_token

    def create_embeddings(self, textos):
        p_token = 0
        t_token = 0
        embeddings = []
        for text in textos:
            embedding, prompt_token, total_token = self.get_embedding(text)
            embeddings.append(embedding)
            p_token = p_token + prompt_token
            t_token = t_token + total_token
        return embeddings, p_token, t_token

    def create_db(self, data_tuple):
        docs = list(data_tuple)
        ids = [textos[:20] for textos in docs]
        embeddings, p_token, t_token = self.create_embeddings(docs)
        collection = self.client.create_collection(name=self.collection_name,
                                                embedding_function=self.get_embedding)
        collection.add(ids=ids, embeddings=embeddings, documents=docs)
        self.client.persist()
        print(len(embeddings))
        print('-----------')
        print(p_token)
        print('-----------')
        print(t_token)
        print("Guardado el embedding en base de datos")
