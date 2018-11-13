from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy
from config import DB_URL
from models import Member, Session, Thread, Profile, Message

# TODO 未加密密码字符串
# TODO 没有判断post请求错误的入参
# TODO 目前仅能用用户名登陆

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
db = SQLAlchemy(app)


@app.route("/")
def index():
    return "welcome to discuz!"


@app.route('/login', methods=['POST'])
def login():
    """
        post request body example:
        {
            "password": "12345678",
            "username": "pieworkplace"
        }
    """
    data = request.json
    query = db.session.query(Member)
    check = query.filter(Member.username.in_([data["username"]]), Member.password.in_([data["password"]])).first()
    if check:
        if db.session.query(Session).filter(Session.username.in_([check.username])).first():
            return "already logged in!"
        newSession = Session(username=check.username)
        db.session.add(newSession)
        db.session.commit()
        return "login success!"
    else:
        return "login fail!"


@app.route('/logout', methods=['POST'])
def logout():
    """
        post request body example:
        {
            "username": "pieworkplace"
        }
    """
    data = request.json
    sessionIn = db.session.query(Session).filter(Session.username.in_([data["username"]])).first()
    if sessionIn:
        db.session.delete(sessionIn)
        db.session.commit()
        return "logout done!"
    return "not logged in!"


@app.route('/register', methods=['POST'])
def register():
    """
        post request body example:
        {
            "password": "12345678",
            "username": "pieworkplace",
            "email": "pieworkplace@gmail.com"
        }
    """
    data = request.json
    query = db.session.query(Member)
    check1 = query.filter(Member.username.in_([data["username"]])).first()
    check2 = query.filter(Member.email.in_([data["email"]])).first()
    if check1 or check2:
        return 'user exists!'
    newMember = Member(username=data["username"], password=data["password"], email=data["email"])
    db.session.add(newMember)
    db.session.commit()
    return 'registered!'


@app.route('/thread_list', methods=['GET'])
def thread_list():
    """
        get request url: http://127.0.0.1:5000/thread_list

    """
    result = db.session.query(Thread).all()
    return repr(result)


@app.route('/user_profile', methods=['GET'])
def user_profile():
    """
        get request url: http://127.0.0.1:5000/user_profile

    """
    result = db.session.query(Profile).all()
    return repr(result)

# 不太明白哪个是站内短信
@app.route('/inbox_message', methods=['GET'])
def inbox_message():
    """
        get request url: http://127.0.0.1:5000/inbox_message

    """
    result = db.session.query(Message).all()
    return repr(result)

if __name__ == "__main__":
    app.run(debug=True)
