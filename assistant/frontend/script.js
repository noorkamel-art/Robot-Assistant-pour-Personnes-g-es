const API_URL = "http://127.0.0.1:5000/api";

let dueReminders = new Map();
let beepInterval = null;


// =========================
// ROBOT STATUS
// =========================

async function loadRobotStatus() {
    try {
        const response = await fetch(`${API_URL}/status`);

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        const currentTime = document.getElementById("currentTime");
        const currentDate = document.getElementById("currentDate");

        if (currentTime) {
            currentTime.textContent = data.time;
        }

        if (currentDate) {
            currentDate.textContent = data.date;
        }

    } catch (error) {
        console.error("Erreur serveur :", error);
    }
}


// =========================
// INTERACTIONS
// =========================

async function loadInteractions() {
    try {
        const response = await fetch(`${API_URL}/interactions`);

        if (!response.ok) {
            throw new Error("Server error");
        }

        const interactions = await response.json();

        updateDashboard(interactions);

    } catch (error) {
        console.error("Erreur interactions :", error);
    }
}


function updateDashboard(interactions) {
    const counter = document.getElementById("conversationCount");
    const statisticsConversations =
        document.getElementById("statisticsConversations");
    const lastInteraction =
        document.getElementById("lastInteraction");

    if (counter) {
        counter.textContent = interactions.length;
    }

    if (statisticsConversations) {
        statisticsConversations.textContent = interactions.length;
    }

    if (lastInteraction) {
        if (interactions.length > 0) {
            lastInteraction.textContent = interactions[0].time;
        } else {
            lastInteraction.textContent = "Aucune";
        }
    }

    updateHistoryPreview(interactions);
    updateConversationLog(interactions);
}


// =========================
// HISTORY PREVIEW
// =========================

function updateHistoryPreview(interactions) {
    const historyPreview =
        document.getElementById("historyPreview");

    if (!historyPreview) {
        return;
    }

    if (interactions.length === 0) {
        historyPreview.innerHTML = `
            <div class="empty-history">
                Aucune interaction enregistrée.
            </div>
        `;
        return;
    }

    historyPreview.innerHTML = "";

    interactions.slice(0, 3).forEach(function(interaction) {
        const element = document.createElement("div");

        element.className = "history-item";

        element.innerHTML = `
            <div class="history-icon">
                💬
            </div>

            <div>
                <strong>
                    ${interaction.time} -
                    ${interaction.language.toUpperCase()}
                </strong>

                <p>
                    ${interaction.question}
                </p>
            </div>
        `;

        historyPreview.appendChild(element);
    });
}


// =========================
// CONVERSATION LOG
// =========================

function updateConversationLog(interactions) {
    const conversationLog =
        document.getElementById("conversationLog");

    if (!conversationLog) {
        return;
    }

    if (interactions.length === 0) {
        conversationLog.innerHTML = `
            <div class="empty-history">
                Aucune conversation enregistrée.
            </div>
        `;
        return;
    }

    conversationLog.innerHTML = "";

    interactions.forEach(function(interaction) {
        const element = document.createElement("div");

        element.className = "history-item";

        element.innerHTML = `
            <div class="history-icon">
                💬
            </div>

            <div>
                <strong>
                    ${interaction.time} -
                    ${interaction.language.toUpperCase()}
                </strong>

                <p>
                    ${interaction.question}
                </p>

                <small>
                    ${interaction.answer}
                </small>
            </div>
        `;

        conversationLog.appendChild(element);
    });
}


// =========================
// HISTORY MODAL
// =========================

async function showHistory() {
    try {
        const response = await fetch(
            `${API_URL}/interactions`
        );

        if (!response.ok) {
            throw new Error("Server error");
        }

        const interactions = await response.json();

        const modal = document.createElement("div");

        modal.className = "modal";

        let historyHTML = "";

        if (interactions.length === 0) {
            historyHTML = `
                <div class="empty-history">
                    Aucune interaction enregistrée.
                </div>
            `;
        } else {
            interactions.forEach(function(interaction) {
                historyHTML += `
                    <div class="modal-history-item">

                        <div class="modal-history-time">
                            ${interaction.time}
                        </div>

                        <div class="modal-history-content">

                            <strong>
                                Conversation
                                (${interaction.language.toUpperCase()})
                            </strong>

                            <p>
                                ${interaction.question}
                            </p>

                            <small>
                                ${interaction.answer}
                            </small>

                        </div>

                    </div>
                `;
            });
        }

        modal.innerHTML = `
            <div class="modal-content">

                <div class="modal-header">

                    <h2>
                        Historique des interactions
                    </h2>

                    <button id="closeHistory">
                        ×
                    </button>

                </div>

                <div class="modal-history">
                    ${historyHTML}
                </div>

            </div>
        `;

        document.body.appendChild(modal);

        document.getElementById("closeHistory")
            .addEventListener("click", function() {
                modal.remove();
            });

        modal.addEventListener("click", function(event) {
            if (event.target === modal) {
                modal.remove();
            }
        });

    } catch (error) {
        console.error("Erreur historique :", error);

        alert("Impossible de charger l'historique.");
    }
}


// =========================
// REMINDERS
// =========================

async function loadReminders() {
    try {
        const response = await fetch(
            `${API_URL}/reminders`
        );

        if (!response.ok) {
            throw new Error("Server error");
        }

        const reminders = await response.json();

        checkDueReminders(reminders);
        updateReminders(reminders);

    } catch (error) {
        console.error("Erreur rappels :", error);
    }
}


// =========================
// CHECK DUE REMINDERS
// =========================

function checkDueReminders(reminders) {
    const now = new Date();

    reminders.forEach(function(reminder) {

        if (reminder.status !== "active") {
            return;
        }

        if (!reminder.date || !reminder.time) {
            return;
        }

        const reminderDateTime =
            new Date(`${reminder.date}T${reminder.time}`);

        if (now >= reminderDateTime) {

            const id = String(reminder.id);

            if (!dueReminders.has(id)) {

                dueReminders.set(id, reminder);

                startBeeping();
            }
        }
    });
}


// =========================
// BEEP
// =========================

function beep() {
    try {
        const AudioContext =
            window.AudioContext ||
            window.webkitAudioContext;

        if (!AudioContext) {
            return;
        }

        const audioContext = new AudioContext();

        const oscillator =
            audioContext.createOscillator();

        const gainNode =
            audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        oscillator.type = "sine";
        oscillator.frequency.value = 800;

        gainNode.gain.setValueAtTime(
            0.3,
            audioContext.currentTime
        );

        oscillator.start();

        gainNode.gain.exponentialRampToValueAtTime(
            0.001,
            audioContext.currentTime + 0.5
        );

        oscillator.stop(
            audioContext.currentTime + 0.5
        );

        oscillator.onended = function() {
            audioContext.close();
        };

    } catch (error) {
        console.error(
            "Erreur son rappel :",
            error
        );
    }
}


function startBeeping() {
    if (beepInterval !== null) {
        return;
    }

    beep();

    beepInterval = setInterval(function() {
        if (dueReminders.size > 0) {
            beep();
        } else {
            stopBeeping();
        }
    }, 2000);
}


function stopBeeping() {
    if (beepInterval !== null) {
        clearInterval(beepInterval);
        beepInterval = null;
    }
}


// =========================
// DISPLAY REMINDERS
// =========================

function updateReminders(reminders) {
    const alertCount =
        document.getElementById("alertCount");

    const statisticsAlerts =
        document.getElementById("statisticsAlerts");

    const alertsContainer =
        document.getElementById("alertsContainer");

    if (alertCount) {
        alertCount.textContent = reminders.length;
    }

    if (statisticsAlerts) {
        statisticsAlerts.textContent = reminders.length;
    }

    if (!alertsContainer) {
        return;
    }

    alertsContainer.innerHTML = "";

    // =========================
    // DUE REMINDERS
    // =========================

    dueReminders.forEach(function(reminder, id) {

        const stillExists = reminders.some(function(item) {
            return String(item.id) === String(id);
        });

        if (!stillExists) {
            dueReminders.delete(id);
            return;
        }

        const element =
            document.createElement("div");

        element.className =
            "alert-item due-reminder";

        element.setAttribute(
            "data-due-id",
            id
        );

        element.innerHTML = `
            <div class="alert-icon">
                🔔
            </div>

            <div>
                <strong>
                    Rappel maintenant
                </strong>

                <p>
                    ${reminder.title}
                </p>

                <small>
                    ${reminder.time}
                </small>
            </div>

            <button
                class="complete-reminder"
                data-id="${id}"
                type="button"
            >
                ✓ Terminé
            </button>
        `;

        alertsContainer.appendChild(element);

        const completeButton =
            element.querySelector(".complete-reminder");

        completeButton.addEventListener(
            "click",
            function() {
                completeReminder(id, element);
            }
        );
    });


    // =========================
    // NORMAL REMINDERS
    // =========================

    reminders.forEach(function(reminder) {

        const id = String(reminder.id);

        if (dueReminders.has(id)) {
            return;
        }

        const element =
            document.createElement("div");

        element.className =
            "alert-item";

        element.setAttribute(
            "data-reminder-id",
            id
        );

        element.innerHTML = `
            <div class="alert-icon">
                🔔
            </div>

            <div>
                <strong>
                    ${reminder.title}
                </strong>

                <p>
                    ${reminder.date}
                    à
                    ${reminder.time}
                </p>

                <small>
                    ${reminder.type}
                </small>
            </div>

            <button
                class="delete-reminder"
                data-id="${id}"
                type="button"
                title="Supprimer"
            >
                ×
            </button>
        `;

        alertsContainer.appendChild(element);

        const deleteButton =
            element.querySelector(".delete-reminder");

        deleteButton.addEventListener(
            "click",
            function() {
                deleteReminder(id);
            }
        );
    });


    // =========================
    // NO ALERT
    // =========================

    if (
        reminders.length === 0 &&
        dueReminders.size === 0
    ) {

        alertsContainer.innerHTML = `
            <div class="no-alert">

                <span class="check-icon">
                    ✓
                </span>

                <div>
                    <strong>
                        Aucune alerte
                    </strong>

                    <p>
                        Tout fonctionne normalement.
                    </p>
                </div>

            </div>
        `;
    }
}


// =========================
// COMPLETE REMINDER
// =========================

async function completeReminder(id, element) {

    try {

        const response = await fetch(
            `${API_URL}/reminders/${id}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error(
                "Erreur lors de la validation"
            );
        }

        dueReminders.delete(String(id));

        if (dueReminders.size === 0) {
            stopBeeping();
        }

        if (element) {
            element.remove();
        }

        await loadReminders();

    } catch (error) {

        console.error(
            "Erreur validation rappel :",
            error
        );

        alert(
            "Impossible de terminer le rappel."
        );
    }
}


// =========================
// DELETE REMINDER
// =========================

async function deleteReminder(id) {

    try {

        const response = await fetch(
            `${API_URL}/reminders/${id}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error(
                "Erreur suppression"
            );
        }

        dueReminders.delete(String(id));

        if (dueReminders.size === 0) {
            stopBeeping();
        }

        await loadReminders();

    } catch (error) {

        console.error(
            "Erreur suppression :",
            error
        );

        alert(
            "Impossible de supprimer le rappel."
        );
    }
}


// =========================
// ADD REMINDER
// =========================

async function addReminder() {

    const title =
        document.getElementById("reminderTitle");

    const date =
        document.getElementById("reminderDate");

    const time =
        document.getElementById("reminderTime");

    const type =
        document.getElementById("reminderType");

    if (!title || !date || !time) {

        alert(
            "Formulaire de rappel introuvable."
        );

        return;
    }

    if (!title.value.trim()) {

        alert(
            "Veuillez entrer un rappel."
        );

        return;
    }

    if (!date.value) {

        alert(
            "Veuillez choisir une date."
        );

        return;
    }

    if (!time.value) {

        alert(
            "Veuillez choisir une heure."
        );

        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/reminders`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    title:
                        title.value.trim(),

                    date:
                        date.value,

                    time:
                        time.value,

                    type:
                        type
                            ? type.value
                            : "general"
                })
            }
        );

        const data =
            await response.json();

        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.error ||
                "Erreur"
            );
        }

        title.value = "";
        date.value = "";
        time.value = "";

        await loadReminders();

        alert(
            "Rappel ajouté avec succès."
        );

    } catch (error) {

        console.error(
            "Erreur ajout rappel :",
            error
        );

        alert(
            "Impossible d'ajouter le rappel."
        );
    }
}


// =========================
// HISTORY BUTTON
// =========================

const historyButton =
    document.getElementById("historyButton");

if (historyButton) {

    historyButton.addEventListener(
        "click",
        showHistory
    );
}


// =========================
// INITIALIZATION
// =========================

loadRobotStatus();
loadInteractions();
loadReminders();


// =========================
// AUTOMATIC REFRESH
// =========================

setInterval(
    loadRobotStatus,
    1000
);

setInterval(
    loadInteractions,
    5000
);

setInterval(
    loadReminders,
    5000
);