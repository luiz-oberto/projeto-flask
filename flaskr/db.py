import sqlite3
import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# adicionando a função python que vai rodar os comandos SQL que criamos no arquivo schema.sql
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """limpa os dados existentes e cria novas tabelas"""
    init_db()
    click.echo('Initialized the database')


# Register with the Application
# as funções close_db e init_db_command precisam estar registradas com a instancia da aplicação
# se não elas não seram usadas pela aplicação

def init_app(app):
    # fala para o flask chamar esta função qao limpar após retornar essa reposta
    app.teardown_appcontext(close_db)
    # adiciona um novo comando que pode ser chamado utilizando o 'flask command'
    app.cli.add_command(init_db_command)