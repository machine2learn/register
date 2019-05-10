import os

from easyregister.forms.new_user import RegisterForm
from config.config import ConfigApp
from database.user import User
from utils.util import randomStringwithDigits, check_user_exists

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
    return render_template("main.html", form=form, error='')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        password = randomStringwithDigits()
        new_user = User(username=form.email.data,
                        email=form.email.data,
                        password=generate_password_hash(password, method='sha256'))
        try:
            db.session.add(new_user)
            db.session.commit()
            if check_user_exists(form.email.data, db):
                recipient = form.email.data
                msg = Message("EasyAI complete register - M2L", sender="tf3deep@gmail.com", recipients=[recipient])
                msg.html = render_template('mail/register.html', username=form.email.data, password=password)
                mail.send(msg)
                return render_template("finish.html", mail=recipient)
            else:
                raise Exception

        except IntegrityError:
            return render_template("main.html", form=form, error='Email is already used. Check your inbox. ')
        except Exception:
            return render_template("main.html", form=form, error='User not created. Please try again')

    return render_template("finish.html", mail=None)


if __name__ == "__main__":
    app.run(debug=config.debug(),
            threaded=config.threaded(),
            host=config.host(),
            port=config.port())
