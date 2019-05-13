import os
import time

from forms.new_user import RegisterForm
from config.config import ConfigApp
from database.user import User
from utils.util import randomStringwithDigits, create_mail

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

from sqlalchemy.exc import IntegrityError
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
config = ConfigApp()

app.config.update(config.mail_settings())
app.config['SQLALCHEMY_DATABASE_URI'] = config.database_uri()
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)
mail = Mail(app)


@app.route("/")
def home():
    form = RegisterForm()
    return render_template("main.html", form=form, error='', ezeeai_url=config.ezeeai_url())


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        print(config.database_uri())
        for u in User.query.all():
            print(u.username)
        password = randomStringwithDigits()
        new_user = User(username=form.email.data, email=form.email.data,
                        password=generate_password_hash(password, method='sha256'))
        try:
            db.session.add(new_user)
            db.session.commit()

            mail_to = form.email.data
            mail_from = config.mail_from()
            content = render_template('mail/register.html', username=form.email.data, password=password)
            message = create_mail(mail_to, mail_from, content)

            try:
                sg = SendGridAPIClient(config.mail_sengrid_api_key())
                response = sg.send(message)
            except Exception as e:
                print(e.message)
                return render_template("main.html", form=form, error='User created but message can not be sent',
                                       ezeeai_url=config.ezeeai_url())

            return render_template("finish.html", mail=form.email.data, ezeeai_url=config.ezeeai_url())

        except IntegrityError:
            return render_template("main.html", form=form, error='Email is already used. Check your inbox. ',
                                   ezeeai_url=config.ezeeai_url())
        except Exception:
            print(e.message)
            return render_template("main.html", form=form, error='User not created. Please try again',
                                   ezeeai_url=config.ezeeai_url())

    return render_template("finish.html", mail=None, ezeeai_url=config.ezeeai_url())


if __name__ == "__main__":
    app.run(debug=config.debug(),
            threaded=config.threaded(),
            host=config.host(),
            port=config.port())
