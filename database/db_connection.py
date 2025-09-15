import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.db_url = os.getenv('DB_URL')
        self.engine = None
        self.connection = None
        
    def connect(self):
        """Établit la connexion à la base de données"""
        try:
            self.engine = create_engine(self.db_url)
            self.connection = self.engine.connect()
            print("✅ Connexion à la base de données établie")
            return True
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            return False
    
    def execute_query(self, query, params=None):
        """Exécute une requête SQL"""
        try:
            from sqlalchemy import text
            if params:
                result = self.connection.execute(text(query), params)
            else:
                result = self.connection.execute(text(query))
            self.connection.commit()
            return result
        except Exception as e:
            print(f"❌ Erreur d'exécution: {e}")
            return None
    
    def query(self, query, params=None):
        """Alias pour execute_query qui retourne les résultats"""
        try:
            from sqlalchemy import text
            if params:
                result = self.connection.execute(text(query), params)
            else:
                result = self.connection.execute(text(query))
            return result.fetchall()
        except Exception as e:
            print(f"❌ Erreur de requête: {e}")
            return []
    
    def read_to_dataframe(self, query, params=None):
        """Lit les données dans un DataFrame pandas"""
        try:
            from sqlalchemy import text
            if params:
                df = pd.read_sql(text(query), self.engine, params=params)
            else:
                df = pd.read_sql(text(query), self.engine)
            print(f"✅ DataFrame créé avec {len(df)} lignes")
            return df
        except Exception as e:
            print(f"❌ Erreur de lecture: {e}")
            return pd.DataFrame()
    
    def write_dataframe(self, df, table_name, if_exists='append'):
        """Écrit un DataFrame dans une table"""
        try:
            df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
            print(f"✅ Données insérées dans {table_name}")
            return True
        except Exception as e:
            print(f"❌ Erreur d'insertion: {e}")
            return False
    
    def close(self):
        """Ferme la connexion"""
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()
        print("🔒 Connexion fermée")

# Instance globale
db = DatabaseConnection()
