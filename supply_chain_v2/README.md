# 🚚 Supply Chain Management Dashboard V2

## Architecture Propre et Modulaire

### Structure du Projet
```
supply_chain_v2/
├── app/
│   ├── __init__.py
│   ├── main.py              # Point d'entrée principal
│   ├── config.py            # Configuration centralisée
│   └── database.py          # Gestion base de données
├── pages/
│   ├── __init__.py
│   ├── dashboard.py         # Page d'accueil
│   ├── stocks.py           # Gestion des stocks
│   ├── orders.py           # Gestion des commandes
│   ├── products.py         # Gestion des produits
│   ├── warehouses.py       # Gestion des entrepôts
│   ├── suppliers.py        # Gestion des fournisseurs
│   └── clients.py          # Gestion des clients
├── components/
│   ├── __init__.py
│   ├── sidebar.py          # Barre latérale
│   ├── forms.py            # Formulaires réutilisables
│   ├── charts.py           # Graphiques
│   └── tables.py           # Tableaux
├── services/
│   ├── __init__.py
│   ├── data_service.py     # Service de données
│   ├── kpi_service.py      # Calcul des KPIs
│   └── export_service.py   # Exports
├── utils/
│   ├── __init__.py
│   ├── helpers.py          # Fonctions utilitaires
│   └── validators.py       # Validation des données
├── static/
│   └── styles.css          # Styles CSS
├── requirements.txt
└── .env.example
```

### Fonctionnalités
- ✅ Architecture modulaire et maintenable
- ✅ Séparation des responsabilités
- ✅ Code réutilisable et testable
- ✅ Interface moderne et responsive
- ✅ CRUD complet pour tous les modules
- ✅ Gestion d'erreurs robuste
- ✅ Configuration centralisée

### Installation
```bash
cd supply_chain_v2
pip install -r requirements.txt
cp .env.example .env
# Configurer .env avec vos paramètres
streamlit run app/main.py
```
