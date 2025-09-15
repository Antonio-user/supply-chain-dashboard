# Tableau de Bord Intelligent Supply Chain

## 🎯 Objectif
Tableau de bord centralisé offrant une vision temps réel des indicateurs clés de la supply chain avec recommandations intelligentes.

## 🏗️ Architecture
- **Base de données** : PostgreSQL (stockage centralisé)
- **ETL** : Scripts Python pour extraction/transformation/chargement
- **Traitement** : Pandas pour calculs KPIs et feature engineering
- **IA** : scikit-learn pour prédictions et détection d'anomalies
- **Dashboard** : Streamlit (interface professionnelle)

## 📊 Fonctionnalités
- Vue one-page avec KPIs essentiels
- Alertes automatiques (ruptures, retards)
- Prévisions demande pour top SKUs
- Export rapports pour managers

## 🚀 Installation
```bash
pip install -r requirements.txt
```

## 📁 Structure du projet
```
├── data/               # Données sources (CSV, exports)
├── database/          # Scripts création/migration DB
├── etl/               # Scripts extraction/transformation
├── models/            # Modèles IA et prédictions
├── dashboard/         # Interface Streamlit
└── config/            # Configuration et variables
```

## 🔧 Configuration
1. Configurer PostgreSQL
2. Ajuster variables dans `.env`
3. Lancer ETL initial
4. Démarrer dashboard : `streamlit run dashboard/app.py`
