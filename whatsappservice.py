import requests, json

def send_message_whatsapp(data):
    try:
        token = "EAACu8yZAXCWcBOZCtdv5cLYgfJfKz4d4bgBItaWNbB0CFZCD5oiZBJPscW0f74aHtZCdpTGTJ30OSPZAJITJ9kLRoOf2l2AO8zMXXtZBgeIPETvBwaZBEgl2sqQ2fD5zno1gw18GubpmFAplr5bgvJdIwLoiRyaZB8I7y3ONLq3oVoqcUktabR7nhI9Ut2HyKnocyKzueLCUP4DPKJ5bjjx5E8o5BIJNpzFYnnPwZD"
        url = "https://graph.facebook.com/v17.0/113516011804071/messages"

        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + token}
        response = requests.post(url=url, 
                                 data= data, 
                                 headers=headers)
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        print(e)
        return False

# send_message_whatsapp("Chalo", 59178040021)
