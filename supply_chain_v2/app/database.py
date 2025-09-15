"""Gestionnaire de base de données pour l'application Supply Chain"""
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import psycopg2
from app.config import Config

class DatabaseManager:
    """Gestionnaire de base de données centralisé"""
    
    def __init__(self):
        self.engine = None
        self.connection = None
        self.config = Config()
        
    def connect(self):
        """Connexion à la base de données avec gestion d'erreurs robuste"""
        try:
            # Fermer l'ancienne connexion si elle existe
            if hasattr(self, 'connection') and self.connection:
                try:
                    self.connection.close()
                except:
                    pass
            
            self.connection = psycopg2.connect(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                database=self.config.DB_NAME,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD,
                connect_timeout=10
            )
            
            # Configurer l'autocommit pour éviter les problèmes de transaction
            self.connection.autocommit = False
            
            print("✅ Connexion à la base réussie")
            return True
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            self.connection = None
            return False
    
    def execute_query(self, query, params=None):
        """Exécute une requête SQL avec gestion d'erreurs améliorée"""
        max_retries = 2
        
        for attempt in range(max_retries):
            try:
                if not self.connection or self.connection.closed:
                    if not self.connect():
                        return None
                
                # Exécuter la requête directement avec psycopg2
                cursor = self.connection.cursor()
                
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # Commit pour les opérations d'insertion/modification
                self.connection.commit()
                
                # Retourner les résultats si c'est un SELECT
                if query.strip().upper().startswith('SELECT'):
                    results = cursor.fetchall()
                    cursor.close()
                    return results
                else:
                    cursor.close()
                    return True  # Succès pour INSERT/UPDATE/DELETE
                    
            except Exception as e:
                print(f"❌ Tentative {attempt + 1} échouée: {e}")
                
                # Rollback en cas d'erreur
                try:
                    self.connection.rollback()
                except:
                    pass
                
                # Fermer et reconnecter pour la prochaine tentative
                try:
                    self.connection.close()
                except:
                    pass
                
                if attempt < max_retries - 1:
                    print(f"🔄 Tentative de reconnexion...")
                    if not self.connect():
                        continue
                else:
                    print(f"❌ Échec définitif après {max_retries} tentatives")
                    return None
        
        return None
    
    def fetch_dataframe(self, query, params=None):
        """Récupère les données dans un DataFrame"""
        try:
            if not self.connection or self.connection.closed:
                if not self.connect():
                    return pd.DataFrame()
            
            # Utiliser psycopg2 directement pour plus de stabilité
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Récupérer les résultats et les noms de colonnes
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            cursor.close()
            
            # Créer le DataFrame
            df = pd.DataFrame(results, columns=columns)
            return df
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des données: {e}")
            # Tenter une reconnexion
            try:
                if self.connect():
                    cursor = self.connection.cursor()
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    results = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description] if cursor.description else []
                    cursor.close()
                    return pd.DataFrame(results, columns=columns)
            except Exception as e2:
                print(f"❌ Erreur de reconnexion: {e2}")
            
            return pd.DataFrame()
    
    def close(self):
        """Ferme la connexion"""
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()

# Instance globale
db = DatabaseManager()
