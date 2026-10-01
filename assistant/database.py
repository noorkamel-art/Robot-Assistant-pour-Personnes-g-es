import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime
from zoneinfo import ZoneInfo


# ==================================================
#              CONNEXION SUPABASE
# ==================================================

# Charger les variables du fichier .env
load_dotenv()


# Connexion à Supabase
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


# ==================================================
#                    PATIENT
# ==================================================

# Ajouter un patient
def create_patient(name):

    response = supabase.table("patients").insert({
        "name": name
    }).execute()

    return response.data


# Récupérer un patient
def get_patient(patient_id):

    response = supabase.table("patients").select("*").eq(
        "id", patient_id
    ).execute()

    return response.data


# ==================================================
#                CONVERSATIONS
# ==================================================

# Enregistrer une conversation
def save_conversation(
    patient_id,
    user_text,
    assistant_text
):

    response = supabase.table("conversations").insert({
        "patient_id": patient_id,
        "user_text": user_text,
        "assistant_text": assistant_text
    }).execute()

    return response.data


# Récupérer les conversations
def get_conversations(patient_id):

    response = supabase.table("conversations").select("*").eq(
        "patient_id", patient_id
    ).order(
        "created_at",
        desc=True
    ).execute()

    return response.data


# Supprimer tout l'historique des conversations
def delete_conversations(patient_id):

    response = supabase.table("conversations").delete().eq(
        "patient_id", patient_id
    ).execute()

    return response.data


# ==================================================
#                     ALERTES
# ==================================================

# Enregistrer une alerte
def save_alert(
    patient_id,
    alert_type,
    message
):

    response = supabase.table("alerts").insert({
        "patient_id": patient_id,
        "type": alert_type,
        "message": message,
        "is_resolved": False
    }).execute()

    return response.data


# Récupérer les alertes
def get_alerts(patient_id):

    response = supabase.table("alerts").select("*").eq(
        "patient_id", patient_id
    ).order(
        "created_at",
        desc=True
    ).execute()

    return response.data


# Supprimer toutes les alertes
# sauf les rappels
def delete_alerts(patient_id):

    response = supabase.table("alerts").delete().eq(
        "patient_id", patient_id
    ).neq(
        "type", "reminder"
    ).execute()

    return response.data


# ==================================================
#                    ACTIVITÉ
# ==================================================

# Récupérer l'activité quotidienne
def get_daily_activity(patient_id):

    response = supabase.table("activity").select("*").eq(
        "patient_id", patient_id
    ).order(
        "date",
        desc=True
    ).execute()

    return response.data


# Enregistrer / mettre à jour l'activité quotidienne
def save_daily_activity(patient_id):

    tunis_tz = ZoneInfo("Africa/Tunis")

    now_tunis = datetime.now(tunis_tz)

    today = now_tunis.date().isoformat()

    now = now_tunis.isoformat()


    # Vérifier si une activité existe déjà aujourd'hui
    response = supabase.table("activity").select("*").eq(
        "patient_id", patient_id
    ).eq(
        "date", today
    ).execute()


    if response.data:

        activity_id = response.data[0]["id"]

        current_count = response.data[0][
            "conversation_count"
        ]


        response = supabase.table("activity").update({

            "last_interaction": now,

            "conversation_count":
                current_count + 1

        }).eq(
            "id",
            activity_id
        ).execute()


    else:

        response = supabase.table("activity").insert({

            "patient_id": patient_id,

            "date": today,

            "last_interaction": now,

            "conversation_count": 1

        }).execute()


    return response.data


# ==================================================
#                    RAPPELS
# ==================================================

# Créer un rappel
def create_reminder(
    patient_id,
    event_name,
    scheduled_at
):

    response = supabase.table("alerts").insert({

        "patient_id": patient_id,

        "type": "reminder",

        "message": event_name,

        "event_name": event_name,

        "scheduled_at": scheduled_at,

        "is_resolved": False

    }).execute()

    return response.data


# Récupérer les rappels
def get_reminders(patient_id):

    response = supabase.table("alerts").select("*").eq(
        "patient_id", patient_id
    ).eq(
        "type", "reminder"
    ).order(
        "scheduled_at",
        desc=False
    ).execute()

    return response.data


# Marquer un rappel comme résolu
def resolve_reminder(reminder_id):

    response = supabase.table("alerts").update({

        "is_resolved": True

    }).eq(
        "id",
        reminder_id
    ).execute()

    return response.data


# Supprimer tous les rappels
def delete_reminders(patient_id):

    response = supabase.table("alerts").delete().eq(
        "patient_id", patient_id
    ).eq(
        "type", "reminder"
    ).execute()

    return response.data