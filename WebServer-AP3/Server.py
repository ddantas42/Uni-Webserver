#
# Importar as bibliotecas necessárias
from flask import Flask, redirect, send_file, request, render_template

import os

import logging
import json

#
# Flask application object (app) no contexto do módulo Python currente
#
app = Flask(__name__)
app.url_map.strict_slashes = False

app.config[ 'TEMPLATES_AUTO_RELOAD' ] = True
app.config[ 'UPLOAD_FOLDER' ] = "./static/images"

#
# Ativar o nível de log para debug
#
logging.basicConfig( level=logging.DEBUG )

#1
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

@app.route('/turma', methods=(['GET']))
def renderTurma():
	logging.debug( f"Route /turma called..." )

	# Ler a "base de dados" de utilizadores de um ficheiro
	db = loadData( './private/dados.json' )

	turma = db[ 'grupos' ]

	return render_template( 'turmaT.html', turma=turma )

@app.route('/grupo', methods=(['GET']) )
def renderGrupo():
    logging.debug( f"Route /grupo called..." )

    groupID = int ( request.args[ 'gID' ] )

    # Ler a "base de dados" de utilizadores de um ficheiro
    db = loadData( './private/dados.json' )

    group = db[ 'grupos' ][ groupID ]

    return render_template( 'grupoT.html', group=group )

#
# Rota para processar o formulário de adição de um aluno
#
@app.route('/addAluno', methods=(['POST']) )
def renderAddAluno():
    logging.debug( f"Route /addAluno called..." )

    if 'imageProfile' not in request.files:
        logging.debug( "No file part!" )
        return render_template( 'dadosInvalidosT.html', errorMessage="No file part!", redirectURL=request.referrer )
    
    file = request.files[ 'imageProfile' ]

    # If the user does not select a file, the browser submits an
    # empty file without a filename.

    if file.filename == '':
        logging.debug( "No selected file!" )
        return render_template( 'dadosInvalidosT.html', errorMessage="No selected file!", redirectURL=request.referrer )

    filename = file.filename

    file.save( os.path.join( app.config['UPLOAD_FOLDER'], filename) )

        # "numero": 7851,
        # "nome": "Isabel",
        # "sobrenome": "Oliveira",
        # "telefone": "+351 912494415",
        # "email": "isabel.oliveira@outlook.com",
        # "foto_perfil": "7851.jpeg"

    return redirect( "/static/index.html", code=302 )

def group_already_exists(db, group_name):
	return any(group['designacao'] == group_name for group in db['grupos'])

@app.route('/addGrupo', methods=(['POST']) )
def renderAddGrupo():
    logging.debug(f"Route /addGrupo called...")
    logging.debug(f'Form data: {request.form}')

    group_name = request.form['Group_Name']
    db = loadData('./private/dados.json')  # Corrected 'db' usage here

    if group_already_exists(db, group_name):  # Corrected function name
        return render_template('dadosInvalidosT.html', errorMessage="Group already exists", redirectURL=request.referrer)
    else:
        new_group = {
            "designacao": group_name,
            "alunos": []
        }
        db['grupos'].append(new_group)

        # Save the updated data to the JSON file
        saveData('./private/dados.json', db)  # Save the updated db

    return redirect("/static/index.html", code=302)
