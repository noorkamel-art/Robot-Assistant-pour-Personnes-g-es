const API_URL = "http://127.0.0.1:5000";
const PATIENT_ID = 1;


// ==================================================
//                  PATIENT
// ==================================================

fetch(`${API_URL}/patient/${PATIENT_ID}`)
    .then(response => response.json())
    .then(data => {

        if (data.length > 0) {

            document.getElementById(
                "patient-name"
            ).textContent =
                data[0].name;

        }

    })
    .catch(error => {

        console.error(
            "Erreur patient :",
            error
        );

    });


// ==================================================
//                CONVERSATIONS
// ==================================================

fetch(`${API_URL}/conversations/${PATIENT_ID}`)
    .then(response => response.json())
    .then(data => {

        document.getElementById(
            "conversations-count"
        ).textContent =
            data.length;


        if (data.length > 0) {

            document.getElementById(
                "last-interaction"
            ).textContent =
                new Date(
                    data[0].created_at
                ).toLocaleTimeString(
                    "fr-FR",
                    {
                        hour: "2-digit",
                        minute: "2-digit"
                    }
                );

        }

    })
    .catch(error => {

        console.error(
            "Erreur conversations :",
            error
        );

    });


// ==================================================
//                    ALERTES
// ==================================================

fetch(`${API_URL}/alerts/${PATIENT_ID}`)
    .then(response => response.json())
    .then(data => {

        const alertMessage =
            document.getElementById(
                "alert-message"
            );


        if (data.length > 0) {

            alertMessage.textContent =
                "⚠️ " + data[0].message;

        } else {

            alertMessage.textContent =
                "Aucune alerte";

        }

    })
    .catch(error => {

        console.error(
            "Erreur alertes :",
            error
        );

    });


// ==================================================
//              HISTORIQUE DES ALERTES
// ==================================================

fetch(`${API_URL}/alerts/${PATIENT_ID}`)
    .then(response => response.json())
    .then(data => {

        const historyAlerts =
            document.getElementById(
                "history-alerts"
            );


        if (data.length > 0) {

            historyAlerts.innerHTML =
                "<strong>Alertes :</strong><br><br>" +

                data.map(alert =>

                    `⚠️ ${alert.message}<br>
                     Type : ${alert.type}<br><br>`

                ).join("");

        } else {

            historyAlerts.textContent =
                "Aucune alerte";

        }

    })
    .catch(error => {

        console.error(
            "Erreur historique alertes :",
            error
        );

    });


// ==================================================
//           HISTORIQUE DES CONVERSATIONS
// ==================================================

fetch(`${API_URL}/conversations/${PATIENT_ID}`)
    .then(response => response.json())
    .then(data => {

        const historyConversation =
            document.getElementById(
                "history-conversation"
            );


        if (data.length > 0) {

            historyConversation.innerHTML =
                "<strong>Conversations :</strong><br><br>" +

                data.map(conversation =>

                    `👤 ${conversation.user_text}<br>
                     🤖 ${conversation.assistant_text}<br><br>`

                ).join("");

        } else {

            historyConversation.textContent =
                "Aucune conversation";

        }

    })
    .catch(error => {

        console.error(
            "Erreur historique conversations :",
            error
        );

    });


// ==================================================
//              ACTIVITÉ QUOTIDIENNE
// ==================================================

fetch(`${API_URL}/activity/${PATIENT_ID}`)
    .then(response => response.json())
    .then(data => {

        if (data.length > 0) {

            document.getElementById(
                "last-interaction"
            ).textContent =
                new Date(
                    data[0].last_interaction
                ).toLocaleTimeString(
                    "fr-FR",
                    {
                        hour: "2-digit",
                        minute: "2-digit"
                    }
                );


            document.getElementById(
                "conversations-count"
            ).textContent =
                data[0].conversation_count;

        }

    })
    .catch(error => {

        console.error(
            "Erreur activité :",
            error
        );

    });


// ==================================================
//              ASSISTANT VOCAL
// ==================================================


// --------------------------------------------------
// Démarrer l'assistant
// --------------------------------------------------

const startAssistantButton =
    document.getElementById(
        "start-assistant"
    );


if (startAssistantButton) {

    startAssistantButton.addEventListener(
        "click",
        async function () {

            try {

                const response =
                    await fetch(
                        `${API_URL}/assistant/start`,
                        {
                            method: "POST"
                        }
                    );


                const result =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        result.error ||
                        "Erreur lors du démarrage."
                    );

                }


                document.getElementById(
                    "robot-status"
                ).textContent =
                    "Assistant vocal en marche";


                alert(
                    "🤖 Assistant vocal démarré !"
                );


                console.log(
                    "Assistant :",
                    result
                );


            } catch (error) {

                console.error(
                    "Erreur démarrage assistant :",
                    error
                );


                alert(
                    "❌ Impossible de démarrer l'assistant."
                );

            }

        }
    );

}


// --------------------------------------------------
// Arrêter l'assistant
// --------------------------------------------------

const stopAssistantButton =
    document.getElementById(
        "stop-assistant"
    );


if (stopAssistantButton) {

    stopAssistantButton.addEventListener(
        "click",
        async function () {

            const confirmation =
                confirm(
                    "Voulez-vous vraiment arrêter l'assistant vocal ?"
                );


            if (!confirmation) {

                return;

            }


            try {

                const response =
                    await fetch(
                        `${API_URL}/assistant/stop`,
                        {
                            method: "POST"
                        }
                    );


                const result =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        result.error ||
                        "Erreur lors de l'arrêt."
                    );

                }


                document.getElementById(
                    "robot-status"
                ).textContent =
                    "Assistant vocal arrêté";


                alert(
                    "🛑 Assistant vocal arrêté."
                );


                console.log(
                    "Assistant :",
                    result
                );


            } catch (error) {

                console.error(
                    "Erreur arrêt assistant :",
                    error
                );


                alert(
                    "❌ Impossible d'arrêter l'assistant."
                );

            }

        }
    );

}


// ==================================================
//              GESTION DES RAPPELS
// ==================================================

const addReminderButton =
    document.getElementById(
        "add-reminder"
    );


const reminderForm =
    document.getElementById(
        "reminder-form"
    );


const createReminderButton =
    document.getElementById(
        "create-reminder"
    );


if (
    addReminderButton &&
    reminderForm &&
    createReminderButton
) {

    // ----------------------------------------------
    // Afficher le formulaire
    // ----------------------------------------------

    addReminderButton.addEventListener(
        "click",
        function () {

            reminderForm.style.display =
                "block";

        }
    );


    // ----------------------------------------------
    // Créer le rappel
    // ----------------------------------------------

    createReminderButton.addEventListener(
        "click",
        async function () {

            const eventName =
                document.getElementById(
                    "event-name"
                ).value.trim();


            const eventDate =
                document.getElementById(
                    "event-date"
                ).value;


            const eventTime =
                document.getElementById(
                    "event-time"
                ).value;


            if (
                !eventName ||
                !eventDate ||
                !eventTime
            ) {

                alert(
                    "Veuillez remplir tous les champs."
                );

                return;

            }


            const scheduledAt =
                `${eventDate}T${eventTime}:00+01:00`;


            try {

                const response =
                    await fetch(
                        `${API_URL}/reminders/${PATIENT_ID}`,
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({

                                event_name:
                                    eventName,

                                scheduled_at:
                                    scheduledAt

                            })
                        }
                    );


                if (!response.ok) {

                    throw new Error(
                        "Erreur lors de la création du rappel."
                    );

                }


                const result =
                    await response.json();


                console.log(
                    "Rappel créé :",
                    result
                );


                alert(
                    "✅ Rappel créé avec succès !"
                );


                document.getElementById(
                    "event-name"
                ).value = "";


                document.getElementById(
                    "event-date"
                ).value = "";


                document.getElementById(
                    "event-time"
                ).value = "";


                reminderForm.style.display =
                    "none";


                loadReminders();


            } catch (error) {

                console.error(
                    "Erreur création rappel :",
                    error
                );


                alert(
                    "❌ Impossible de créer le rappel."
                );

            }

        }
    );

}


// ==================================================
//              AFFICHER LES RAPPELS
// ==================================================

async function loadReminders() {

    try {

        const response =
            await fetch(
                `${API_URL}/reminders/${PATIENT_ID}`
            );


        if (!response.ok) {

            throw new Error(
                "Erreur lors de la récupération des rappels."
            );

        }


        const data =
            await response.json();


        const reminderList =
            document.getElementById(
                "reminder-list"
            );


        if (!reminderList) {

            return;

        }


        if (data.length === 0) {

            reminderList.innerHTML =
                "<p>Aucun rappel</p>";

            return;

        }


        reminderList.innerHTML =
            "<br><strong>Rappels programmés :</strong><br><br>" +

            data.map(reminder => {

                const date =
                    new Date(
                        reminder.scheduled_at
                    );


                const formattedDate =
                    date.toLocaleString(
                        "fr-FR",
                        {
                            dateStyle: "short",
                            timeStyle: "short"
                        }
                    );


                return `
                    🔔 ${reminder.event_name}<br>
                    📅 ${formattedDate}<br><br>
                `;

            }).join("");


    } catch (error) {

        console.error(
            "Erreur rappels :",
            error
        );

    }

}


// ==================================================
//            SUPPRIMER TOUTES LES ALERTES
// ==================================================

const deleteAlertsButton =
    document.getElementById(
        "delete-alerts"
    );


if (deleteAlertsButton) {

    deleteAlertsButton.addEventListener(
        "click",
        async function () {

            const confirmation =
                confirm(
                    "Voulez-vous vraiment supprimer toutes les alertes et leur historique ?"
                );


            if (!confirmation) {

                return;

            }


            try {

                const response =
                    await fetch(
                        `${API_URL}/alerts/${PATIENT_ID}`,
                        {
                            method: "DELETE"
                        }
                    );


                if (!response.ok) {

                    throw new Error(
                        "Erreur lors de la suppression des alertes."
                    );

                }


                document.getElementById(
                    "alert-message"
                ).textContent =
                    "Aucune alerte";


                document.getElementById(
                    "history-alerts"
                ).textContent =
                    "Aucune alerte";


                alert(
                    "✅ Toutes les alertes ont été supprimées."
                );


            } catch (error) {

                console.error(
                    "Erreur suppression alertes :",
                    error
                );


                alert(
                    "❌ Impossible de supprimer les alertes."
                );

            }

        }
    );

}


// ==================================================
//            SUPPRIMER TOUS LES RAPPELS
// ==================================================

const deleteRemindersButton =
    document.getElementById(
        "delete-reminders"
    );


if (deleteRemindersButton) {

    deleteRemindersButton.addEventListener(
        "click",
        async function () {

            const confirmation =
                confirm(
                    "Voulez-vous vraiment supprimer tous les rappels ?"
                );


            if (!confirmation) {

                return;

            }


            try {

                const response =
                    await fetch(
                        `${API_URL}/reminders/${PATIENT_ID}`,
                        {
                            method: "DELETE"
                        }
                    );


                const result =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        result.error ||
                        "Erreur lors de la suppression des rappels."
                    );

                }


                document.getElementById(
                    "reminder-list"
                ).innerHTML =
                    "<p>Aucun rappel</p>";


                alert(
                    "✅ Tous les rappels ont été supprimés."
                );


                console.log(
                    "Rappels supprimés :",
                    result
                );


            } catch (error) {

                console.error(
                    "Erreur suppression rappels :",
                    error
                );


                alert(
                    "❌ Impossible de supprimer les rappels."
                );

            }

        }
    );

}


// ==================================================
//          CHARGER LES RAPPELS AU DÉMARRAGE
// ==================================================

loadReminders();


// ==================================================
//              DATE & HEURE ACTUELLE
// ==================================================

function updateDateTime() {

    const now = new Date();


    const hours = String(
        now.getHours()
    ).padStart(2, "0");


    const minutes = String(
        now.getMinutes()
    ).padStart(2, "0");


    const seconds = String(
        now.getSeconds()
    ).padStart(2, "0");


    const day = String(
        now.getDate()
    ).padStart(2, "0");


    const month = String(
        now.getMonth() + 1
    ).padStart(2, "0");


    const year = now.getFullYear();


    const currentTime =
        document.getElementById(
            "current-time"
        );


    const currentDate =
        document.getElementById(
            "current-date"
        );


    if (currentTime) {

        currentTime.textContent =
            `${hours}:${minutes}:${seconds}`;

    }


    if (currentDate) {

        currentDate.textContent =
            `${day}/${month}/${year}`;

    }

}


// Mise à jour immédiate
updateDateTime();


// Mise à jour chaque seconde
setInterval(
    updateDateTime,
    1000
);