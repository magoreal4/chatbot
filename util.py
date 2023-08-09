import json

def get_text_user(message):
    text = ""
    tipo = ""
    
    if 'text' in message:
        print("Tipo Mensaje")
        text = message['text']['body']
        tipo = 'texto'
    elif 'location' in message:
        print("Tipo Location")
        tipo = 'location'
        # interactiveObject = message['interactive']
        # typeInteractive = interactiveObject['type']
        # if typeInteractive == 'button_reply':
        #     text = interactiveObject['button_reply']['title']
        # elif typeInteractive == 'list_reply':
        #     text = interactiveObject['list_reply']['title']
        # else:
        #     print("sin mensaje")
    else:
        print("sin mensaje")

    return text, tipo

def text_message(text, number):
    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": text
            }
        })
    return data
