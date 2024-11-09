#
# Importar as bibliotecas necessárias
from flask import Flask, redirect, send_file, request, render_template, session

from flask_session import Session
from flask_mail import Mail, Message

import logging
import json
import re

vatRegEx = "^[\d]{9}$"
passwordRegEx = "^[\w]{3,7}$"
emailRegEx = "^([a-z0-9_\.\-])+\@(([a-z0-9\-])+\.)+([a-z0-9]{2,4})$/i"
  
"""
    Note: Everytime we want to write a special character we use \ before so it knows is that character we want and not an operation
    "/" -> Start of regular expression 
    ^ -> initates the start of the string 
    "([a-z0-9_\.\-])" -> Any combination from a-z, 0-9, '_', '.', '-', and we add a + at the end to indicate there can be more than 1 character
    "\@" -> Following must be an @
    "(([a-z0-9\-])+\.)+" -> Any combination from a-z, 0-9, '-', plus a dot at the end
    "([a-z0-9]{2,4})" -> This is the domain part which only has a-z, 0-9 and between 2 and 4 characters long
    "$" -> Symbolizes the end of the string
    "/" -> End of regular expression
    "i" -> is a flag to tell the filter not to be case sensitive
"""

#
# Flask application object (app) no contexto do módulo Python currente
#
app = Flask(__name__)
app.url_map.strict_slashes = False

app.config[ 'TEMPLATES_AUTO_RELOAD' ] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.config[ 'MAIL_SERVER' ]= 'smtp.gmail.com'
app.config[ 'MAIL_PORT' ] = 465
app.config[ 'MAIL_USERNAME' ] = 'pereiramiguelsr222@gmail.com'
app.config[ 'MAIL_PASSWORD' ] = 'fuxmnqndwpuqxoos'
app.config[ 'MAIL_USE_TLS' ] = False
app.config[ 'MAIL_USE_SSL' ] = True

Session(app)
mail = Mail(app)

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


@app.route('/formLogin')
def buildFormLogin():
	logging.debug( f"Route /buildFormLogin called..." )

	return render_template( 'formLoginT.html', vatRegEx=vatRegEx, passwordRegEx=passwordRegEx )

@app.route('/doLogin', methods=(['POST']) )
def doLogin():
	logging.debug( f"Route /doLogin called..." )

	nif = request.form[ 'vatName' ]
	logging.debug( f"NIF recebido: {nif}" )

	password = request.form[ 'passwordName' ]
	logging.debug( f"Password recebida: {password}" )

	nifCheck = re.search( vatRegEx, nif)
	logging.debug( f"Check NIF: {nifCheck}" )

	passworCheck = re.search( passwordRegEx, password)
	logging.debug( f"Check password: {passworCheck}" )

	if (nifCheck==False or passworCheck==False):
		return render_template( 'dadosInvalidosT.html', errorMessage="Formato dos dados inválido", redirectURL=request.referrer )

	session[ 'NIF'] = nif

	return buildFormProfile()

@app.route('/formProfile')
def buildFormProfile():
	logging.debug( f"Route /buildFormProfile called..." )

	if not session.get( "NIF" ):
		return buildFormLogin()

	districts = loadData( './private/cp-districts.json' )

	return render_template( 'formProfileT.html', districts=districts )

@app.route('/doProfile', methods=(['POST']) )
def doProfile():
	logging.debug( f"Route /doProfile called..." )

	return buildFormProfile()

@app.route("/doLogout")
def doLogout():
	logging.debug( f"Route /doLogout called..." )

	session[ 'NIF' ] = None
	
	return redirect( "/" )

@app.route('/doSendEmail')
def doSendEmail():
	logging.debug( f"Route /doSendEmail called..." )

	_subject = 'Hello from the other side!'
	_senderName = 'Pg Web Semester 24/25'
	_senderEmail = 'pereiramiguelsr222@gmail.com'  
	_recipientEmail = 'pereiramiguelsr222@gmail.com'

	_msgContent = "Sending an e-mail from a Flask app."
	
	msg = Message( 
		subject=_subject, 
		sender=(_senderName, _senderEmail), 
		recipients=[ _recipientEmail ] )

	msg.body = _msgContent

	mail.send( msg )

	return "Message sent!"

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

@app.route('/createProfile')
def createProfile():
	logging.debug( f"Route /createProfile called..." )
	return render_template( 'formRegisterT.html', vatRegEx=vatRegEx, passwordRegEx=passwordRegEx, emailRegEx=emailRegEx )

	
@app.route('/doRegister', methods=(['POST']) )
def	doRegister():
	logging.debug(  f"Route /doRegister called...")

	try:
		logging.debug( f"NIF = {request.form['vatName']}")
		logging.debug( f"email = {request.form['emailName']}")
		logging.debug( f"password = {request.form['passwordName']}")
	except Exception as e:
		logging.debug( f"Error: ${e}")

	return redirect( "/static/index.html", code=302 )
