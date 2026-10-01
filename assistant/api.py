from flask import Flask, jsonify, request
from flask_cors import CORS

import os
import sys
import subprocess

from database import (
    get_conversations,
    get_alerts,
    get_patient,
    get_daily_activity,
    delete_conversations,
    create_reminder,
    get_reminders,
    delete_alerts,
    delete_reminders
)

app = Flask(__name__)
CORS(app)


# ==================================================
#              ASSISTANT VOCAL
# ==================================================

assistant_process = None


# ==================================================
#              DÉMARRER L'ASSISTANT
# ==================================================

@app.route("/assistant/start", methods=["POST"])
def start_assistant():

    global assistant_process

    if (
        assistant_process is not None
        and assistant_process.poll() is None
    ):

        return jsonify({
            "message": "Assistant déjà en marche"
        }), 200

    main_path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "main.py"
    )

    try:

        assistant_process = subprocess.Popen(
            [sys.executable, main_path]
        )

        print(
            "🤖 Assistant vocal démarré."
        )

        return jsonify({
            "message": "Assistant démarré",
            "pid": assistant_process.pid
        }), 200

    except Exception as error:

        print(
            "❌ ERREUR DÉMARRAGE ASSISTANT :",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# ==================================================
#              ARRÊTER L'ASSISTANT
# ==================================================

@app.route("/assistant/stop", methods=["POST"])
def stop_assistant():

    global assistant_process

    if (
        assistant_process is None
        or assistant_process.poll() is not None
    ):

        return jsonify({
            "message": "Assistant déjà arrêté"
        }), 200

    try:

        pid = assistant_process.pid

        print(
            f"🛑 Arrêt de l'assistant... PID : {pid}"
        )

        # Windows
        if os.name == "nt":

            result = subprocess.run(
                [
                    "taskkill",
                    "/PID",
                    str(pid),
                    "/T",
                    "/F"
                ],
                capture_output=True,
                text=True
            )

            print(
                "TASKKILL :",
                result.stdout
            )

            if result.stderr:

                print(
                    "TASKKILL ERROR :",
                    result.stderr
                )

        # Linux / Mac
        else:

            assistant_process.terminate()

            assistant_process.wait(
                timeout=3
            )

        assistant_process = None

        print(
            "🛑 Assistant vocal arrêté."
        )

        return jsonify({
            "message": "Assistant arrêté"
        }), 200

    except Exception as error:

        print(
            "❌ ERREUR ARRÊT ASSISTANT :",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# ==================================================
#                    PATIENT
# ==================================================

@app.route("/patient/<int:patient_id>")
def patient(patient_id):

    return jsonify(
        get_patient(patient_id)
    )


# ==================================================
#                CONVERSATIONS
# ==================================================

@app.route("/conversations/<int:patient_id>")
def conversations(patient_id):

    return jsonify(
        get_conversations(patient_id)
    )


# Supprimer tout l'historique des conversations

@app.route(
    "/conversations/<int:patient_id>",
    methods=["DELETE"]
)
def delete_conversation_history(patient_id):

    return jsonify(
        delete_conversations(patient_id)
    )


# ==================================================
#                     ALERTES
# ==================================================

# Récupérer les alertes

@app.route(
    "/alerts/<int:patient_id>",
    methods=["GET"]
)
def alerts(patient_id):

    return jsonify(
        get_alerts(patient_id)
    )


# Supprimer toutes les alertes

@app.route(
    "/alerts/<int:patient_id>",
    methods=["DELETE"]
)
def delete_alerts_api(patient_id):

    try:

        result = delete_alerts(
            patient_id
        )

        return jsonify(
            result
        )

    except Exception as error:

        print(
            "❌ ERREUR DELETE ALERTS :",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# ==================================================
#                    ACTIVITÉ
# ==================================================

@app.route(
    "/activity/<int:patient_id>"
)
def activity(patient_id):

    return jsonify(
        get_daily_activity(patient_id)
    )


# ==================================================
#                    RAPPELS
# ==================================================

# Récupérer les rappels

@app.route(
    "/reminders/<int:patient_id>"
)
def reminders(patient_id):

    return jsonify(
        get_reminders(patient_id)
    )


# Supprimer tous les rappels

@app.route(
    "/reminders/<int:patient_id>",
    methods=["DELETE"]
)
def delete_reminders_api(patient_id):

    try:

        result = delete_reminders(
            patient_id
        )

        return jsonify(
            result
        )

    except Exception as error:

        print(
            "❌ ERREUR DELETE REMINDERS :",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# Créer un rappel

@app.route(
    "/reminders/<int:patient_id>",
    methods=["POST"]
)
def create_reminder_api(patient_id):

    data = request.get_json()

    event_name = data.get(
        "event_name"
    )

    scheduled_at = data.get(
        "scheduled_at"
    )

    if not event_name or not scheduled_at:

        return jsonify({
            "error":
                "event_name et scheduled_at sont obligatoires"
        }), 400

    result = create_reminder(
        patient_id,
        event_name,
        scheduled_at
    )

    return jsonify(
        result
    ), 201


# ==================================================
#                 DÉMARRAGE SERVEUR
# ==================================================

if __name__ == "__main__":

    app.run(
        debug=False
    )