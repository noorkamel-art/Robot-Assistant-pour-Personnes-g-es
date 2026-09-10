import sqlite3

DATABASE = "backend/robot_assistant.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Table des patients
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            date_naissance TEXT,
            telephone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table des conversations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            question TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)

    # Table des alertes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            message TEXT NOT NULL,
            type TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)

    # Table de l'activite
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            activity_type TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)

    connection.commit()
    connection.close()

def create_patient(nom, prenom, date_naissance=None, telephone=None):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO patients (nom, prenom, date_naissance, telephone)
        VALUES (?, ?, ?, ?)
    """, (nom, prenom, date_naissance, telephone))

    connection.commit()

    patient_id = cursor.lastrowid

    connection.close()

    return patient_id

def get_patient(patient_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM patients
        WHERE id = ?
    """, (patient_id,))

    patient = cursor.fetchone()

    connection.close()

    return patient

def save_conversation(patient_id, question, response):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO conversations (patient_id, question, response)
        VALUES (?, ?, ?)
    """, (patient_id, question, response))

    connection.commit()

    conversation_id = cursor.lastrowid

    connection.close()

    return conversation_id

def get_conversations(patient_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM conversations
        WHERE patient_id = ?
        ORDER BY created_at DESC
    """, (patient_id,))

    conversations = cursor.fetchall()

    connection.close()

    return conversations

def save_alert(patient_id, message, type_alert=None):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO alerts (patient_id, message, type)
        VALUES (?, ?, ?)
    """, (patient_id, message, type_alert))

    connection.commit()

    alert_id = cursor.lastrowid

    connection.close()

    return alert_id

def get_alerts(patient_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM alerts
        WHERE patient_id = ?
        ORDER BY created_at DESC
    """, (patient_id,))

    alerts = cursor.fetchall()

    connection.close()

    return alerts

def get_daily_activity(patient_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM activities
        WHERE patient_id = ?
        AND DATE(created_at) = DATE('now')
        ORDER BY created_at DESC
    """, (patient_id,))

    activities = cursor.fetchall()

    connection.close()

    return activities