# 🚀 Guide de Démarrage Rapide

## Installation et Configuration

### 1. Prérequis
- Python 3.8+
- PostgreSQL 12+
- pip3

### 2. Installation automatique
```bash
# Rendre le script exécutable et lancer
chmod +x start.sh
./start.sh
```

### 3. Configuration manuelle (alternative)

#### Étape 1: Installer les dépendances
```bash
pip install -r requirements.txt
```

#### Étape 2: Configurer PostgreSQL
```bash
# Créer la base de données
createdb supply_chain_db

# Exécuter le schéma
psql -d supply_chain_db -f database/schema.sql
```

#### Étape 3: Configurer les variables d'environnement
```bash
cp .env.example .env
# Éditer .env avec vos paramètres de base de données
```

#### Étape 4: Générer des données de test
```bash
python etl/data_generator.py
```

#### Étape 5: Lancer le dashboard
```bash
streamlit run dashboard/app.py
```

## 🎯 Fonctionnalités Principales

### Dashboard Principal
- **KPIs temps réel** : Taux de service, stocks critiques, OTIF, valeur stock
- **Alertes automatiques** : Stocks critiques, retards de livraison
- **Visualisations interactives** : Graphiques, tableaux, métriques

### Modules IA
- **Prévision de demande** : Modèles ML pour anticiper les besoins
- **Détection d'anomalies** : Identification automatique des problèmes
- **Recommandations** : Suggestions d'actions correctives

### Exports et Rapports
- **Rapports Excel** : Export des données et analyses
- **Alertes email** : Notifications automatiques
- **Tableaux de bord** : Vues personnalisables

## 📊 Utilisation du Dashboard

### Navigation
1. **Onglet Alertes** : Vue des problèmes critiques
2. **Onglet Stocks** : Analyse détaillée des inventaires
3. **Onglet Prévisions** : Modèles prédictifs IA
4. **Onglet Performance** : Métriques et KPIs

### Filtres Disponibles
- **Période** : 7j, 30j, 90j, année
- **Entrepôt** : Sélection par site
- **Catégorie** : Filtrage par type de produit

### Actions Rapides
- **Actualiser** : Mise à jour des données
- **Générer rapport** : Export automatique
- **Entraîner IA** : Mise à jour des modèles

## 🔧 Personnalisation

### Ajout de Nouveaux KPIs
Modifiez `models/kpi_calculator.py` pour ajouter vos métriques.

### Configuration des Alertes
Ajustez les seuils dans `config/config.py`.

### Nouveaux Modèles IA
Étendez `models/ai_models.py` avec vos algorithmes.

## 🚨 Dépannage

### Problème de Connexion DB
```bash
# Vérifier PostgreSQL
sudo systemctl status postgresql

# Tester la connexion
psql -h localhost -U postgres -d supply_chain_db
```

### Erreurs de Dépendances
```bash
# Réinstaller les packages
pip install --upgrade -r requirements.txt
```

### Port Streamlit Occupé
```bash
# Utiliser un autre port
streamlit run dashboard/app.py --server.port 8502
```

## 📈 Optimisation Performance

### Base de Données
- Index sur les colonnes fréquemment utilisées
- Partitioning pour les grandes tables
- Maintenance régulière (VACUUM, ANALYZE)

### Dashboard
- Cache des requêtes fréquentes
- Pagination pour les gros datasets
- Optimisation des graphiques

## 🔐 Sécurité

### Variables Sensibles
- Utilisez des variables d'environnement
- Ne commitez jamais les mots de passe
- Chiffrement des connexions DB

### Accès Dashboard
- Authentification Streamlit (optionnel)
- Reverse proxy pour la production
- HTTPS recommandé

## 📞 Support

Pour toute question ou problème :
1. Consultez les logs dans `logs/`
2. Vérifiez la configuration dans `.env`
3. Testez la connexion DB avec `python database/db_connection.py`
