from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# CORS設定の見直し
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# SQLite データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thanks_images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 画像保存ディレクトリ設定
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads/thanks')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# データベースのモデル
class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(100), nullable=False)
    main_image_path = db.Column(db.String(255), nullable=True)
    sub_image_paths = db.Column(db.PickleType, nullable=True)
    tags = db.Column(db.PickleType, nullable=True)
    comments = db.Column(db.Text, nullable=True)

# アプリケーションコンテキスト内でデータベースを初期化
with app.app_context():
    db.create_all()

# 新規登録エンドポイント
@app.route('/images', methods=['POST'])
def add_image():
    data = request.form
    author_name = data['author_name']
    tags = data.getlist('tags')
    comments = data['comments']

    # メイン画像の保存
    main_image = request.files['main_image']
    main_image_filename = secure_filename(main_image.filename)
    main_image_path = os.path.join(app.config['UPLOAD_FOLDER'], main_image_filename)
    main_image.save(main_image_path)

    # サブ画像の保存
    sub_image_paths = []
    for sub_image in request.files.getlist('sub_images'):
        sub_image_filename = secure_filename(sub_image.filename)
        sub_image_path = os.path.join(app.config['UPLOAD_FOLDER'], sub_image_filename)
        sub_image.save(sub_image_path)
        sub_image_paths.append(sub_image_filename)

    new_image = ImageData(
        author_name=author_name,
        main_image_path=main_image_filename,
        sub_image_paths=sub_image_paths,
        tags=tags,
        comments=comments
    )
    db.session.add(new_image)
    db.session.commit()
    return jsonify({"message": "Image added successfully"}), 201

# 画像の取得エンドポイント
@app.route('/images', methods=['GET'])
def get_images():
    images = ImageData.query.all()
    result = []
    for image in images:
        image_data = {
            'id': image.id,
            'author_name': image.author_name,
            'main_image_path': f"/img/thanks/{image.main_image_path}",
            'sub_image_paths': [f"/img/thanks/{path}" for path in image.sub_image_paths],
            'tags': image.tags,
            'comments': image.comments,
        }
        result.append(image_data)
    return jsonify(result), 200

# 個別ページのエンドポイント
@app.route('/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = ImageData.query.get_or_404(image_id)
    image_data = {
        'id': image.id,
        'author_name': image.author_name,
        'main_image_path': f"/img/thanks/{image.main_image_path}",
        'sub_image_paths': [f"/img/thanks/{path}" for path in image.sub_image_paths],
        'tags': image.tags,
        'comments': image.comments,
    }
    return jsonify(image_data), 200

# OPTIONSリクエストの処理
@app.route('/images', methods=['OPTIONS'])
def images_options():
    response = jsonify({"message": "CORS preflight"})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)