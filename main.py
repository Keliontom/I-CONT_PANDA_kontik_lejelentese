import time

from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import os
from google_sheet import Icont_sheet

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'mail.i-cont.eu'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_DEBAG'] = True
app.config['MAIL_USERNAME'] = 'lejelentes@i-cont.eu'
app.config['MAIL_PASSWORD'] = os.environ.get('PASS')
app.config['MAIL_DEFAULT_SENDER'] = ('Tomi I-CONT','lejelentes@i-cont.eu')
app.config['MAIL_SMAX_EMAILS'] = 2
#app.config['MAIL_SUPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/not_good')
def not_good():
    return render_template("not_good.html"), {"Refresh": "8; url='https://panda-lejelentes.onrender.com'"}


@app.route("/email_sent", methods=["POST"])
def receive_data():

    booking = (request.form['booking'])
    icont_ref = (request.form['icont_ref'])
    cont = (request.form['cont'])
    seal = (request.form['seal'])
    truck_number = (request.form['rendszam'])
    print(f"Booking: {booking}")
    print(f"Konténer: {cont}")
    print(f"Zár: {seal}\n")

    if googlesheet_kitoltes(icont_ref, booking, cont, seal, truck_number) == False:
        return redirect(url_for('not_good'))


    msg = Message(f"booking: {booking} / {cont}", recipients=['export@coscoshipping.hu', 'export.rco.hu@railcargo.com', 'Zsofia.Ordog@railcargo.com','Liza.Simon@railcargo.com','fanni.vamos@i-cont.eu'])
    #msg = Message(f"booking: {booking} / {cont}", recipients=['tomi@i-cont.eu','fanni.vamos@i-cont.eu'])
    #msg.body = "Kerlek jelentsetek le Bilken az alabbi kontenert:"
    #<h5 style=”font-family: ’Calibri’; font-size:11; color:black;”>
    msg.html = f"""
    <div class="col-4 col-sm-3 col-md-5"> 
        <div>
            Sziasztok,<br>
            <br>
            Kérlek jelentsétek le Bilken az alábbi konténert:<br>
            <br>
            konténer: <b>{cont}</b><br>
            zár: <b>{seal}</b><br>
            <br>
            Köszönöm előre is,<br>
            Tomi <br>
            <br>
        </div>
        <div>
            Üdvözlettel / Best regards:<br>
            Tamás Kele</h4><br>
            <br>
            <img src='https://icontshipping.com/wp-content/uploads/2020/06/logo-2.png'; width='100'><br>
        </div>
        <div>
            <b>I-CONT Freight Forwarding S.R.L.</b><br>
            300671-Timisoara-Calea Circumvalatiunii 22.<br>
            <br>
            Mobil: <b>+36 70 779 0921</b><br>
            E-mail: tomi@i-cont.eu<br>
            Web: http://www.i-cont.eu </h5><br>
        </div>
    </div>"""
    
    mail.send(msg)

    return f"""
                Booking: <b>{booking}</b>
                </br>
                Konténer: <b>{cont}</b>
                </br>
                Zár: <b>{seal}</b>
                </br>
                Rendszám: <b>{truck_number}</b>
                </br>
                </br>
                </br>
                <h3>Az alábbi e-mail lett elküldve a terminálra:</h3>       
                {msg.html}"""


def googlesheet_kitoltes(icont_ref, booking, cont,seal, truck_number):
    googletabla = Icont_sheet()
    googlesheet = "https://docs.google.com/spreadsheets/d/1mQN5woJVHJrqf49D4TlEwQGtDx8PsnqKiLa6B_3Fd4g/edit#gid=0"
    worksheet = "Munkalap1"

    if googletabla.opensheet(googlesheet, worksheet) == False:
        exit()

    #googletabla.opensheet(sheetname="KISZALLITASOK", worksheet="Munkalap1")

    first_row = googletabla.get_container_rows("ICONT Ref.")[0]
    print(first_row)
    try:
        row = googletabla.get_container_rows(icont_ref)[0]
    except:
        return False
    print(row)
    row_dict = googletabla.bild_dictionary(first_row, row)
    print(row_dict)
    row_number= googletabla.get_container_row_numbers(icont_ref)
    print(int(row_number[0]))
    print(row_dict["CONTAINER NO.."])


    if row_dict["CONTAINER NO.."] == booking:
        print("MINDEN RENDBEN!!!!!")
        googletabla.updating_cell(int(row_number[0]), 6, cont)
        googletabla.updating_cell(int(row_number[0]), 15, truck_number)
        googletabla.updating_cell(int(row_number[0]), 24, seal)
        return True
    else:
        print("NEM JÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓ")
        return False


    #email(booking, container, seal)

def email(booking, cont, seal):
    msg = Message("Hello", recipients=['sivokiw143@undewp.com'])
    mail.send(msg)

if __name__ == "__main__":
    app.run()
