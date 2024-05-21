from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import request
from flask import render_template

app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Oi CDFs!"

# if __name__ == "__main__":
#     app.run()

# flask --app hello.py run --> roda a aplicação ou só aperte o botão run no canto suparior direito do VScode


# HTML Escape
# @app.route("/<name>")
# def escaping(name):
#     return f"Hello, {escape(name)}"
''' 
utilize o ip fornecido e acrescente ao final /(seu nome) para ver a execução deste bloco de código
ele vai pegar o nome fornecido na HTML e vai retornar uma string na tela com o nome passado
'''

# Routing (rotas)
@app.route('/')
def index():
    return 'Index'

# @app.route('/hello')
# def hello():
#     return 'Hello, word!'


# Variable rules
# @app.route('/user/<username>')
# def show_user_profile(username):
#     # mostra o perfil de usário para este usuário
#     return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'subpath {escape(subpath)}'


# |Unique URLs / redirection behavior

@app.route('/projects/')
def projects():
    return 'The project page'
'''Aqui, se eu acessar a URL '/projects/' sem a barra no final '/projects', eu serei redirecionado para a página '/projects/'
automaticamente''' 

@app.route('/about')
def about():
    return 'the about page'
'''Já aqui nesta situação, se eu tentar acessar a URL /about/ receberei um erro 404 pois esta URL não existe, 
o que a torna úica'''

# URL building
# @app.route('/login')
# def login():
#     return 'login'

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

with app.test_request_context():
    print(url_for('index'))
    # print(url_for('login'))
    # print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))


# HTTP Methods
# import request
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return 'do_the_login()'
#     else:
#         return 'show_the_login_form()'

# @app.get('/login')
# def login_get():
#     return show_the_login_form()

# @app.post('/login')
# def login_post():
#     return do_the_login()


# Static FIles
with app.test_request_context():
    url_for('static', filename='style.css')

# rendering templates
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


# Accessing Request Data
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


# File Uploads
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')


# Cookies
# reading cookies
@app.route('/')
def index():
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.

# storing cookies
from flask import make_response

@app.route('/')
def index():
    resp = make_response(render_template(...))
    resp.set_cookie('username', 'the username')
    return resp


# redirects and errors
from flask import abort, redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()

# decorar uma página de error
from flask import render_template

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
