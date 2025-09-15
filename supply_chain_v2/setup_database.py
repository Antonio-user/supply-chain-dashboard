#!/usr/bin/env python3
"""Script pour configurer et mettre à jour la base de données Supply Chain"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Charger les variables d'environnement
load_dotenv()

def get_db_connection():
    """Créer une connexion à la base de données"""
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'supply_chain_db')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', '')
    
    db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    
    try:
        engine = create_engine(db_url)
        return engine
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return None

def execute_sql_file(engine, file_path):
    """Exécuter un fichier SQL"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        with engine.connect() as conn:
            # Diviser le contenu en statements individuels
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            for statement in statements:
                if statement:
                    try:
                        conn.execute(text(statement))
                        conn.commit()
                    except Exception as e:
                        print(f"⚠️  Avertissement lors de l'exécution: {e}")
                        continue
        
        print(f"✅ Fichier {file_path} exécuté avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution de {file_path}: {e}")
        return False

def check_tables(engine):
    """Vérifier quelles tables existent"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            tables = [row[0] for row in result]
            print(f"📋 Tables existantes: {', '.join(tables)}")
            return tables
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des tables: {e}")
        return []

def add_sample_data(engine):
    """Ajouter des données d'exemple"""
    sample_data = [
        # Entrepôts
        """INSERT INTO warehouses (warehouse_name, location, capacity_m3) 
           VALUES ('Entrepôt Paris', 'Paris, France', 1000.0),
                  ('Entrepôt Lyon', 'Lyon, France', 800.0),
                  ('Entrepôt Marseille', 'Marseille, France', 1200.0)
           ON CONFLICT DO NOTHING""",
        
        # Produits
        """INSERT INTO skus (sku_code, product_name, category, unit_cost, description)
           VALUES ('SKU001', 'Ordinateur Portable', 'Électronique', 800.00, 'Ordinateur portable 15 pouces'),
                  ('SKU002', 'Souris Sans Fil', 'Électronique', 25.00, 'Souris optique sans fil'),
                  ('SKU003', 'Clavier Mécanique', 'Électronique', 120.00, 'Clavier mécanique RGB'),
                  ('SKU004', 'Écran 24 pouces', 'Électronique', 200.00, 'Moniteur LED 24 pouces Full HD')
           ON CONFLICT DO NOTHING""",
        
        # Fournisseurs
        """INSERT INTO suppliers (supplier_name, contact_person, email, phone, address, country)
           VALUES ('TechSupply France', 'Jean Dupont', 'contact@techsupply.fr', '01.23.45.67.89', '123 Rue de la Tech, Paris', 'France'),
                  ('ElectroWorld', 'Marie Martin', 'info@electroworld.com', '04.56.78.90.12', '456 Avenue des Composants, Lyon', 'France')
           ON CONFLICT DO NOTHING""",
        
        # Clients
        """INSERT INTO customers (customer_name, contact_person, email, phone, address, city, country)
           VALUES ('Entreprise ABC', 'Pierre Durand', 'pierre@abc-corp.fr', '01.11.22.33.44', '789 Boulevard du Commerce', 'Paris', 'France'),
                  ('Société XYZ', 'Sophie Leblanc', 'sophie@xyz-company.fr', '04.55.66.77.88', '321 Rue de l\'Innovation', 'Lyon', 'France'),
                  ('StartUp Tech', 'Marc Rousseau', 'marc@startup-tech.fr', '02.99.88.77.66', '654 Avenue du Numérique', 'Nantes', 'France')
           ON CONFLICT DO NOTHING""",
        
        # Commandes
        """INSERT INTO orders (order_number, customer_id, order_date, required_date, status, priority, total_value)
           VALUES ('ORD-2024-001', '1', CURRENT_DATE - INTERVAL '5 days', CURRENT_DATE + INTERVAL '2 days', 'PROCESSING', 'HIGH', 1500.00),
                  ('ORD-2024-002', '2', CURRENT_DATE - INTERVAL '3 days', CURRENT_DATE + INTERVAL '5 days', 'PENDING', 'NORMAL', 800.00),
                  ('ORD-2024-003', '3', CURRENT_DATE - INTERVAL '1 day', CURRENT_DATE + INTERVAL '7 days', 'PENDING', 'LOW', 345.00)
           ON CONFLICT DO NOTHING""",
        
        # Stock initial
        """INSERT INTO inventory (warehouse_id, sku_id, quantity_available, safety_stock, reorder_point)
           VALUES (1, 1, 50, 10, 20),
                  (1, 2, 200, 50, 100),
                  (1, 3, 75, 15, 30),
                  (1, 4, 30, 5, 15),
                  (2, 1, 30, 10, 20),
                  (2, 2, 150, 50, 100),
                  (3, 3, 40, 15, 30),
                  (3, 4, 25, 5, 15)
           ON CONFLICT DO NOTHING"""
    ]
    
    try:
        with engine.connect() as conn:
            for query in sample_data:
                try:
                    conn.execute(text(query))
                    conn.commit()
                except Exception as e:
                    print(f"⚠️  Avertissement données d'exemple: {e}")
                    continue
        
        print("✅ Données d'exemple ajoutées")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout des données d'exemple: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚚 Configuration de la base de données Supply Chain...")
    
    # Connexion à la base de données
    engine = get_db_connection()
    if not engine:
        print("❌ Impossible de se connecter à la base de données")
        sys.exit(1)
    
    print("✅ Connexion à la base de données réussie")
    
    # Vérifier les tables existantes
    existing_tables = check_tables(engine)
    
    # Exécuter le script de mise à jour
    if os.path.exists('update_schema.sql'):
        print("📝 Exécution du script de mise à jour...")
        execute_sql_file(engine, 'update_schema.sql')
    
    # Vérifier à nouveau les tables
    print("\n📋 Vérification après mise à jour:")
    updated_tables = check_tables(engine)
    
    # Ajouter des données d'exemple si les tables sont vides
    print("\n📊 Ajout de données d'exemple...")
    add_sample_data(engine)
    
    print("\n✅ Configuration terminée!")
    print("🌐 Vous pouvez maintenant démarrer l'application avec: ./start.sh")

if __name__ == "__main__":
    main()
