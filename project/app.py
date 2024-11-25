from flask import Flask, request, jsonify
from database import Session, Participante, Resposta
from limesurvey import get_respostas
from whatsapp import enviar_mensagem

app = Flask(__name__)

# Banco de dados
session = Session()

@app.route("/validar", methods=["POST"])
def validar_participante():
    """Valida o CPF e registra o participante."""
    data = request.json
    cpf = data.get("cpf")
    participante = session.query(Participante).filter_by(cpf=cpf).first()

    if participante:
        return jsonify({"erro": "CPF já registrado!"}), 400

    novo_participante = Participante(nome=data["nome"], cpf=cpf, email=data["email"])
    session.add(novo_participante)
    session.commit()

    return jsonify({"mensagem": "Participante registrado com sucesso!"})

@app.route("/receber_respostas", methods=["POST"])
def receber_respostas():
    """Recebe e armazena respostas de uma pesquisa."""
    pesquisa_id = request.json.get("pesquisa_id")
    respostas = get_respostas(pesquisa_id)

    for resposta in respostas:
        participante = session.query(Participante).filter_by(cpf=resposta["cpf"]).first()
        if participante:
            nova_resposta = Resposta(
                participante_id=participante.id,
                pesquisa_id=pesquisa_id,
                resposta=str(resposta)
            )
            session.add(nova_resposta)

    session.commit()
    return jsonify({"mensagem": "Respostas salvas com sucesso!"})

@app.route("/enviar_whatsapp", methods=["POST"])
def enviar_whatsapp():
    """Envia mensagem no WhatsApp após registro."""
    data = request.json
    numero = data.get("numero")
    mensagem = f"Olá {data.get('nome')}, obrigado por participar! Vamos agendar o encontro."
    enviar_mensagem(numero, mensagem)
    return jsonify({"mensagem": "Mensagem enviada com sucesso!"})

if __name__ == "__main__":
    app.run(debug=True)
