from flask import Flask, request, jsonify
import os
import sqlite3
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Nuxt.jsからのリクエストを許可するためにCORSを設定します

DATABASE = 'blog.db'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# データベースに接続するヘルパー関数
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# データベースを初期化する関数
def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                image_path TEXT
            )
        ''')
        conn.commit()

# ファイルの拡張子が許可されているか確認する関数
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/posts', methods=['GET'])
def get_posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return jsonify([dict(post) for post in posts])

@app.route('/posts', methods=['POST'])
def create_post():
    title = request.form.get('title')
    content = request.form.get('content')
    image_path = None

    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not title or not content:
        return jsonify({'error': 'Title and content are required!'}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO posts (title, content, image_path) VALUES (?, ?, ?)',
                 (title, content, image_path))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Post created!'}), 201

@app.route('/upload-multiple', methods=['POST'])
def upload_multiple():
    if 'images' not in request.files:
        return jsonify({'error': 'No files provided!'}), 400

    files = request.files.getlist('images')
    saved_files = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            saved_files.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return jsonify({'message': 'Files uploaded!', 'files': saved_files}), 201

@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Post deleted!'}), 200

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    init_db()
    app.run(debug=True)