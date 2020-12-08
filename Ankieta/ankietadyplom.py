from flask import Flask, render_template, request
import sqlite3
from pprint import pprint

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("ankieta.html")


@app.route("/raport")
def raport():
    return render_template("raport.html")


@app.route("/wyslij", methods=["POST"])
def wyslij():
    req_data = request.form
    pprint(req_data)

    connection = sqlite3.connect("ankieta.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Ankieta (Id, Objawy, KontaktCovid19, PobytZagranica, NrTelefonu, \
                    Plec, Wiek, Wojewodztwo, WielkoscMiejscaZamieszkania, Marzniecie, Sinienie, \
                    ZimneKapiele, Morsowanie, ZalecenieUnikaniaZimna, Choroby, Leki, Uwagi)\
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            int(req_data["id"]),
            req_data["objawy"],
            req_data["kontaktCovid"],
            req_data["zagranica"],
            int(req_data["telefon"]),
            req_data["plec"],
            int(req_data["wiek"]),
            req_data["wojewodztwo"],
            req_data["wielkoscMiejscaZamieszkania"],
            req_data["marzniecie"],
            req_data["sinienie"],
            req_data["zimneKapiele"],
            req_data["morsowanie"],
            req_data["unikanieZimna"],
            req_data["choroby"],
            req_data["leki"],
            req_data["uwagi"],
        ],
    )
    connection.commit()

    return render_template("ankietaKoniec.html")


@app.route("/raport/wyslij", methods=["POST"])
def raportWyslij():
    req_data = request.form
    pprint(req_data)

    connection = sqlite3.connect("ankieta.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Ankieta (TempBadanego, TetnoPoczatkowe, CisSkurczPoczatkowe, \
                    CisRozkurczPoczatkowe, TempWodyDo1Badania, TetnoPo1Badaniu, CisSkurczPo1Badaniu, \
                    CisRozkurczPo1Badaniu, TempWodyDo2Badania, TetnoPo2Badaniu, CisSkurczPo2Badaniu, CisRozkurczPo2Badaniu) \
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) WHERE Id=?",
        [
            float(req_data["tempBadanego"]),
            int(req_data["tetnoPoczatkowe"]),
            int(req_data["cisSkurczPoczatkowe"]),
            int(req_data["cisRozkurczPoczatkowe"]),
            float(req_data["tempWodyDo1Badania"]),
            int(req_data["tetnoPo1Badaniu"]),
            int(req_data["cisSkurczPo1Badaniu"]),
            int(req_data["cisRozkurczPo1Badaniu"]),
            float(req_data["tempWodyDo2Badania"]),
            int(req_data["tetnoPo2Badaniu"]),
            int(req_data["cisSkurczPo2Badaniu"]),
            int(req_data["cisRozkurczPo2Badaniu"]),
            int(req_data["id"]),
        ],
    )
    connection.commit()


if __name__ == "__main__":
    app.run(debug=True)
