from flask import Flask, render_template, request
import smtplib

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def receive_data():

    booking = (request.form['booking'])
    container = (request.form['container'])
    seal = (request.form['seal'])
    print(f"Booking: {booking}")
    print(f"Konténer: {container}")
    print(f"Zár: {seal}\n")
    email(email, booking, container, seal)

    return f"<h1>Booking number: {booking},</br>Container number: {container},</br>Seal number: {seal}</h1>"

def email(to_email, booking, container, seal):
    my_email = "teszt@i-cont.eu"
    password = "Icont87412"
    to_email = "kele.tomka@gmail.com"

    message = f"Sziasztok,\n" \
            f"\n" \
            f"Kerlek jelentsetek le Bilken az alabbi kontenert: \n" \
            f"\n" \
            f"kontener: {container} \n" \
            f"zar: {seal} \n" \
            f"\n" \
            f"Koszonom elore is. \n" \
            f"Tomi\n" \
            f"\n" \
            f"\n" \
            f"Udvozlettel / Best regards:\n" \
            f"Tamas Kele\n" \
            f"I-CONT Freight Forwarding S.R.L.\n" \
            f"300671-Timisoara-Calea Circumvalatiunii 22.\n" \
            f"\n" \
            f"Mobil: +36 70 779 09 21\n" \
            f"E-mail: tomi@i-cont.eu\n" \
            f"Web: http://www.i-cont.eu\n"

    print(message)
    with smtplib.SMTP("mail.i-cont.eu") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=to_email,
            msg=f"Subject:Booking: {booking}/ {container}\n\n{message}"
        )

if __name__ == "__main__":
    app.run(debug=True)
