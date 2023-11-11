from enum import unique
from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_bootstrap import BOOTSTRAP_VERSION, Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import pytz
from form import Form
from blogform import BlogForm

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SECRET_KEY"] = os.urandom(24)
# initialize the app with the extension
db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)


# db.Modelを継承してテーブルを定義
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(12))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
@login_required  #ログインしているユーザのみアクセス可能
def index():
    if request.method == 'GET':
        # 全てのデータを取得
        posts = Post.query.all()

        return(render_template('index.html', posts=posts))
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    
    form = Form()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            username = request.form.get('username')
            password = request.form.get('password')
            
            user = User.query.filter_by(username=username).first()
            if user != None :
                return render_template('signup.html', form=form, message='入力したユーザ名は既に存在します')            

            user = User(username=username, password=generate_password_hash(password))

            db.session.add(user)
            db.session.commit()
            return redirect('/login')
        else:
            return render_template('signup.html', form=form, message='')    
        
    else:
        return render_template('signup.html', form=form, message='')
    
@app.route('/login', methods=['GET', 'POST'])
def login():

    form = Form()
       
    if request.method == 'POST':
        
        # 入力チェックOK
        if form.validate_on_submit():
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()
            if user == None :
                return render_template('login.html', form=form, message='入力したユーザ名は存在しません')
            
            # パスワードチェック
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect('/')
            else:
                return render_template('login.html', form=form, pswerr='パスワードが相違しています')
            
        # 入力チェックNG            
        else:
            return render_template('login.html', form=form, message='',pswerr='')
                
    else:
        return render_template('login.html', form=form, message='',pswerr='')

@app.route('/logout')
@login_required  #ログインしているユーザのみアクセス可能
def logout():
     logout_user()
     return redirect('/login')

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    
    blogform = BlogForm()
    
    if request.method == 'POST':
        if 'regist' in request.form:
                        
            if blogform.validate_on_submit():
                
                title = request.form.get('title')
                containt = request.form.get('containt')
     
                # DBに登録
                post = Post(title=title, body=containt)
                db.session.add(post)
                db.session.commit()

                return redirect('/')
            
            else:
                return(render_template('create.html',form=blogform))
        
        elif 'back' in request.form:
              return redirect('/')  
        else:
            return(render_template('create.html',form=blogform))

    else:
        return(render_template('create.html',form=blogform))
    
@app.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required  #ログインしているユーザのみアクセス可能
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
@login_required  #ログインしているユーザのみアクセス可能
def delete(id):
    # データを取得
    post = Post.query.get(id)
    
    # データを削除
    db.session.delete(post)
    
    # DBに反映
    db.session.commit()

    return redirect('/')   