from datetime import datetime
from flask import Flask, render_template, request, jsonify, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from local import SQLALCHEMY_URL
from utils import return_json, strip_html

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_URL
db = SQLAlchemy(app)


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(255), unique=True)
    signup_date = db.Column(db.DateTime)
    active = db.Column(db.Integer, default=1)

    def __init__(self, email_address):
        self.email_address = email_address
        self.signup_date = datetime.now()

    def __repr__(self):
        return '<Email %r>' % self.email_address


@app.route("/")
def hello():
    return render_template('catmailer.html')


@app.route("/signup", methods=['POST'])
def signup():
    email = request.form['email']
    if len(email) > 0 and '.' in email and '@' in email:
        try:
            email_obj = Email(email)
            db.session.add(email_obj)
            db.session.commit()
            return return_json({'message': 'Successfully signed up.'})
        except IntegrityError as e:
            app.logger.error(e)
            if 'Duplicate entry' in str(e):
                return return_json({'error': 'That email address has already been signed up.'})
            else:
                return return_json({'error': 'Something went wrong with the database. Try again later.'})
        except Exception as e:
            app.logger.error(e)
            return return_json({'error': 'Agh, something went wrong. Try again later.'})

    else:
        return return_json({'error': 'Please enter a valid email address.'})


@app.route('/unsubscribe/<email_address>')
def unsubscribe(email_address):
    try:
        unsub_email = Email.query.filter_by(email_address=email_address).first()
        db.session.delete(unsub_email)
        db.session.commit()
        return 'Succesfully unsubscribed ' + strip_html(email_address)
    except Exception as e:
        app.logger.error(e)
        return 'Something went wrong trying to unsubscribe ' + strip_html(email_address) \
               + '. Try again later.'


if __name__ == "__main__":
    app.debug = True
    app.run()


