from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Jogo
from dao import JogoDao, UsuarioDao
import time, os
from jogoteca import db,app
from helpers import recupera_imagem, deleta_arquivo

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    lista = jogo_dao.listar()
    return render_template('listar.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # return redirect('/login?proxima=novo') #redireciona pra pagina de Login e depois de logado redireciona para pagina de novo
        #do jeito acima, esta usando o redirecionamento para rotas. Mudaremos para usar o methods, assim se a rota mudar não afeta nosso cód.
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo jogo')

#pegando os dados digitados na criação do jogo
#por padrão, qndo não passamos mais informações pra rota ela aceita apenas methods Get e estamos passando um Post. Temos q informar
#Qndo é uma lista, em Python por padrão coloca-se a vírgula no final
@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    #salvando no BD
    jogo = jogo_dao.salvar(jogo)

    arquivo = request.files['arquivo']
    #arquivo.save(f'uploads/{arquivo.filename}')
    upload_path = app.config['UPLOAD_PATH']
    # estamos usando a variavel timestamp, que contem a hora, minuto e segundo para add no nome da imagem, evitando que fiquem com o msm nome
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso')  # Msg q exibo no HTML
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado. Try again!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect (url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    #recuperar o jogo do banco pelo ID
    jogo = jogo_dao.busca_por_id(id)
    # recuperando o nome da imagem para usar no criar()
    nome_imagem = recupera_imagem(id)

    return render_template('editar.html', titulo='Editando jogo', jogo=jogo, capa_jogo = nome_imagem or 'capa_padrao.jpg')

@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console, id=request.form['id'])

    arquivo = request.files['arquivo'] #possivel erro
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    jogo_dao.salvar(jogo)

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    flash('O jogo foi removido com sucesso!')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

