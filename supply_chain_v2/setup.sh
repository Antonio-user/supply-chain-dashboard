#!/bin/bash
# Mise à jour des paquets
apt-get update

# Installation des dépendances système
apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    python3-venv \
    python3-pip

# Création d'un environnement virtuel
python3 -m venv /opt/venv
source /opt/venv/bin/activate

# Installation des dépendances Python
pip install --upgrade pip
pip install -r requirements.txt
