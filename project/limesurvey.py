import requests

LIMESURVEY_URL = "https://seu-limesurvey.com"
API_KEY = "sua_api_key"

def get_respostas(pesquisa_id):
    """Obtém respostas de uma pesquisa no LimeSurvey."""
    endpoint = f"{LIMESURVEY_URL}/index.php/admin/remotecontrol"
    payload = {
        "method": "export_responses",
        "params": {
            "sSessionKey": API_KEY,
            "iSurveyID": pesquisa_id,
            "sDocumentType": "json"
        }
    }
    response = requests.post(endpoint, json=payload)
    return response.json() if response.status_code == 200 else None


def webhook_limesurvey(resposta):
    """Exemplo de processamento de webhook do LimeSurvey."""
    participante_id = resposta.get("participante_id")
    pesquisa_id = resposta.get("pesquisa_id")
    resposta_texto = resposta.get("resposta")

    # Envia resposta para o endpoint de registro
    response = requests.post(
        "http://127.0.0.1:5000/respostas",
        json={
            "participante_id": participante_id,
            "pesquisa_id": pesquisa_id,
            "resposta": resposta_texto
        }
    )
    return response.status_code