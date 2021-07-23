from flask import Flask, render_template, request, make_response, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime
import json
from flask_mail import Mail


with open('config.json', 'r') as c:
    params = json.load(c)["params"]
local_server = True

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']= "465"
app.config['MAIL_USERNAME']=params["gmail-user"]
app.config['MAIL_PASSOWRD']=params["gmail-password"]
app.config['MAIL_USE_SSL']=True
mail= Mail(app)
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db=SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    phone_num = db.Column(db.String(13), unique=True, nullable=False)
    msg = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.String(120))


@app.route('/')
def home():
    return render_template('index.html', params=params)


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method=='POST':
        name= request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone_num')
        message = request.form.get('message')

        entry=Contacts(name=name, email=email, phone_num=phone, msg=message, date=datetime.date)
        db.session.add(entry)
        db.session.commit()
        mail.send_message("new message from"+name,
                          sender="email",
                          recipients=[params["gmail-user"]],
                          body=message
                          )
    return render_template('contact.html', params=params)

@app.route('/index')
def index():
    return render_template('index.html', params=params)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post')
def post():
    return render_template('post.html', params=params)

@app.route('/setcookie')
def set():
    resp = make_response(render_template('about.html'))
    resp.set_cookie('cookie', 'flask')
    return resp


if __name__ == '__main__':
    app.run(debug=True, port=2000)
