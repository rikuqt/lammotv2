from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

measurements = []

@app.route('/')
def get_all_measurements_page():
    return render_template('mittaukset.html', result=measurements)

@app.route('/chart')
def get_line():
    return render_template('charts.html', result=measurements)

@app.route('/uusimittaus', methods=['POST'])
def new_meas():
    # luetaan data viestistä ja deserialisoidaan JSON-data
    m = request.get_json(force=True)
    # muutetaan mittaus Google Chartille sopivaan muotoon (sanakirja -> lista)
    mg = [m['alfa'], m['cpu'], m['cpupros'], m['ram'], m['rampros']]
    # laitetaan listamuotoinen mittaus taulukkoon
    measurements.append(mg)

    # palautetaan vastaanotettu tieto JSON-muodossa
    return jsonify(m)

@app.route('/data')
def get_data():
    # Muodostetaan mittauksista JSON-muotoinen merkkijono
    s = json.dumps(measurements)
    # palautetaan merkkijono JSON-muodossa
    return jsonify(result=s)

if __name__ == '__main__':
    app.run()
