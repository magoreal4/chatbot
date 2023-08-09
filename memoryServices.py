import json,os,aiofiles
from langchain.schema import messages_from_dict, messages_to_dict
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.memory import ConversationBufferMemory


class MemoryClient:    
    def __init__(self, filename):
        self.filename = filename

    def check(self):
        return os.path.exists(self.filename)
    
    def memory_start(self):
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
            )
        return memory

    def read_file(self):
        with open(self.filename, 'r') as f:
            retrieve_from_db = json.load(f)
            retrieved_messages = messages_from_dict(retrieve_from_db)
            retrieved_chat_history = ChatMessageHistory(messages=retrieved_messages)
            retrieved_memory = ConversationBufferMemory(
                chat_memory=retrieved_chat_history,
                return_messages=True,
                memory_key="chat_history"
                )
        return retrieved_memory

    def write_file(self, extracted_messages):
        ingest_to_db = messages_to_dict(extracted_messages)
        with open(self.filename, 'w') as f:
            json.dump(ingest_to_db, f)
