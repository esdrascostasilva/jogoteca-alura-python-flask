'''
Minha primeira aplicação Web utilizando Python e o MicroFramework Flask
Misturamos um pouco de HTML, CSS, Bootstrap, JQuery e MySQL
A aplicação trata-se de im website de Jogos de video game aonde se ocnsegue visulizar uma lista de jogos,
depois de logado vc consegue cadastrar um novo jogo, edita-lo, carregar uma imagem para esse jogo, deletar, ou seja, fazer um CRUD.
Very nice!

'''

from flask import Flask, redirect, flash, url_for, send_from_directory
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

#IMPORTANDO O ARQUIVO DE CONFIGURAÇÃO
app.config.from_pyfile('config.py')

#estanciando meu DB
db = MySQL(app)

from views import *

#Só sera executado se executar jogoteca.py, caso contrario ele não executa se for importado
if __name__ == '__main__':
    #Parametro 'debug=True' permite q eu não precise dar Rerun após toda modificação
    app.run(debug=True)


