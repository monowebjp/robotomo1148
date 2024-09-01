from flask import Flask, request, jsonify, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

AUTHORIZATION_BASE_URL = 'https://id.twitch.tv/oauth2/authorize'
TOKEN_URL = 'https://id.twitch.tv/oauth2/token'
REDIRECT_URI = 'http://localhost:5000/callback'  # フロントエンドからリダイレクトされるURL

# ログイン
@app.route('/login')
def login():
    twitch_auth_url = (
        f"{AUTHORIZATION_BASE_URL}?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=user:read:email"
    )
    return redirect(twitch_auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    token_response = requests.post(TOKEN_URL, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    session['access_token'] = access_token

    return redirect('http://localhost:3000/dashboard')  # Nuxt3のフロントエンドにリダイレクト

@app.route('/userinfo')
def userinfo():
    access_token = session.get('access_token')
    if not access_token:
        return {'error': 'Unauthorized'}, 401

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-ID': CLIENT_ID
    }

    response = requests.get('https://api.twitch.tv/helix/users', headers=headers)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)

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
    main_image_has_background = db.Column(db.Boolean, nullable=False, default=False)
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

    main_image_has_background = request.form.get('main_image_has_background', 'false').lower() == 'true'

    # サブ画像の保存
    sub_image_paths = []
    for i, sub_image in enumerate(request.files.getlist('sub_images')):
        sub_image_filename = secure_filename(sub_image.filename)
        sub_image_path = os.path.join(app.config['UPLOAD_FOLDER'], sub_image_filename)
        sub_image.save(sub_image_path)

        has_background = request.form.get(f'sub_image_has_background_{i}', 'false').lower() == 'true'

        sub_image_paths.append({
            'filename': sub_image_filename,
            'has_background': has_background
        })

    new_image = ImageData(
        author_name=author_name,
        main_image_path=main_image_filename,
        main_image_has_background=main_image_has_background,
        sub_image_paths=sub_image_paths,
        tags=tags,
        comments=comments
    )
    db.session.add(new_image)
    db.session.commit()
    return jsonify({"message": "Image added successfully"}), 201

# 編集エンドポイント
@app.route('/images/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    image = ImageData.query.get_or_404(image_id)

    data = request.form
    image.author_name = data.get('author_name', image.author_name)
    image.tags = data.getlist('tags') if 'tags' in data else image.tags
    image.comments = data.get('comments', image.comments)
    image.main_image_has_background = request.form.get('main_image_has_background', 'false').lower() == 'true'

    # メイン画像の更新（必要な場合）
    if 'main_image' in request.files:
        main_image = request.files['main_image']
        main_image_filename = secure_filename(main_image.filename)
        main_image_path = os.path.join(app.config['UPLOAD_FOLDER'], main_image_filename)
        main_image.save(main_image_path)
        image.main_image_path = main_image_filename

    # サブ画像の更新（必要な場合）
    if 'sub_images' in request.files:
        sub_image_paths = []
        for i, sub_image in enumerate(request.files.getlist('sub_images')):
            sub_image_filename = secure_filename(sub_image.filename)
            sub_image_path = os.path.join(app.config['UPLOAD_FOLDER'], sub_image_filename)
            sub_image.save(sub_image_path)

            has_background = request.form.get(f'sub_image_has_background_{i}', 'false').lower() == 'true'

            sub_image_paths.append({
                'filename': sub_image_filename,
                'has_background': has_background
            })

        image.sub_image_paths = sub_image_paths

    db.session.commit()
    return jsonify({"message": "Image updated successfully"}), 200


#削除
@app.route('/images/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    image = ImageData.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
    return jsonify({"message": "Image deleted successfully"}), 200


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
            'main_image_has_background': image.main_image_has_background,
            'sub_image_paths': [{
                'filename': f"/img/thanks/{sub_image['filename']}",
                'has_background': sub_image['has_background']
            } for sub_image in image.sub_image_paths],
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
        'main_image_has_background': image.main_image_has_background,
        'sub_image_paths': [{
            'filename': f"/img/thanks/{sub_image['filename']}",
            'has_background': sub_image['has_background']
        } for sub_image in image.sub_image_paths],
        'tags': image.tags,
        'comments': image.comments,
    }
    return jsonify(image_data), 200

# OPTIONSリクエストの処理
@app.route('/images', methods=['OPTIONS'])
def images_options():
    response = jsonify({"message": "CORS preflight"})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Methods", "POST, GET, PUT, DELETE, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)