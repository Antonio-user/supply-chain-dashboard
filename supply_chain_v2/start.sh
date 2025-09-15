#!/bin/bash

# Script de démarrage pour Supply Chain Dashboard v2.0
echo "🚚 Démarrage du Supply Chain Dashboard v2.0..."

# Vérification de Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Vérification du répertoire
if [ ! -f "app/main.py" ]; then
    echo "❌ Fichier app/main.py non trouvé"
    echo "Assurez-vous d'être dans le répertoire supply_chain_v2/"
    exit 1
fi

# Vérification du fichier .env
if [ ! -f ".env" ]; then
    echo "⚠️  Fichier .env non trouvé"
    echo "Copiez .env.example vers .env et configurez vos paramètres"
    cp .env.example .env
    echo "✅ Fichier .env créé à partir de .env.example"
fi

# Installation des dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# Démarrage de l'application
echo "🚀 Lancement de l'application..."
echo "📍 URL: http://localhost:8501"
echo "⏹️  Arrêt: Ctrl+C"
echo ""

streamlit run app/main.py --server.port 8501 --server.address 0.0.0.0
