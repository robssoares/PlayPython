from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave-secreta'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp'}

# Banco de dados
def init_db():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS imagens (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome_sanscrito TEXT NOT NULL,
                        nome_portugues TEXT NOT NULL,
                        categoria1 INTEGER NOT NULL,
                        categoria2 INTEGER NOT NULL,
                        imagem TEXT NOT NULL)''')
        conn.commit()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome_sanscrito = request.form.get('nome_sanscrito')
        nome_portugues = request.form.get('nome_portugues')
        categoria1 = request.form.get('categoria1')
        categoria2 = request.form.get('categoria2')
        imagem = request.files.get('imagem')

        if not all([nome_sanscrito, nome_portugues, categoria1, categoria2, imagem]):
            flash("Todos os campos são obrigatórios.")
            return redirect(request.url)

        if not allowed_file(imagem.filename):
            flash("Formato de imagem inválido.")
            return redirect(request.url)

        filename = secure_filename(imagem.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        imagem.save(image_path)

        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO imagens (nome_sanscrito, nome_portugues, categoria1, categoria2, imagem) VALUES (?, ?, ?, ?, ?)",
                      (nome_sanscrito, nome_portugues, categoria1, categoria2, filename))
            conn.commit()

        flash("Imagem cadastrada com sucesso!")
        return redirect(url_for('index'))

    # Consulta as imagens cadastradas
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("SELECT nome_sanscrito, nome_portugues, imagem FROM imagens")
        imagens = c.fetchall()

    return render_template('index.html', imagens=imagens)

    
    
    
    
    
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs('static/uploads', exist_ok=True)
    init_db()
    app.run(debug=True)
