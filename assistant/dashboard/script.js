const API_URL = "http://127.0.0.1:5000";
const PATIENT_ID = 1;


// Récupérer les données du patient
fetch(`${API_URL}/patient/${PATIENT_ID}`)
    .then(response => response.json())
    .then(data => {

        if (data.length > 0) {
            document.getElementById("patient-name").textContent = data[0].name;
        }

    })
    .catch(error => {
        console.error("Erreur patient :", error);
    });


// Récupérer les conversations
fetch(`${API_URL}/conversations/${PATIENT_ID}`)
    .then(response => response.json())
    .then(data => {

        document.getElementById("conversations-count").textContent = data.length;

        if (data.length > 0) {
            document.getElementById("last-interaction").textContent =
                new Date(data[0].created_at).toLocaleTimeString("fr-FR", {
                    hour: "2-digit",
                    minute: "2-digit"
                });
        }

    })
    .catch(error => {
        console.error("Erreur conversations :", error);
    });


// Récupérer les alertes
fetch(`${API_URL}/alerts/${PATIENT_ID}`)
    .then(response => response.json())
    .then(data => {

        const alertMessage = document.getElementById("alert-message");

        if (data.length > 0) {
            alertMessage.textContent =
                "⚠️ " + data[0].message;
        } else {
            alertMessage.textContent = "Aucune alerte";
        }

    })
    .catch(error => {
        console.error("Erreur alertes :", error);
    });

// Afficher l'historique des alertes
fetch(`${API_URL}/alerts/${PATIENT_ID}`)
    .then(response => response.json())
    .then(data => {

        const historyAlerts =
            document.getElementById("history-alerts");

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
        console.error("Erreur historique alertes :", error);
    });

// Afficher l'historique des conversations
fetch(`${API_URL}/conversations/${PATIENT_ID}`)
    .then(response => response.json())
    .then(data => {

        const historyConversation =
            document.getElementById("history-conversation");

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
        console.error("Erreur historique conversations :", error);
    });

// Récupérer l'activité quotidienne
fetch(`${API_URL}/activity/${PATIENT_ID}`)
    .then(response => response.json())
    .then(data => {

        if (data.length > 0) {

            document.getElementById("last-interaction").textContent =
                new Date(data[0].last_interaction).toLocaleTimeString("fr-FR", {
                    hour: "2-digit",
                    minute: "2-digit"
                });

            document.getElementById("conversations-count").textContent =
                data[0].conversation_count;

        }

    })
    .catch(error => {
        console.error("Erreur activité :", error);
    });