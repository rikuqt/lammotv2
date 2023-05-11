from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, emit
import json
import requests
import random
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


measurements = []
pros = []

def random_lammot():
    cpu = 0
    cpupros = 0
    ram = 0
    rampros = 0

    alfa = 0
    while alfa < 100:
        cpu = random.randint(80,85)
        cpupros = random.randint(60,70)
        ram = random.randint(35,40)
        rampros = random.randint(65,70)

        measurement = { }
        measurement['alfa'] = alfa
        measurement['cpu'] = cpu
        measurement['cpupros'] = cpupros
        measurement['ram'] = ram
        measurement['rampros'] = rampros

        # TODO: lähetä data HTTP Postilla serverille
        s = json.dumps(measurement)
        response = requests.post("http://localhost:5000/uusimittaus", data = s)

        print(s)
        time.sleep(1)

        alfa += 1
        
@app.route('/')
def get_all_measurements_page():
    return render_template('mittaukset.html', result = measurements)


@app.route('/chart')
def get_line():
    return render_template('charts.html', result = measurements)

@app.route('/uusimittaus', methods=['POST'])
def new_meas():
    # luetaan data viestistä ja deserialisoidaan JSON-data
    m = request.get_json(force=True)
    # muutetaan mittaus Google Chartille sopivaan muotoon (sanakirja -> lista)
    mg = [m['alfa'], m['cpu'], m['cpupros'], m['ram'],m['rampros']]
    # laitetaan listamuotoinen mittaus taulukkoon
    measurements.append(mg)
    # lähetetään koko taulukko socket.io:n avulla html-sivulle
    s = json.dumps(measurements)
    socketio.emit('my_response', {'result': s})
    # palautetaan vastaanotettu tieto
    return json.dumps(m, indent=True)

if __name__ == '__main__':
    random_lammot()
    socketio.run(app)
