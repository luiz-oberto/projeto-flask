# Aqui no Init vai conter a Fábrica de aplicação (application factory) 
# e que o diretório flaskr será tratado como um pacote
import os
from flask import Flask

# Create_app é a funcão de fábrica de aplicações
def create_app(test_config=None):
    # cria e configura o app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
    )

    if test_config is None:
        # carrega a instancia config, se ela existir, quando não testado
        app.config.from_pyfile('config.py', silent=True)
    else:
        # carrega o test config se passar
        app.config.from_mapping(test_config)

    # garantir que o arquivo exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # uma página simples que diga olá
    @app.route('/hello/')
    def hello():
        return 'Hello, Word!'
    
    # importando e chamando a função da fábrica
    from . import db
    db.init_app(app)
    # agora inicializamos o arquivo de banco de dados utilizando o seguinte comando:
    # flask --app flaskr init-db

    # importando e registrando o blueprint de auth.py
    from . import auth
    app.register_blueprint(auth.bp)
    
    return app
