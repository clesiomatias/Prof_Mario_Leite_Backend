import datetime
import os
import sqlite3
from functools import wraps

import jwt
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY").encode("utf-8")
CORS(app)


# Função para verificar se o usuário está autenticado
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token de autenticação necessário!"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return jsonify({"message": "Token de autenticação inválido!"}), 401

        return f(*args, **kwargs)

    return decorated


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Verifica se as credenciais são válidas
    valid_users = {
        os.getenv("USUARIO1"): os.getenv("SENHA1"),
        os.getenv("USUARIO2"): os.getenv("SENHA2"),
        os.getenv("USUARIO3"): os.getenv("SENHA3"),
    }
    
    if username in valid_users and valid_users[username] == password:
        # Gera um token JWT com o username e uma expiração de 30 minutos
        token = jwt.encode(
            {
                "user": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            app.config["SECRET_KEY"],
        )
        return jsonify({"token": token})

    return jsonify({"message": "Falha na autenticação!"}), 401


# Rota protegida que requer autenticação JWT
@app.route("/protected")
@token_required
def protected():
    return jsonify({"message": "Rota protegida!"})


# Configurações do banco de dados
DB_FILE = 'database.db'
SCHEMA = """
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    uploader TEXT NOT NULL
);
"""

# Função para inicializar o banco de dados
def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute(SCHEMA)
    conn.commit()
    conn.close()

# Verifica se o banco de dados existe, se não, o inicializa
if not os.path.exists(DB_FILE):
    init_db()


# Função para fazer upload de arquivos
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]
    uploader = request.form["uploader"]

    if file.filename == "":
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    # Define o nome do arquivo usando o nome original do arquivo escolhido pelo usuário
    filename = secure_filename(file.filename)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM files WHERE uploader = ?", (uploader,))
    count = cursor.fetchone()[0]

    if count > 0:
        return jsonify({"error": "Você já fez upload de um arquivo"}), 400

    cursor.execute(
        "INSERT INTO files (filename, uploader) VALUES (?, ?)", (filename, uploader)
    )
    conn.commit()
    conn.close()

    # Salva o arquivo com o nome escolhido pelo usuário
    file.save(os.path.join("uploads", filename))

    return jsonify({"message": "Arquivo enviado com sucesso"}), 201


# Função para listar os arquivos disponíveis para download
@app.route('/files', methods=['GET'])
def list_files():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM files")
    files = cursor.fetchall()
    conn.close()

    file_list = [{'id': row[0], 'filename': row[1], 'uploader':row[2]} for row in files]
    return jsonify(file_list)

# Função para fazer o download de um arquivo específico
@app.route('/download/<int:file_id>', methods=['GET'])
def download_file(file_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM files WHERE id = ?", (file_id,))
    file_record = cursor.fetchone()
    conn.close()

    if file_record:
        filename = file_record[0]
        return send_file(os.path.join('uploads', filename), as_attachment=True)
    else:
        return jsonify({'error': 'Arquivo não encontrado'}), 404


@app.route("/delete/<int:file_id>", methods=["DELETE"])
def delete_file(file_id):
    # Primeiro, você precisa encontrar o nome do arquivo no banco de dados usando o ID
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM files WHERE id = ?", (file_id,))
    file_data = cursor.fetchone()
    conn.close()

    if file_data is None:
        return jsonify({"error": "Arquivo não encontrado"}), 404

    filename = file_data[0]

    # Em seguida, você precisa excluir o registro do banco de dados
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM files WHERE id = ?", (file_id,))
    conn.commit()
    conn.close()

    # Finalmente, você pode excluir o arquivo do sistema de arquivos
    try:
        os.remove(os.path.join("uploads", filename))
    except OSError as e:
        return (
            jsonify({"error": "Erro ao deletar o arquivo do sistema de arquivos"}),
            500,
        )

    return jsonify({"message": "Arquivo deletado com sucesso"}), 200


if __name__ == '__main__':
    app.run(debug=True)
