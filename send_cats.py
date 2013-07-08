# get all the cat lovers from the database and blast the cats at them
from email.mime.text import MIMEText
import smtplib
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from catmailer import Email
from local import *
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_URL
db = SQLAlchemy(app)


def send_cats():
    # first get 3 cats to send to everyone
    cat_images = []
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                             'Ubuntu Chromium/28.0.1500.52 Chrome/28.0.1500.52 Safari/537.36'}
    for i in range(0, 3):
        r = requests.get('http://thecatapi.com/api/images/get?format=html', headers=headers)
        print r.text
        cat_images.append(r.text)

    cat_lovers = Email.query.filter_by(active=1)
    for cat_lover in cat_lovers:
        print 'sending to ' + cat_lover.email_address
        body_html = build_email_html(cat_images, cat_lover.email_address)
        headers = ['from: catmailer@trillworks.com'
                   'subject: Here are your daily cats',
                   'to: ' + cat_lover.email_address,
                   'mime-version: 1.0',
                   'content-type: text/html'
        ]
        message_string = '\r\n'.join(headers) + '\r\n\r\n' + body_html
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login(GMAIL_USER, GMAIL_PASSWORD)
        session.ehlo()
        session.sendmail('catmailer@trillworks.com', cat_lover.email_address, headers, message_string)
        session.quit()


def build_email_html(cat_images, recipient_email):
    html = '<html> ' \
           '<meta http-equiv="Content-Type" content="text/html charset=UTF-8" />' \
           '<head><style>body {font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}</style></head>' \
           '<body><h3>Enjoy your daily cats!</h3>'
    for cat in cat_images:
        html += cat + '<br>'
    unsubscribe_url = 'http://' + HOSTNAME + '/unsubscribe?email=' + recipient_email
    html += '<a href="' + unsubscribe_url + '" style="color: #787878">Click to unsubscribe</a>'
    html += '</body></html>'
    return html


if __name__ == '__main__':
    send_cats()