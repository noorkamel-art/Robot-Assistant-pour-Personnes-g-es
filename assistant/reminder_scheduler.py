import time
import winsound
from datetime import datetime
from zoneinfo import ZoneInfo

from database import get_reminders, resolve_reminder


PATIENT_ID = 1

TUNIS_TZ = ZoneInfo("Africa/Tunis")


# ==================================================
#                  SIGNAL SONORE
# ==================================================

def play_alarm():

    print("\n🔔🔔🔔 RAPPEL ! 🔔🔔🔔")

    for i in range(3):

        winsound.Beep(1000, 700)

        time.sleep(0.3)


# ==================================================
#             VÉRIFIER LES RAPPELS
# ==================================================

def check_reminders():

    reminders = get_reminders(PATIENT_ID)

    now = datetime.now(TUNIS_TZ)


    for reminder in reminders:

        # Ignorer les rappels déjà exécutés
        if reminder["is_resolved"]:
            continue


        scheduled_at = datetime.fromisoformat(
            reminder["scheduled_at"].replace("Z", "+00:00")
        )


        # Convertir vers l'heure de Tunis
        scheduled_at = scheduled_at.astimezone(TUNIS_TZ)


        # Vérifier si l'heure du rappel est arrivée
        if scheduled_at <= now:

            print()
            print("================================")
            print("🔔 RAPPEL")
            print("Événement :", reminder["event_name"])
            print(
                "Heure :",
                scheduled_at.strftime("%d/%m/%Y %H:%M")
            )
            print("================================")


            # Jouer le signal sonore
            play_alarm()


            # Marquer le rappel comme exécuté
            resolve_reminder(reminder["id"])


            print("✅ Rappel marqué comme résolu.")


# ==================================================
#                    PROGRAMME
# ==================================================

if __name__ == "__main__":

    print("🔔 Reminder Scheduler démarré.")

    print("Surveillance des rappels en cours...")


    while True:

        try:

            check_reminders()

        except Exception as error:

            print("❌ Erreur :", error)


        # Vérifier toutes les 5 secondes
        time.sleep(5)