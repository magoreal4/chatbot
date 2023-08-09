ChatPromptTemplate(
input_variables=['input', 'chat_history', 'agent_scratchpad'], 
output_parser=None, 
partial_variables={}, 
messages=[
    SystemMessagePromptTemplate(
        prompt=PromptTemplate(input_variables=[], output_parser=None, partial_variables={}, template='Responde en Español', template_format='f-string', validate_template=True), 
        additional_kwargs={}), 
    MessagesPlaceholder(variable_name='chat_history'), 
    HumanMessagePromptTemplate(
        prompt=PromptTemplate(input_variables=['input'], output_parser=None, partial_variables={}, template='TOOLS\n
                              ------\n
                              Assistant can ask the user to use tools to look up information that may be helpful in answering the users original question. The tools the human can use are:\n\n> Calcula el precio: Útil cuando necesitas responder preguntas sobre precios o el costo del servicio.\n> Knowledge Base: Útil cuando necesitas responder a preguntas de conocimiento general.\n\nRESPONSE FORMAT INSTRUCTIONS\n----------------------------\n\nWhen responding to me, please output a response in one of two formats:\n\n**Option 1:**\nUse this if you want the human to use a tool.\nMarkdown code snippet formatted in the following schema:\n\n```json\n{
        {\n    "action": string, \\ The action to take. Must be one of Calcula el precio, Knowledge Base\n    "action_input": string \\ The input to the action\n
        }
    }\n```\n\n**Option #2:**\nUse this if you want to respond directly to the human. Markdown code snippet formatted in the following schema:\n\n```json\n{
        {\n    "action": "Final Answer",\n    "action_input": string \\ You should put what you want to return to use here\n
        }
    }\n```\n\nUSER\'S INPUT\n--------------------\nHere is the user\'s input (remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else):\n\n{input
    }', template_format='f-string', validate_template=True), additional_kwargs={}), MessagesPlaceholder(variable_name='agent_scratchpad')
]