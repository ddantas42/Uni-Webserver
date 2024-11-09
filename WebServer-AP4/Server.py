#
# Importar as bibliotecas necessárias
from flask import Flask, redirect, send_file, request, render_template

import logging
import json
import re

#
# Flask application object (app) no contexto do módulo Python currente
#
app = Flask(__name__)
app.url_map.strict_slashes = False

app.config[ 'TEMPLATES_AUTO_RELOAD' ] = True

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
# Função auxiliar para escrever dados JSON (em formato utf-8) num ficheiro
#
def saveData(fName, data):
    logging.debug( f"Saving data to {fName}..." )

    data_json = json.dumps( data, indent=4)

    with open( fName, "w", encoding='utf-8') as f:
        f.write( data_json )
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

@app.route('/formProfile')
def buildFormProfile():
    logging.debug( f"Route /buildFormProfile called..." )

    districts = loadData( './private/cp-districts.json' )

    return render_template( 'formProfile.html', districts=districts )

@app.route('/counties')
def getListOfCounties():
    logging.debug( f"Route /getListOfCounties called..." )

    districtID = request.args[ 'idDistrict' ]

    fileName = 'cp-county-' + districtID + ".json"

    try:
        return loadData( './private/' + fileName )
    except OSError as e:
        logging.debug( f"County ID ({districtID}) not found ..." )

        return { "concelhos" : [] }

@app.route('/postal')
def getListOfPostal():
    logging.debug( f"Route /getListOfPostal called..." )

    postal = request.args[ 'idPostal' ]

    fileName = 'cp-postal-' + postal + ".json"

    try:
        return loadData( './private/' + fileName )
    except OSError as e:
        logging.debug( f"County ID ({postal}) not found ..." )

        return { "postal" : [] }

@app.route('/doLogin', methods=(['POST']) )
def doLogin():
    logging.debug( f"Route /doLogin called..." )

    password_check = False
    name_check = False

    password_pattern = r'^[\w]{3,7}$'
    name_pattern = r'^[\w]{1,9}$'

    password = request.form['password']
    name = request.form['name']

    if re.fullmatch(password_pattern, password):
        logging.debug("Password format verified")
        password_check = True
    else:
        logging.debug("Password format failed to verify")

    if re.fullmatch(name_pattern, name):
        logging.debug("Username format verified")
        name_check = True
    else:
        logging.debug("Username format failed to verify")

    if password_check == True and name_check == True:
        return buildFormProfile()

    return redirect( "/static/index.html", code=302 )