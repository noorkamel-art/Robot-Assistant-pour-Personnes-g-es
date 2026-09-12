from flask import Flask, jsonify
from flask_cors import CORS
from database import get_conversations, get_alerts, get_patient,get_daily_activity

app = Flask(__name__)
CORS(app)


@app.route("/patient/<int:patient_id>")
def patient(patient_id):
    return jsonify(get_patient(patient_id))


@app.route("/conversations/<int:patient_id>")
def conversations(patient_id):
    return jsonify(get_conversations(patient_id))


@app.route("/alerts/<int:patient_id>")
def alerts(patient_id):
    return jsonify(get_alerts(patient_id))

@app.route("/activity/<int:patient_id>")
def activity(patient_id):
    return jsonify(get_daily_activity(patient_id))

if __name__ == "__main__":
    app.run(debug=True)
