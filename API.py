#Bibliotecas para Interface
import ttkbootstrap as ttk
from ttkbootstrap.widgets import DateEntry
from ttkbootstrap.constants import *
from ttkbootstrap.icons import Emoji
from tkinter import messagebox
from datetime import datetime
from ttkbootstrap import Window
#Bibliotecas para API
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Configuração da API google sheets/google drive
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SPREADSHEET_NAME = "Projeto"

#Credenciais, o correto é via arquivo json porem utilizaremos assim para instalar apenas o executavel do projeto na maquina dos vendedores
GOOGLE_SHEETS_CREDENTIALS = {
  "type": "service_account",
  "project_id": "projeto-esamc",
  "private_key_id": "7a6443800c73cd35be60edb9bbfcedc48d48528d",
  "private_key": "-----BEGIN PRIVATE KEY-----\n", #Chave secreta está excluida pois o projeto está publico no git, e o git bloqueia o envio
  "client_email": "projeto-esamc@projeto-esamc.iam.gserviceaccount.com",
  "client_id": "115276368391780217584",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/projeto-esamc%40projeto-esamc.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

credenciais = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_SHEETS_CREDENTIALS, SCOPE)
cliente = gspread.authorize(credenciais)