from chatGPT import OpenAIConfigKey, AgentConfig
from langchain.callbacks import get_openai_callback

def input(text, number):
    key = OpenAIConfigKey()
    agente = AgentConfig(number)
        
    with get_openai_callback() as cb:
        # response = agent.run("Hola, mi nombre es Gonzalo")
        response = agente.agent.run(text)
        # response = agent.run("Que profundidad debe tener un pozo?")
        # response = agent.run("Anotaste mi nombre?")
        # response = agent.run("Capital de Peru?")
        # print(response)
        # print(f"Total Tokens: {cb.total_tokens}")
        # print(f"Prompt Tokens: {cb.prompt_tokens}")
        # print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")
        extracted_messages = agente.agent.memory.chat_memory.messages
        agente.mem.write_file(extracted_messages)
        return response




# preguntas = ["Hola, mi nombre es Gonzalo", "trabajan en La guardia", "?"]
