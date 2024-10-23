#
# Importar as bibliotecas necessárias
from flask import Flask, redirect, send_file, request, render_template

import logging
import json

#
# Flask application object (app) no contexto do módulo Python currente
#
app = Flask(__name__)
app.url_map.strict_slashes = False

#
# Ativar o nível de log para debug
#
logging.basicConfig( level=logging.DEBUG )

#
# Função auxiliar para ler dados JSON (em formato utf-8) de um ficheiro
#
def loadData(fName):
    logging.debug( f"Loading data from {fName}..." )

    with open( fName, encoding='utf-8') as f:
        data = json.load( f )
    f.close()

    return data

#
# Adicionar o tratamento das rotas / e /static e /static/
#
# Redirecionar para a página de index (/static/index.html)
#
@app.route('/')
@app.route('/static')
def getRoot():
    logging.debug( f"Route / called..." )
    return redirect( "/static/index.html", code=302 )

@app.route('/favicon.ico')
def getFavicon():
    logging.debug( f"Route /favicon.ico called..." )
    return send_file( "./static/favicon.ico", as_attachment=True, max_age=1 )