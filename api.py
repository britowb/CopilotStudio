from flask import Flask, jsonify, request, current_app
import os
import requests
from dotenv import load_dotenv
#from flask import Resource, Api, reqreparse, fields, marshal_with, abort


#Carregar as var de ambiente
load_dotenv()

#Variáveis de ambiente abstraídas para app.config que é nossa API
app = Flask(__name__)
app.config['CLIENT_ID'] = os.getenv('CLIENT_ID')
app.config['CLIENT_SECRET'] = os.getenv('CLIENT_SECRET')
app.config['TENANT_ID'] = os.getenv('TENANT_ID')
app.config['ORG_URL'] = os.getenv('ORG_URL')

######### Função para obter Token de acesso do Azure AD usando os valores do app.config #########
def get_access_token():
    ########## recuperando valores ##########
    tenant_id = current_app.config['TENANT_ID']
    client_id = current_app.config['CLIENT_ID']
    client_secret = current_app.config['CLIENT_SECRET']
    org_url = current_app.config['ORG_URL']

    ###### Montando URL para o Token (O formato é padrão) ######
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    scope = f'{org_url}/.default' ########## PREPARAR dados que serão enviados via POST para o endpoint do token ##########
    data = {
        'client_id':client_id,
        'client_secret':client_secret,
        'grant_type':'client_credentials',
        'scope':scope
        }
    
    ###### o fluxo OAuth2 segue uma especificação internacional (um padrão) que define tanto os nomes quanto os valores dos parâmetros em inglês.
    # Isso significa que o endpoint de token da Microsoft – e serviços que implementam OAuth2 – espera que o parâmetro seja exatamente chamado "grant_type" e que o valor para o fluxo de credenciais seja "client_credentials" ######

    response = requests.post(token_url, data=data) ########## REQUISIÇÃO 
    if response.status_code == 200: #código 200 é requisição bem-sucedida
        return response.json()["access_token"] #Retorna o token extraído da resposta JSON
    else:
        raise Exception(f'Erro ao obter token')

######### FUNÇÃO AUXILIAR PARA MONTAR CABEÇALHOS DE REQUISIÇÃO #########
def get_headers(token): #transforma o token em um conjunto de instruções para ser enviado junto das requisições que vamos fazer.
    return{
        "Authorization":f'Bearer {token}', # Bearer Token - formatação indicando que eu estou autorizado a acessar x recurso. É necessário o espaço.
        "Accept":"aplication/json", #Informo esperar resposta em json
        "Content-type":"application/json" #Tipo de dado enviado ( em formato json)
    }

########## get_headers é um cabeçalho que se não for modularizado se repete por todas requisições. ##########



@app.route('/')
def home():
   return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True)
