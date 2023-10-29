from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'mail.i-cont.eu'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_DEBAG'] = True
app.config['MAIL_USERNAME'] = 'teszt@i-cont.eu'
app.config['MAIL_PASSWORD'] = os.environ.get('PASS')
app.config['MAIL_DEFAULT_SENDER'] = ('Tomi I-CONT','teszt@i-cont.eu')
app.config['MAIL_SMAX_EMAILS'] = 2
#app.config['MAIL_SUPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def receive_data():

    booking = (request.form['booking'])
    container = (request.form['cont'])
    seal = (request.form['seal'])
    print(f"Booking: {booking}")
    print(f"Konténer: {container}")
    print(f"Zár: {seal}\n")

    msg = Message(f"booking: {booking} / {container}", recipients=['kele.tomka@gmail.com'])
    #msg.body = "Kerlek jelentsetek le Bilken az alabbi kontenert:"
    #<h5 style=”font-family: ’Calibri’; font-size:11; color:black;”>
    msg.html = f"""
        <div>
            Sziasztok,<br>
            <br>
            Kérlek jelentsétek le Bilken az alábbi konténert:<br>
            <br>
            konténer: <b>{container}</b><br>
            zár: <b>{seal}</b><br>
            <br>
            Köszönöm előre is,<br>
            Tomi <br>
            <br>
        </div>
        <div>
            Üdvözlettel / Best regards:<br>
            Tamás Kele</h4><br>
            <img src='https://icontshipping.com/wp-content/uploads/2020/06/logo-2.png'; width='100'><br>
        </div>
        <div>
            <b>I-CONT Freight Forwarding S.R.L.</b><br>
            300671-Timisoara-Calea Circumvalatiunii 22.<br>
            <br>
            Mobil: <b>+36 70 779 0921</b><br>
            E-mail: tomi@i-cont.eu<br>
            Web: http://www.i-cont.eu </h5><br>
        </div>"""

    mail.send(msg)

    #email(booking, container, seal)

    return f"""
                Booking: <b>{booking}</b>
                </br>
                Konténer: <b>{container}</b>
                </br>
                Zár: <b>{seal}</b>"""

if __name__ == "__main__":
    app.run()
