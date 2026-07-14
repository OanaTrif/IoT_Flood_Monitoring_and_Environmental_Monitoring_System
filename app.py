from flask import Flask, render_template, request, jsonify
import serial
import threading
import time
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

app = Flask(__name__)

PORT_SERIAL = 'COM3'  
BAUD_RATE = 9600

date_curente = {"temperatura": "--", "umiditate": "--", "nivel_apa": "0"}
istoric_mesaje = []
istoric_inundatii = []
alerta_trimisa = False


EMAIL_EXPEDITOR = "oanatrif23@gmail.com"
EMAIL_PAROLA = "uilk eztm zcsu pokx"  
EMAIL_DESTINATAR = "oanatrif23@gmail.com"

try:
    conexiune_seriala = serial.Serial(PORT_SERIAL, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Conectat cu succes la Arduino pe portul {PORT_SERIAL}")
except Exception as e:
    print(f"Eroare port serial: {e}. Asigura-te ca Serial Monitor din Arduino IDE este INCHIS!")
    conexiune_seriala = None

def trimite_email_alerta(data_ora):
    try:
        msg = MIMEText(f"Alerta! Sistemul a detectat o inundatie la data de: {data_ora}")
        msg['Subject'] = 'ALERTA INUNDATIE - Sistem IoT'
        msg['From'] = EMAIL_EXPEDITOR
        msg['To'] = EMAIL_DESTINATAR
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_EXPEDITOR, EMAIL_PAROLA)
        server.sendmail(EMAIL_EXPEDITOR, [EMAIL_DESTINATAR], msg.as_string())
        server.quit()
    except Exception:
        print("E-mailul nu s-a trimis (necesita configurare cont Google), dar logica functioneaza!")

def citeste_date_arduino():
    global date_curente, alerta_trimisa, istoric_inundatii
    while True:
        if conexiune_seriala and conexiune_seriala.in_waiting > 0:
            try:
                linie = conexiune_seriala.readline().decode('utf-8').strip()
                if linie.startswith("DATA"):
                    parti = linie.split('\t')
                    date_curente["umiditate"] = parti[1]
                    date_curente["temperatura"] = parti[2]
                    date_curente["nivel_apa"] = parti[3]
                    
                    val_apa = int(parti[3])
                    if val_apa > 100:
                        if not alerta_trimisa:
                            acum = datetime.now().strftime("%d/%m %H:%M:%S")
                            conexiune_seriala.write(f"F:{acum}\n".encode())
                            threading.Thread(target=trimite_email_alerta, args=(acum,)).start()
                            if acum not in istoric_inundatii:
                                if len(istoric_inundatii) >= 10: istoric_inundatii.pop(0)
                                istoric_inundatii.append(acum)
                            alerta_trimisa = True
                    else:
                        alerta_trimisa = False
            except Exception:
                pass
        time.sleep(0.1)

threading.Thread(target=citeste_date_arduino, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html', mesaje=istoric_mesaje, inundatii=istoric_inundatii)

@app.route('/date-senzor')
def date_senzor():
    return jsonify(date_curente)

@app.route('/comanda-led', methods=['POST'])
def comanda_led():
    comanda = request.json.get('comanda')
    if conexiune_seriala and comanda in ['A', 'S']:
        conexiune_seriala.write(f"{comanda}\n".encode())
        return jsonify({"status": "succes"})
    return jsonify({"status": "eroare"}), 500

@app.route('/trimite-mesaj', methods=['POST'])
def trimite_mesaj():
    global istoric_mesaje
    text_mesaj = request.json.get('mesaj', '')
    if len(text_mesaj) > 18: text_mesaj = text_mesaj[:18]
    if conexiune_seriala and text_mesaj:
        conexiune_seriala.write(f"M:{text_mesaj}\n".encode())
        if len(istoric_mesaje) >= 10: istoric_mesaje.pop(0)
        istoric_mesaje.append(text_mesaj)
        return jsonify({"status": "succes"})
    return jsonify({"status": "eroare"}), 400

@app.route('/sterge-eveniment', methods=['POST'])
def sterge_eveniment():
    global istoric_inundatii
    idx = request.json.get('index')
    if 0 <= idx < len(istoric_inundatii):
        istoric_inundatii.pop(idx)
        return jsonify({"status": "succes"})
    return jsonify({"status": "eroare"}), 400

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)