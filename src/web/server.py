from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime
import json
import os


# =========================
# PATHS
# =========================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "assistant",
    "frontend"
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

DATA_FILE = os.path.join(
    DATA_DIR,
    "dashboard.json"
)

REMINDERS_FILE = os.path.join(
    DATA_DIR,
    "reminders.json"
)


# =========================
# FLASK
# =========================

app = Flask(__name__)


# =========================
# DASHBOARD DATA
# =========================

def load_data():

    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(DATA_FILE):

        return {
            "interactions": [],
            "alerts": []
        }

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {
            "interactions": [],
            "alerts": []
        }


def save_data(data):

    os.makedirs(DATA_DIR, exist_ok=True)

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


# =========================
# REMINDER DATA
# =========================

def load_reminders():

    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(REMINDERS_FILE):

        return {
            "reminders": []
        }

    try:

        with open(
            REMINDERS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {
            "reminders": []
        }


def save_reminders(data):

    os.makedirs(DATA_DIR, exist_ok=True)

    with open(
        REMINDERS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


# =========================
# FRONTEND
# =========================

@app.route("/")
def index():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


@app.route("/<path:filename>")
def frontend_files(filename):

    return send_from_directory(
        FRONTEND_DIR,
        filename
    )


# =========================
# ROBOT STATUS
# =========================

@app.route("/api/status", methods=["GET"])
def status():

    now = datetime.now()

    return jsonify({
        "robot": "connected",
        "status": "normal",
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%d/%m/%Y")
    })


# =========================
# INTERACTIONS
# =========================

@app.route("/api/interactions", methods=["GET"])
def get_interactions():

    data = load_data()

    return jsonify(
        data["interactions"]
    )


@app.route("/api/interactions", methods=["POST"])
def add_interaction():

    interaction = request.get_json(
        silent=True
    )

    if not interaction:

        return jsonify({
            "success": False,
            "error": "No data received"
        }), 400

    now = datetime.now()

    new_interaction = {
        "date": now.strftime("%d/%m/%Y"),
        "time": now.strftime("%H:%M:%S"),
        "language": interaction.get("language", ""),
        "question": interaction.get("question", ""),
        "answer": interaction.get("answer", "")
    }

    data = load_data()

    data["interactions"].insert(
        0,
        new_interaction
    )

    save_data(data)

    print("📊 New interaction:")
    print("   Language :", new_interaction["language"])
    print("   Question :", new_interaction["question"])
    print("   Time     :", new_interaction["time"])

    return jsonify({
        "success": True,
        "interaction": new_interaction
    })


# =========================
# REMINDERS
# =========================

@app.route("/api/reminders", methods=["GET"])
def get_reminders():

    data = load_reminders()

    return jsonify(
        data["reminders"]
    )


@app.route("/api/reminders", methods=["POST"])
def add_reminder():

    reminder = request.get_json(
        silent=True
    )

    if not reminder:

        return jsonify({
            "success": False,
            "error": "No data received"
        }), 400

    title = reminder.get(
        "title",
        ""
    ).strip()

    reminder_time = reminder.get(
        "time",
        ""
    ).strip()

    reminder_date = reminder.get(
        "date",
        ""
    ).strip()

    reminder_type = reminder.get(
        "type",
        "general"
    ).strip()

    if not title:

        return jsonify({
            "success": False,
            "error": "Reminder title is required"
        }), 400

    if not reminder_time:

        return jsonify({
            "success": False,
            "error": "Reminder time is required"
        }), 400

    new_reminder = {
        "id": int(
            datetime.now().timestamp() * 1000
        ),
        "title": title,
        "time": reminder_time,
        "date": reminder_date,
        "type": reminder_type,
        "status": "active"
    }

    data = load_reminders()

    data["reminders"].append(
        new_reminder
    )

    save_reminders(data)

    print("🔔 Nouveau rappel :")
    print("   Titre :", title)
    print("   Date  :", reminder_date)
    print("   Heure :", reminder_time)

    return jsonify({
        "success": True,
        "reminder": new_reminder
    })


@app.route(
    "/api/reminders/<int:reminder_id>",
    methods=["DELETE"]
)
def delete_reminder(reminder_id):

    data = load_reminders()

    original_count = len(
        data["reminders"]
    )

    data["reminders"] = [
        reminder
        for reminder in data["reminders"]
        if reminder["id"] != reminder_id
    ]

    save_reminders(data)

    deleted = len(
        data["reminders"]
    ) < original_count

    return jsonify({
        "success": deleted
    })


# =========================
# ALERTS
# =========================

@app.route("/api/alerts", methods=["GET"])
def get_alerts():

    data = load_reminders()

    active_reminders = [
        reminder
        for reminder in data["reminders"]
        if reminder.get("status") == "active"
    ]

    return jsonify(
        active_reminders
    )


# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":

    print("===================================")
    print("   ROBOT ASSISTANT WEB SERVER")
    print("===================================")
    print("Dashboard:")
    print("http://127.0.0.1:5000")
    print("===================================")
    print("Frontend folder:")
    print(FRONTEND_DIR)
    print("===================================")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )