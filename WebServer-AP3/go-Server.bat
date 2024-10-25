@echo off

:: Configura a variável de ambiente para o app do Flask
set FLASK_APP=Server.py

:: Define o caminho do Flask
set FLASK_BIN=.env\Scripts\flask

:: Exibe mensagem e executa o servidor Flask diretamente
echo Iniciando o servidor...
%FLASK_BIN% run --port 80 --host="0.0.0.0"

:: Checa se o comando foi bem-sucedido
if %errorlevel% neq 0 (
    echo Houve um erro ao iniciar o servidor.
) else (
    start http://localhost
)

:: Mantém o terminal aberto
pause
