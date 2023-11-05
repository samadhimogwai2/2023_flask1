from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
# initialize the app with the extension
db = SQLAlchemy(app)

# db.Modelを継承してテーブルを定義
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # 全てのデータを取得
        posts = Post.query.all()

        return(render_template('index.html', posts=posts))

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        # DBに登録
        post = Post(title=title, body=body)

        db.session.add(post)
        db.session.commit()

        return redirect('/')

    else:    
        return(render_template('create.html'))
    
@app.route('/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    # データを取得
    post = Post.query.get(id)
    
    if request.method == 'GET':
        return(render_template('update.html', post=post))
    else:    
        post.title = request.form.get('title')
        post.body = request.form.get('body')

        # DBに反映
        db.session.commit()

        return redirect('/')

@app.route('/<int:id>/delete', methods=['GET'])
def delete(id):
    # データを取得
    post = Post.query.get(id)
    
    # データを削除
    db.session.delete(post)
    
    # DBに反映
    db.session.commit()

    return redirect('/')   