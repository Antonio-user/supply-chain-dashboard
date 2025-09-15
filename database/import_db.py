#!/usr/bin/env python3
"""
Script d'import pour PostgreSQL
Crée la base de données, le schéma et importe les données de démonstration
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import subprocess

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_connection import DatabaseConnection
from etl.data_generator import DataGenerator

class PostgreSQLImporter:
    def __init__(self):
        """Initialise l'importeur PostgreSQL"""
        load_dotenv()
        
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'supply_chain_db')
        }
        
        self.schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
        
    def check_postgresql_service(self):
        """Vérifie si PostgreSQL est en cours d'exécution"""
        print("🔍 Vérification du service PostgreSQL...")
        
        try:
            # Tenter de se connecter à PostgreSQL
            conn = psycopg2.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                database='postgres'  # Base par défaut
            )
            conn.close()
            print("✅ PostgreSQL est accessible")
            return True
        except psycopg2.OperationalError as e:
            print(f"❌ Erreur de connexion PostgreSQL: {e}")
            print("\n📋 Instructions pour démarrer PostgreSQL:")
            print("   • Ubuntu/Debian: sudo systemctl start postgresql")
            print("   • CentOS/RHEL: sudo systemctl start postgresql")
            print("   • macOS: brew services start postgresql")
            print("   • Windows: net start postgresql-x64-xx")
            return False
    
    def create_database(self):
        """Crée la base de données si elle n'existe pas"""
        print(f"🗄️ Création de la base de données '{self.db_config['database']}'...")
        
        try:
            # Connexion à la base postgres par défaut
            conn = psycopg2.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                database='postgres'
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Vérifier si la base existe
            cursor.execute(
                "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
                (self.db_config['database'],)
            )
            
            if cursor.fetchone():
                print(f"✅ La base de données '{self.db_config['database']}' existe déjà")
            else:
                # Créer la base de données
                cursor.execute(f"CREATE DATABASE {self.db_config['database']}")
                print(f"✅ Base de données '{self.db_config['database']}' créée avec succès")
            
            cursor.close()
            conn.close()
            return True
            
        except psycopg2.Error as e:
            print(f"❌ Erreur lors de la création de la base: {e}")
            return False
    
    def import_schema(self):
        """Importe le schéma SQL"""
        print("📋 Import du schéma SQL...")
        
        if not os.path.exists(self.schema_file):
            print(f"❌ Fichier schema.sql introuvable: {self.schema_file}")
            return False
        
        try:
            # Connexion à la base de données cible
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Lire et exécuter le fichier SQL
            with open(self.schema_file, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            # Exécuter le schéma par blocs
            sql_commands = schema_sql.split(';')
            
            for command in sql_commands:
                command = command.strip()
                if command:
                    try:
                        cursor.execute(command)
                    except psycopg2.Error as e:
                        # Ignorer les erreurs de tables/index déjà existants
                        if "already exists" not in str(e):
                            print(f"⚠️ Avertissement SQL: {e}")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print("✅ Schéma importé avec succès")
            return True
            
        except psycopg2.Error as e:
            print(f"❌ Erreur lors de l'import du schéma: {e}")
            return False
    
    def generate_demo_data(self):
        """Génère et importe les données de démonstration"""
        print("📊 Génération des données de démonstration...")
        
        try:
            # Utiliser le générateur de données existant
            generator = DataGenerator()
            
            if generator.connect_db():
                print("✅ Connexion à la base établie")
                
                # Générer les données
                generator.generate_all_data()
                print("✅ Données de démonstration générées avec succès")
                
                generator.close_connection()
                return True
            else:
                print("❌ Impossible de se connecter à la base pour générer les données")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de la génération des données: {e}")
            return False
    
    def verify_installation(self):
        """Vérifie que l'installation s'est bien déroulée"""
        print("🔍 Vérification de l'installation...")
        
        try:
            db = DatabaseConnection()
            if db.connect():
                # Vérifier quelques tables clés
                tables_to_check = ['warehouses', 'skus', 'inventory', 'orders']
                
                for table in tables_to_check:
                    result = db.query(f"SELECT COUNT(*) FROM {table}")
                    count = result[0][0] if result else 0
                    print(f"  📋 Table {table}: {count} enregistrements")
                
                db.close()
                print("✅ Installation vérifiée avec succès")
                return True
            else:
                print("❌ Impossible de vérifier l'installation")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de la vérification: {e}")
            return False
    
    def run_import(self):
        """Exécute l'import complet"""
        print("🚀 Démarrage de l'import PostgreSQL")
        print("=" * 50)
        
        steps = [
            ("Vérification PostgreSQL", self.check_postgresql_service),
            ("Création base de données", self.create_database),
            ("Import du schéma", self.import_schema),
            ("Génération données démo", self.generate_demo_data),
            ("Vérification installation", self.verify_installation)
        ]
        
        for step_name, step_func in steps:
            print(f"\n📌 {step_name}...")
            if not step_func():
                print(f"❌ Échec à l'étape: {step_name}")
                return False
        
        print("\n" + "=" * 50)
        print("🎉 Import PostgreSQL terminé avec succès!")
        print("\n📋 Prochaines étapes:")
        print("   1. Vérifiez votre fichier .env avec les bonnes informations de connexion")
        print("   2. Lancez le dashboard: python dashboard/app.py")
        print("   3. Ou lancez la démo: python demo_dashboard.py")
        
        return True

def main():
    """Fonction principale"""
    print("🗄️ Script d'import PostgreSQL pour Supply Chain Dashboard")
    print("=" * 60)
    
    # Vérifier si le fichier .env existe
    if not os.path.exists('.env'):
        print("⚠️ Fichier .env non trouvé")
        print("📋 Copiez .env.example vers .env et configurez vos paramètres:")
        print("   cp .env.example .env")
        print("   # Puis éditez .env avec vos paramètres PostgreSQL")
        return
    
    importer = PostgreSQLImporter()
    
    try:
        success = importer.run_import()
        if success:
            print("\n🚀 Vous pouvez maintenant lancer l'application!")
        else:
            print("\n❌ L'import a échoué. Vérifiez les messages d'erreur ci-dessus.")
            
    except KeyboardInterrupt:
        print("\n⏹️ Import interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    main()
