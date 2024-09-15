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

# データベースモデル
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(100), unique=True, nullable=False)
    sns_urls = db.Column(db.PickleType, nullable=True)  # SNSのURLリスト

    # 画像とのリレーションシップ
    images = db.relationship('ImageData', backref='author', lazy=True)

class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    main_image_path = db.Column(db.String(255), nullable=True)
    main_image_has_background = db.Column(db.Boolean, nullable=False, default=False)
    sub_image_paths = db.Column(db.PickleType, nullable=True)
    tags = db.Column(db.PickleType, nullable=True)
    comments = db.Column(db.Text, nullable=True)

# アプリケーションコンテキスト内でデータベースを初期化
with app.app_context():
    db.create_all()

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

# すべての著者を取得するエンドポイント
@app.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    result = []
    for author in authors:
        author_data = {
            'id': author.id,
            'author_name': author.author_name,
            'sns_urls': author.sns_urls
        }
        result.append(author_data)
    return jsonify(result), 200

# 新規登録エンドポイント
@app.route('/images', methods=['POST'])
def add_image():
    data = request.form

    author_id = data.get('author_id')
    if author_id and author_id.isdigit():
        author = Author.query.get_or_404(int(author_id))  # 数字であることを確認してからintにキャスト
    elif 'new_author_name' in data:
        sns_urls = []
        for key in data:
            if key.startswith('new_author_sns_urls'):
                sns_urls.append(data[key])

        new_author = Author(
            author_name=data['new_author_name'],
            sns_urls=sns_urls
        )
        db.session.add(new_author)
        db.session.commit()
        author = new_author  # 新規登録された著者をauthorに割り当て
    else:
        return jsonify({"message": "author_id or new_author_name is required"}), 400

    # タグの処理：カンマで分割し、空白を除去してリストに変換
    tags = data.get('tags', '')
    tags_list = [tag.strip() for tag in tags.split(',')] if tags else []

    comments = data['comments']

    # メイン画像の保存
    main_image = request.files.get('main_image')  # .get()を使用してファイルが存在しない場合にNoneを返す
    if main_image:
        main_image_filename = secure_filename(main_image.filename)
        main_image_path = os.path.join(app.config['UPLOAD_FOLDER'], main_image_filename)
        main_image.save(main_image_path)
        main_image_has_background = request.form.get('main_image_has_background', 'false').lower() == 'true'
    else:
        return jsonify({"message": "Main image is required"}), 400  # メイン画像がない場合エラーメッセージを返す

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
        author_id=author.id,
        main_image_path=main_image_filename,
        main_image_has_background=main_image_has_background,
        sub_image_paths=sub_image_paths,
        tags=tags_list,
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
    author_id = data.get('author_id')
    if author_id:
        author = Author.query.get_or_404(author_id)
        image.author_id = author.id

    # タグの更新：カンマ区切りの文字列をリストに変換
    tags = data.get('tags', '')
    image.tags = [tag.strip() for tag in tags.split(',')] if tags else image.tags

    # コメントの更新
    image.comments = data.get('comments', image.comments)

    # メイン画像の背景情報の更新
    image.main_image_has_background = request.form.get('main_image_has_background', 'false').lower() == 'true'

    # メイン画像の更新（必要な場合）
    if 'main_image' in request.files:
        main_image = request.files.get('main_image')
        if main_image:
            main_image_filename = secure_filename(main_image.filename)
            main_image_path = os.path.join(app.config['UPLOAD_FOLDER'], main_image_filename)
            try:
                main_image.save(main_image_path)
                print(f"Image saved to {main_image_path}")
                image.main_image_path = main_image_filename  # 更新
            except Exception as e:
                print(f"Error saving image: {str(e)}")
                return jsonify({"message": "Failed to save image", "error": str(e)}), 500

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
            'author': {
                'id': image.author.id,
                'author_name': image.author.author_name,
                'sns_urls': image.author.sns_urls
            },
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
        'author_name': image.author.author_name,
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
# @app.route('/images', methods=['OPTIONS'])
# @app.route('/authors', methods=['OPTIONS'])
# def handle_options():
#     response = jsonify({"message": "CORS preflight"})
#     response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
#     response.headers.add("Access-Control-Allow-Methods", "POST, GET, PUT, DELETE, OPTIONS")
#     response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
#     return response, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)