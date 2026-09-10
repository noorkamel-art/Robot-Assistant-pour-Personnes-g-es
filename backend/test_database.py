from database import create_patient, get_patient, save_conversation, get_conversations, save_alert, get_alerts, get_daily_activity

patient_id = create_patient(
    nom="Ben Ali",
    prenom="Ahmed",
    date_naissance="1945-05-10",
    telephone="22123456"
)

print("Patient créé avec ID :", patient_id)

patient = get_patient(patient_id)

print("Patient récupéré :", dict(patient))

conversation_id = save_conversation(
    patient_id,
    "Bonjour, pouvez-vous m'aider ?",
    "Bonjour Ahmed, bien sûr. Comment puis-je vous aider ?"
)

print("Conversation enregistrée avec ID :", conversation_id)

conversations = get_conversations(patient_id)

print("Historique des conversations :")

for conversation in conversations:
    print(dict(conversation))

    alert_id = save_alert(
    patient_id,
    "Le patient doit prendre son médicament.",
    "medication"
)

print("Alerte enregistrée avec ID :", alert_id)
alerts = get_alerts(patient_id)

print("Historique des alertes :")

for alert in alerts:
    print(dict(alert))

    activities = get_daily_activity(patient_id)

print("Activités du jour :")

for activity in activities:
    print(dict(activity))