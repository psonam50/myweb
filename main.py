from flask import Flask, render_template, request, make_response, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime
import json
from flask_mail import Mail


app = Flask(__name__)

with open('config.json', 'r') as c:
    params = json.load(c)["params"]
local_server = params["local_server"]



app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']= 465
app.config['MAIL_USERNAME']= "actecalsales@gmail.com"
app.config['MAIL_PASSWORD']="Buddy@2020"
app.config['MAIL_USE_SSL']= True
app.secret_key= 'be6d7dc1a115b49ab6de6ac2'
mail= Mail(app)
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db=SQLAlchemy(app)

class ContactUs(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    phone_num = db.Column(db.String(13), unique=False, nullable=False)
    msg = db.Column(db.String(120), unique=False, nullable=False)
    date = db.Column(db.String(120))


@app.route('/')
def home():
    return render_template('index.html', params=params)


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name= request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone_num')
        message = request.form.get('message')


        entry=ContactUs(name=name, email=email, phone_num=phone, msg=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message(
                          sender=email,
                          recipients=[app.config['MAIL_USERNAME']],
                          body=message
                          )
    return render_template('contact.html', params=params)

@app.route('/index')
def index():
    return render_template('index.html', params=params)


@app.route('/about')
def about():
    return render_template('about.html', params=params)


@app.route('/post')
def post():
    return render_template('post.html', params=params)


@app.route('/cookie/')
def cookie():
    if not request.cookies.get('foo'):
        res = make_response("Setting a cookie")
        res.set_cookie('foo', 'bar', max_age=60*60*24*365*2)
    else:
        res = make_response("Value of cookie foo is {}".format(request.cookies.get('foo')))
    return res

@app.route('/delete-cookie/')
def delete_cookie():
    res = make_response("Cookie Removed")
    res.set_cookie('foo', 'bar', max_age=0)
    return res


@app.route('/article/', methods=['POST', 'GET'])
def article():
    if request.method == 'POST':
        print(request.form)
        res = make_response("")
        res.set_cookie("font", request.form.get('font'), 60 * 60 * 24 * 15)
        res.headers['location'] = url_for('article')
        return res, 302

    return render_template('article.html')


@app.route('/show')
def show_all():
   return render_template('show_all.html', Contacts = ContactUs.query.all() )

@app.route('/login')
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('psw')
        message = request.form.get('message')

    return render_template('login.html')

if __name__ == '__main__':
    db.create_all()
    app.run( debug=True)
