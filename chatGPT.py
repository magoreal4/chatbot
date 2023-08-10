# 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
import openai
import os
from dotenv import load_dotenv, find_dotenv
from langchain.chains import RetrievalQA
from langchain.tools import BaseTool
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.prompts import PromptTemplate
from memoryServices import MemoryClient


class OpenAIConfigKey:
    def __init__(self):
        _ = load_dotenv(find_dotenv())
        openai.api_key = os.getenv('OPENAI_API_KEY')


class VectorDBConfig:
    def __init__(self):
        persist_directory = "dbChroma"
        vectordb = Chroma(
            collection_name="collection",
            embedding_function=OpenAIEmbeddings(),
            persist_directory=persist_directory
        )
        self.retriever = vectordb.as_retriever(search_kwargs={"k": 2})

class QAConfig:
    def __init__(self):
        retriever = VectorDBConfig()
        chat = ChatOpenAI(
            temperature=0,
            model_name='gpt-3.5-turbo',
        )
        prompt_template = """Para responder usa solo el contexto que se encuentra entre tres signos iguales para responder. Si no sabes la respuesta, simplemente contestas que no lo sabes, NO intentes inventar una respuesta. \
        ===
        {context}
        ===
        Pregunta: {question}"""
        prompt_qa = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        chain_type_kwargs = {"prompt": prompt_qa}
        
        self.qa = RetrievalQA.from_chain_type(
            llm=chat,
            retriever=retriever.retriever,
            chain_type="stuff",
            verbose=True,
            chain_type_kwargs=chain_type_kwargs
            )

# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class PrecioTool(BaseTool):
    name = "Calculo de precio"
    description = "Usar para responder preguntas sobre precios o costo del servicio."
    return_direct = True

    def _run(self, ubicacion: str) -> str:
        return "Para darle el precio, por favor envíenos su ubicación a través de este medio..."
        # return "Bs.300"
    
    def _arun(self, ubicacion: str) -> str:
        # return "Bs.400"
        raise NotImplementedError("This tool does not support async")


class AgentConfig:
    def __init__(self,telefono):
        qa_config = QAConfig()
        self.mem = MemoryClient(telefono+'.json')
        
        chat = ChatOpenAI(
            temperature=0,
            model_name='gpt-3.5-turbo',
        )
        
        tools = [
            PrecioTool(),
            Tool(
                name="Knowledge Base",
                func=qa_config.qa.run,
                description="Usar para responder a preguntas generales.",
                return_direct=True,
            ),
            ]

        sys_msg = 'Eres un asistente de atención al cliente para una empresa que da servicios de limpieza de pozos y cámaras sépticas (pozos ciegos). Respuesta concreta y en Español'
        
        file_exists = self.mem.check()
        memoria = self.mem.memory_start() if not file_exists else self.mem.read_file()
        
        self.agent = initialize_agent(
            tools=tools,
            llm=chat,
            max_iterations=2,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            early_stopping_method='generate',
            memory=memoria,
            handle_parsing_errors=True,
        )
        new_prompt = self.agent.agent.create_prompt(
            system_message=sys_msg,
            tools=tools
        )
        self.agent.agent.llm_chain.prompt = new_prompt
        
        # print(self.agent.agent.llm_chain.prompt)

# agent.agent.llm_chain.prompt.messages[0].prompt.template="Responde en Español"

# agent.agent.llm_chain.verbose=True
# langchain.debug = False

# import langchain
# # agent.agent.llm_chain.prompt
# # agent.agent.llm_chain.prompt.messages[0].prompt.template

# langchain.debug = False

# agent.agent.llm_chain.verbose=False



# print(agent.agent.llm_chain.prompt)


# agent.agent.llm_chain.prompt.messages[0]

