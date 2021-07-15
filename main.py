from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/actecal'
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
    return render_template('index.html')


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
    return render_template('contact.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post')
def post():
    return render_template('post.html')


if __name__ == '__main__':
    app.run(debug=True, port=2000)
