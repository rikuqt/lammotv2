from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def get_all_measurements_page():
    return render_template('mittaukset.html', result = measurements)


@app.route('/chart')
def get_line():
    return render_template('charts.html', result = measurements)

#@app.route('/temps')
#def get_all_measurements_page():
#    return render_template('raspberrytemp.html', result = pros)


#@app.route('/raspberry')
#def get_line():
#    return render_template('raspberry.html', result = pros)

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
    socketio.run(app)
