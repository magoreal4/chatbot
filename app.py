from flask import Flask, request
import util, whatsappservice
from chatGPTInput import input

app = Flask(__name__)

@app.route('/welcome', methods=['GET'])
def index():
    return "Bienvenido"


@app.route('/whatsapp', methods=['GET'])
def verify_token():
    try:
        # accesToken = request.args.get('hub.verify_token')
        accesToken = "qwertyuiopasdfghjklzxcvbnm"
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if token is not None and challenge is not None and token == accesToken:
            return challenge
        else:
            return "Error",400
    except Exception as e:
        return e + " ",400


@app.route('/whatsapp', methods=['POST'])
def recived_message():
    
    body = request.get_json()
    entry = body['entry'][0]
    changes = entry['changes'][0]
    value = changes['value']
    message = (value['messages'])[0]
    number = message['from']    
    contenido, tipo = util.get_text_user(message)
    if (tipo == 'texto'):
        generate_message(contenido, number)
    return "EVENT_RECEIVED"

def generate_message(text, number):
    # print('----1----')
    texto = input(text, number)
    # print(texto)
    # print('----2----')
    data = util.text_message(texto, number)
    # print(data)
    # print('----3----')
    whatsappservice.send_message_whatsapp(data)

if(__name__ == '__main__'):
    app.run()