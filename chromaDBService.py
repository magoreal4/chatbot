import chromadb, re 
from chromadb.config import Settings
from embOpenAIService import MyEmbedding

class MyChromaDB:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./dbChroma" # Optional, defaults to .chromadb/ in the current directory
            ))
        self.embeddings = MyEmbedding()
        
    def get_id(self, texto: str):
        words = re.findall(r'\w+', texto)
        if len(words) < 5:
            result = "_".join(words)
        else:
            result = "_".join(words[:5])
        return result
    
    def create_db(self, textos: list[str], collection_name: str):
        ids = []
        for text in textos:
            id = self.get_id(text)
            ids.append(id)
        embeddings, t_token = self.embeddings.get_list_embeddings(textos)
        collection = self.client.create_collection(name=collection_name,
                                                embedding_function=self.embeddings.get_embedding)
        collection.add(ids=ids, 
                       embeddings=embeddings, 
                       documents=textos,
                       metadatas=[{"source": f"{i}-pl"} for i in range(len(textos))]
                       )
        self.client.persist()
        print("Cantidad de embeddings: ", len(embeddings))
        print('-----------')
        print("Tokens: ",t_token)
        print("Guardado el embedding en base de datos")

    def list_collections(self):
        collections = self.client.list_collections()
        colecciones = [collection.name for collection in collections]
        return colecciones
  