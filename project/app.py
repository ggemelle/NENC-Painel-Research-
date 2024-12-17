from flask import Flask, render_template, request, redirect, flash, jsonify
from database import Session, Participante, LogAuditoria
from cryptography.fernet import Fernet
from validate_email_address import validate_email
import phonenumbers

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Para mensagens flash

# Banco de dados
session = Session()

# Chave de criptografia
CHAVE_CPF = Fernet.generate_key()
fernet = Fernet(CHAVE_CPF)

@app.route("/", methods=["GET"])
def home():
    """Exibe o formulário de cadastro."""
    return render_template("index.html")

@app.route("/validar", methods=["POST"])
def validar_participante():
    """Valida o CPF, e-mail, telefone e registra o participante."""
    nome = request.form.get("nome")
    cpf = request.form.get("cpf")
    email = request.form.get("email")
    telefone = request.form.get("telefone")
    consentimento = request.form.get("consentimento")

    # Consentimento
    if not consentimento:
        flash("É necessário consentir com os termos de privacidade (LGPD).", "danger")
        return redirect("/")

    # Validação de e-mail
    if not validate_email(email):
        flash("E-mail inválido.", "danger")
        return redirect("/")

    # Validação de telefone
    try:
        numero_formatado = phonenumbers.parse(telefone, "BR")
        if not phonenumbers.is_valid_number(numero_formatado):
            flash("Número de telefone inválido.", "danger")
            return redirect("/")
        telefone_formatado = phonenumbers.format_number(numero_formatado, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        flash("Número de telefone inválido.", "danger")
        return redirect("/")

    # Criptografar CPF
    cpf_criptografado = fernet.encrypt(cpf.encode())

    # Verificar se CPF existe
    participante = session.query(Participante).filter_by(cpf=cpf).first()
    if participante:
        flash("CPF já registrado!", "danger")
        return redirect("/")

    # Salvar no banco
    novo_participante = Participante(
        nome=nome,
        cpf=cpf,
        cpf_criptografado=cpf_criptografado,
        email=email,
        telefone=telefone_formatado,
        consentimento=1
    )
    session.add(novo_participante)
    session.commit()

    # Log de auditoria
    log = LogAuditoria(participante_id=novo_participante.id, acao="Registro de participante")
    session.add(log)
    session.commit()

    flash("Participante cadastrado com sucesso!", "success")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
