# coding=utf-8

__author__ = 'Jay'
# imports
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# grabs the folder where the script runs
from UserORM import UserORMHelper, Users
from User_Role import UserRoleORMHelper, User_Role
from Role import RoleORMHelper, Role
from ArticleORM import ArticleORMHelper,Article

basedir = os.path.abspath(os.path.dirname(__file__))

# configuration
DATABASE = 'role.db'

DEBUG = True
SECRET_KEY = 'my_precious'
USERNAME = 'admin'
PASSWORD = 'admin'

# defines the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

# create app
app = Flask(__name__)
app.config.from_object(__name__)
# db = SQLAlchemy(app)
User_helper = UserORMHelper(DATABASE)
User_helper.create_db()
User_Role_helper = UserRoleORMHelper(DATABASE)
User_Role_helper.create_db()
Role_helper = RoleORMHelper(DATABASE)
Role_helper.create_db()
Article_helper=ArticleORMHelper(DATABASE)
Article_helper.create_db()



@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    # 注册
    user_name = request.form['username']
    pass_word = request.form['password']
    role_Id = request.form['roleId']
    user = Users(user_name, pass_word)
    isSuccess = User_helper.addUser(user)
    user = User_helper.query_first_name_password(user)
    if isSuccess:
       addUserRoleSuccess=User_Role_helper.addUserRole(User_Role(user.id, int(role_Id)))
       if  addUserRoleSuccess:
           return render_template('signUpSuccess.html')
       else:
           return render_template('signUpLose.html')
    else:
        return render_template('signUpLose.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录."""
    user_name = request.form['username']
    pass_word = request.form['password']
    user = Users(user_name, pass_word)
    loginUser = User_helper.query_first_name_password(user)

    user_Role = User_Role_helper.query_first_userId(loginUser.id if loginUser else None)
    rId=int(user_Role.roleId if user_Role else "404")
    role = Role_helper.queryRoleByRoleId(rId)
    session['user_id']=user_name
    session[user_name + 'Role'] = role.function if role else "None"
    sessions = session[user_name + 'Role']
    if sessions == "CRUD":
        return render_template('loginSuccess.html')
    elif sessions == "CR":
        return render_template('loginSuccess.html')
    elif sessions == "R":
        return render_template('loginSuccess.html')
    elif sessions == "None":
        return render_template('loginFail.html')

@app.route('/Change', methods=['GET', 'POST'])
def Change():
    # 修改密码
    user_name = request.form['username']
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    userss = Users(user_name, old_password)
    users=Users(user_name, new_password)
    user = User_helper.query_first_name_password(userss)
    if user>0 :
        users=User_helper.update_user_extra_by_user_name(users)
        if users>0:
            return render_template('changeSuccess.html')
        else:
            return render_template('changeFail.html')
    else:
        return render_template('changeFail.html')


@app.route('/addArticle', methods=['GET', 'POST'])
def addArticle():
    """User logout/authentication/session management."""

    title=request.form['title']
    text=request.form['text']
    article=Article(title,text)

    isSucess=Article_helper.addArticle(article)


    articleList=Article_helper.query_all_articles()
    print len(articleList)
    if (isSucess and len(articleList) > 0):

        return render_template('addArticleSuccess.html',entries=articleList)



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """注销."""
    session.clear()
    flash('You were logged out')
    return redirect(url_for('index'))




@app.route('/', methods=['GET', 'POST'])
def index():
    """Searches the database for entries, then displays them."""
    return render_template('login_idx.html')


@app.route('/login_idx', methods=['GET', 'POST'])
def login_idx():
    """Searches the database for entries, then displays them."""
    return render_template('login_idx.html')


@app.route('/signUp_idx', methods=['GET', 'POST'])
def signUp_idx():
    """Searches the database for entries, then displays them."""
    return render_template('user_sign_up_idx.html')


@app.route('/signUp_Success', methods=['GET', 'POST'])
def signUp_Success():
    """Searches the database for entries, then displays them."""
    return render_template('Success.html')

@app.route('/password_change', methods=['GET', 'POST'])
def password_change():
    """Searches the database for entries, then displays them."""
    return render_template('change_password.html')


if __name__ == '__main__':
    app.run()
