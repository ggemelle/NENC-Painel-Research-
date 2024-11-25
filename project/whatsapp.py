from twilio.rest import Client

def enviar_mensagem(nome, numero):
    ACCOUNT_SID = "seu_account_sid"
    AUTH_TOKEN = "seu_auth_token"
    WHATSAPP_NUMBER = "whatsapp:+14155238886"

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    mensagem = f"Olá {nome}, obrigado por participar! Vamos agendar um encontro."
    
    client.messages.create(
        body=mensagem,
        from_=WHATSAPP_NUMBER,
        to=f"whatsapp:{numero}"
    )
