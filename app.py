import os
import pathlib

import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = Flask("Google Login App")
app.secret_key = "Adicionar o client_secret aqui"  # Certifique-se de que isso coincide com o que está no client_secret.json

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Permitir tráfego HTTP para desenvolvimento local

GOOGLE_CLIENT_ID = "Adicionar o client_id aqui"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost/callback"
)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Autorização necessária
        else:
            return function()

    return wrapper

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)  # Redireciona o usuário para a página de autorização do Google

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # Estado não coincide!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")  # Armazena o ID do usuário Google na sessão
    session["name"] = id_info.get("name")  # Armazena o nome do usuário na sessão
    return redirect("/protected_area")

@app.route("/logout")
def logout():
    session.clear()  # Limpa a sessão do usuário
    return redirect("/")

@app.route("/")
def index():
    return "Hello World <a href='/login'><button>Login</button></a>"  # Página inicial com link para login

@app.route("/protected_area")
@login_is_required
def protected_area():
    return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"  # Área protegida, acessível apenas após login

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)  # Inicia o servidor Flask
