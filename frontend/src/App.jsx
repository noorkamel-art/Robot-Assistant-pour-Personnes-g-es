import { useState } from "react";

function App() {
  const [activePage, setActivePage] = useState("Dashboard");

  const menuItems = [
    { name: "Dashboard", icon: "⌂" },
    { name: "Conversations", icon: "💬" },
    { name: "Alertes", icon: "⚠" },
    { name: "Activité", icon: "◷" },
    { name: "Statistiques", icon: "▥" },
    { name: "Profil patient", icon: "♙" },
    { name: "Notifications", icon: "♢" },
    { name: "Médecin", icon: "⚕" },
    { name: "Paramètres", icon: "⚙" },
  ];

  const conversations = [
    {
      time: "14:32",
      question: "Bonjour, pouvez-vous m'aider ?",
      response: "Bien sûr, comment puis-je vous aider ?",
    },
    {
      time: "13:15",
      question: "Quelle heure est-il ?",
      response: "Il est 13 heures 15.",
    },
    {
      time: "11:40",
      question: "Je veux prendre mon médicament.",
      response: "N'oubliez pas de prendre votre médicament.",
    },
  ];

  const alerts = [
    {
      type: "Information",
      title: "Interaction normale",
      text: "La dernière interaction avec le robot s'est bien déroulée.",
      level: "normal",
    },
    {
      type: "Rappel",
      title: "Médicament à prendre",
      text: "Un rappel de médicament est prévu prochainement.",
      level: "warning",
    },
  ];

  const activities = [
    { hour: "08:00", activity: "Réveil" },
    { hour: "09:30", activity: "Interaction avec le robot" },
    { hour: "11:40", activity: "Rappel médicament" },
    { hour: "13:15", activity: "Question posée au robot" },
    { hour: "14:32", activity: "Interaction avec le robot" },
  ];

  return (
    <div className="app">

      {/* ================= SIDEBAR ================= */}

      <aside className="sidebar">

        <div className="logo-section">
          <div className="robot-logo">🤖</div>

          <div>
            <h2>Robot Assistant</h2>
            <p>Personnes âgées</p>
          </div>
        </div>

        <div className="menu-title">
          MENU PRINCIPAL
        </div>

        <nav className="menu">

          {menuItems.map((item) => (
            <button
              key={item.name}
              className={`menu-item ${
                activePage === item.name ? "active" : ""
              }`}
              onClick={() => setActivePage(item.name)}
            >
              <span className="menu-icon">
                {item.icon}
              </span>

              <span>
                {item.name}
              </span>
            </button>
          ))}

        </nav>

        <div className="sidebar-bottom">

          <div className="robot-status-small">
            <span className="status-dot"></span>

            <div>
              <strong>Robot connecté</strong>
              <small>Tout fonctionne normalement</small>
            </div>
          </div>

        </div>

      </aside>


      {/* ================= MAIN ================= */}

      <main className="main">

        {/* HEADER */}

        <header className="header">

          <div>
            <p className="header-small">
              ESPACE FAMILLE / MÉDECIN
            </p>

            <h1>
              {activePage}
            </h1>
          </div>

          <div className="header-right">

            <button className="notification-button">
              🔔
              <span className="notification-badge">2</span>
            </button>

            <div className="user-profile">

              <div className="avatar">
                FM
              </div>

              <div>
                <strong>Famille</strong>
                <small>Administrateur</small>
              </div>

            </div>

          </div>

        </header>


        {/* ================= DASHBOARD ================= */}

        {activePage === "Dashboard" && (

          <div className="dashboard">

            {/* Welcome */}

            <section className="welcome-card">

              <div>

                <p className="welcome-label">
                  BONJOUR 👋
                </p>

                <h2>
                  Bienvenue sur votre espace
                </h2>

                <p>
                  Consultez facilement l'état du robot,
                  l'activité du patient et les dernières alertes.
                </p>

              </div>

              <div className="welcome-robot">
                🤖
              </div>

            </section>


            {/* STAT CARDS */}

            <section className="stats-grid">

              <div className="stat-card">

                <div className="stat-icon blue">
                  ♙
                </div>

                <div>
                  <p>Patient</p>
                  <h3>Normal</h3>
                  <span className="green-text">
                    ● État stable
                  </span>
                </div>

              </div>


              <div className="stat-card">

                <div className="stat-icon purple">
                  ◷
                </div>

                <div>
                  <p>Dernière interaction</p>
                  <h3>14:32</h3>
                  <span>
                    Aujourd'hui
                  </span>
                </div>

              </div>


              <div className="stat-card">

                <div className="stat-icon orange">
                  💬
                </div>

                <div>
                  <p>Conversations</p>
                  <h3>12</h3>
                  <span>
                    Aujourd'hui
                  </span>
                </div>

              </div>


              <div className="stat-card">

                <div className="stat-icon red">
                  ⚠
                </div>

                <div>
                  <p>Alertes</p>
                  <h3>1</h3>
                  <span>
                    À vérifier
                  </span>
                </div>

              </div>

            </section>


            {/* CONTENT GRID */}

            <section className="content-grid">

              {/* ACTIVITY */}

              <div className="panel">

                <div className="panel-header">

                  <div>
                    <h2>Activité récente</h2>
                    <p>
                      Dernières activités du patient
                    </p>
                  </div>

                  <button
                    className="link-button"
                    onClick={() => setActivePage("Activité")}
                  >
                    Voir tout →
                  </button>

                </div>


                <div className="activity-list">

                  {activities.map((item, index) => (

                    <div
                      className="activity-item"
                      key={index}
                    >

                      <div className="activity-time">
                        {item.hour}
                      </div>

                      <div className="activity-line">
                        <span></span>
                      </div>

                      <div className="activity-info">
                        <strong>
                          {item.activity}
                        </strong>

                        <small>
                          Activité enregistrée par le système
                        </small>
                      </div>

                    </div>

                  ))}

                </div>

              </div>


              {/* ALERTS */}

              <div className="panel">

                <div className="panel-header">

                  <div>
                    <h2>Alertes</h2>
                    <p>
                      Informations importantes
                    </p>
                  </div>

                  <button
                    className="link-button"
                    onClick={() => setActivePage("Alertes")}
                  >
                    Voir tout →
                  </button>

                </div>


                <div className="alerts-list">

                  {alerts.map((alert, index) => (

                    <div
                      className={`alert-card ${alert.level}`}
                      key={index}
                    >

                      <div className="alert-icon">
                        {alert.level === "warning"
                          ? "⚠"
                          : "✓"}
                      </div>

                      <div>

                        <span className="alert-type">
                          {alert.type}
                        </span>

                        <h3>
                          {alert.title}
                        </h3>

                        <p>
                          {alert.text}
                        </p>

                      </div>

                    </div>

                  ))}

                </div>

              </div>

            </section>


            {/* CONVERSATIONS */}

            <section className="panel conversation-panel">

              <div className="panel-header">

                <div>
                  <h2>
                    Dernières conversations
                  </h2>

                  <p>
                    Historique des interactions avec le robot
                  </p>
                </div>

                <button
                  className="link-button"
                  onClick={() =>
                    setActivePage("Conversations")
                  }
                >
                  Voir l'historique →
                </button>

              </div>


              <div className="conversation-list">

                {conversations.map((conversation, index) => (

                  <div
                    className="conversation-item"
                    key={index}
                  >

                    <div className="conversation-time">
                      {conversation.time}
                    </div>

                    <div className="conversation-content">

                      <div className="question">

                        <span className="conversation-label">
                          Patient
                        </span>

                        <p>
                          {conversation.question}
                        </p>

                      </div>


                      <div className="response">

                        <span className="conversation-label">
                          Robot
                        </span>

                        <p>
                          {conversation.response}
                        </p>

                      </div>

                    </div>

                  </div>

                ))}

              </div>

            </section>


            {/* BOTTOM CARDS */}

            <section className="bottom-grid">

              <div className="quick-card">

                <div className="quick-icon">
                  💬
                </div>

                <div>
                  <h3>Conversations</h3>
                  <p>
                    Consulter toutes les interactions
                    avec le robot.
                  </p>
                </div>

                <button
                  onClick={() =>
                    setActivePage("Conversations")
                  }
                >
                  →
                </button>

              </div>


              <div className="quick-card">

                <div className="quick-icon">
                  📊
                </div>

                <div>
                  <h3>Statistiques</h3>
                  <p>
                    Visualiser l'activité et les statistiques.
                  </p>
                </div>

                <button
                  onClick={() =>
                    setActivePage("Statistiques")
                  }
                >
                  →
                </button>

              </div>


              <div className="quick-card">

                <div className="quick-icon">
                  ⚕
                </div>

                <div>
                  <h3>Espace médecin</h3>
                  <p>
                    Accéder aux informations médicales.
                  </p>
                </div>

                <button
                  onClick={() =>
                    setActivePage("Médecin")
                  }
                >
                  →
                </button>

              </div>

            </section>

          </div>

        )}


        {/* ================= CONVERSATIONS ================= */}

        {activePage === "Conversations" && (

          <div className="page-content">

            <div className="page-title">
              <h2>Historique des conversations</h2>
              <p>
                Toutes les interactions entre le patient et le robot.
              </p>
            </div>

            <div className="panel">

              {conversations.map((conversation, index) => (

                <div
                  className="full-conversation"
                  key={index}
                >

                  <span className="full-time">
                    {conversation.time}
                  </span>

                  <div>

                    <strong>
                      Patient
                    </strong>

                    <p>
                      {conversation.question}
                    </p>

                    <strong>
                      Robot Assistant
                    </strong>

                    <p>
                      {conversation.response}
                    </p>

                  </div>

                </div>

              ))}

            </div>

          </div>

        )}


        {/* ================= ALERTES ================= */}

        {activePage === "Alertes" && (

          <div className="page-content">

            <div className="page-title">
              <h2>Alertes</h2>
              <p>
                Consultez les alertes et rappels importants.
              </p>
            </div>

            <div className="alerts-page">

              {alerts.map((alert, index) => (

                <div
                  className={`big-alert ${alert.level}`}
                  key={index}
                >

                  <div className="big-alert-icon">
                    {alert.level === "warning"
                      ? "⚠"
                      : "✓"}
                  </div>

                  <div>
                    <span>{alert.type}</span>
                    <h2>{alert.title}</h2>
                    <p>{alert.text}</p>
                  </div>

                </div>

              ))}

            </div>

          </div>

        )}


        {/* ================= ACTIVITE ================= */}

        {activePage === "Activité" && (

          <div className="page-content">

            <div className="page-title">
              <h2>Activité du patient</h2>
              <p>
                Historique des activités enregistrées.
              </p>
            </div>

            <div className="panel">

              <div className="big-activity-list">

                {activities.map((item, index) => (

                  <div
                    className="big-activity"
                    key={index}
                  >

                    <div className="big-activity-time">
                      {item.hour}
                    </div>

                    <div className="big-activity-icon">
                      ✓
                    </div>

                    <div>
                      <h3>{item.activity}</h3>
                      <p>
                        Activité enregistrée automatiquement.
                      </p>
                    </div>

                  </div>

                ))}

              </div>

            </div>

          </div>

        )}


        {/* ================= STATISTIQUES ================= */}

        {activePage === "Statistiques" && (

          <div className="page-content">

            <div className="page-title">
              <h2>Statistiques</h2>
              <p>
                Vue générale de l'activité du robot.
              </p>
            </div>

            <div className="statistics-grid">

              <div className="stat-box">
                <span>Conversations aujourd'hui</span>
                <strong>12</strong>
              </div>

              <div className="stat-box">
                <span>Interactions cette semaine</span>
                <strong>68</strong>
              </div>

              <div className="stat-box">
                <span>Alertes</span>
                <strong>1</strong>
              </div>

              <div className="stat-box">
                <span>État du robot</span>
                <strong className="green-text">
                  Normal
                </strong>
              </div>

            </div>

            <div className="panel chart-panel">

              <h2>
                Activité de la semaine
              </h2>

              <div className="fake-chart">

                <div style={{ height: "40%" }}></div>
                <div style={{ height: "65%" }}></div>
                <div style={{ height: "50%" }}></div>
                <div style={{ height: "80%" }}></div>
                <div style={{ height: "70%" }}></div>
                <div style={{ height: "90%" }}></div>
                <div style={{ height: "60%" }}></div>

              </div>

              <div className="chart-labels">
                <span>Lun</span>
                <span>Mar</span>
                <span>Mer</span>
                <span>Jeu</span>
                <span>Ven</span>
                <span>Sam</span>
                <span>Dim</span>
              </div>

            </div>

          </div>

        )}


        {/* ================= PROFIL ================= */}

        {activePage === "Profil patient" && (

          <div className="page-content">

            <div className="page-title">
              <h2>Profil patient</h2>
              <p>
                Informations générales du patient.
              </p>
            </div>

            <div className="profile-card">

              <div className="large-avatar">
                👴
              </div>

              <div className="profile-info">

                <h2>
                  Patient
                </h2>

                <p>
                  Profil utilisateur
                </p>

                <div className="profile-details">

                  <div>
                    <span>Statut</span>
                    <strong className="green-text">
                      Normal
                    </strong>
                  </div>

                  <div>
                    <span>Robot</span>
                    <strong>
                      Connecté
                    </strong>
                  </div>

                  <div>
                    <span>Dernière interaction</span>
                    <strong>
                      14:32
                    </strong>
                  </div>

                </div>

              </div>

            </div>

          </div>

        )}


        {/* ================= NOTIFICATIONS ================= */}

        {activePage === "Notifications" && (

          <div className="page-content">

            <div className="page-title">
              <h2>Notifications</h2>
              <p>
                Notifications importantes pour la famille.
              </p>
            </div>

            <div className="notification-list">

              <div className="notification-card">
                <span>🔔</span>
                <div>
                  <strong>Rappel médicament</strong>
                  <p>
                    Un rappel est prévu prochainement.
                  </p>
                </div>
              </div>

              <div className="notification-card">
                <span>✓</span>
                <div>
                  <strong>Robot opérationnel</strong>
                  <p>
                    Le robot fonctionne normalement.
                  </p>
                </div>
              </div>

            </div>

          </div>

        )}


        {/* ================= MEDECIN ================= */}

        {activePage === "Médecin" && (

          <div className="page-content">

            <div className="page-title">
              <h2>Espace médecin</h2>
              <p>
                Informations utiles au suivi du patient.
              </p>
            </div>

            <div className="doctor-grid">

              <div className="doctor-card">
                <span>⚕</span>
                <h3>Suivi patient</h3>
                <p>
                  Consulter l'état général et l'activité du patient.
                </p>
              </div>

              <div className="doctor-card">
                <span>📋</span>
                <h3>Historique</h3>
                <p>
                  Consulter les conversations et les événements importants.
                </p>
              </div>

              <div className="doctor-card">
                <span>📊</span>
                <h3>Statistiques</h3>
                <p>
                  Analyser l'activité du patient.
                </p>
              </div>

            </div>

          </div>

        )}


        {/* ================= PARAMETRES ================= */}

        {activePage === "Paramètres" && (

          <div className="page-content">

            <div className="page-title">
              <h2>Paramètres</h2>
              <p>
                Configuration du robot assistant.
              </p>
            </div>

            <div className="settings-panel">

              <div className="setting-row">

                <div>
                  <strong>Robot activé</strong>
                  <p>
                    Le robot peut interagir avec le patient.
                  </p>
                </div>

                <label className="switch">
                  <input
                    type="checkbox"
                    defaultChecked
                  />
                  <span></span>
                </label>

              </div>


              <div className="setting-row">

                <div>
                  <strong>Notifications famille</strong>
                  <p>
                    Recevoir les notifications importantes.
                  </p>
                </div>

                <label className="switch">
                  <input
                    type="checkbox"
                    defaultChecked
                  />
                  <span></span>
                </label>

              </div>


              <div className="setting-row">

                <div>
                  <strong>Rappels médicaments</strong>
                  <p>
                    Activer les rappels de médicaments.
                  </p>
                </div>

                <label className="switch">
                  <input
                    type="checkbox"
                    defaultChecked
                  />
                  <span></span>
                </label>

              </div>

            </div>

          </div>

        )}

      </main>

    </div>
  );
}

export default App;