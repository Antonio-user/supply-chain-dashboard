"""Configuration centralisée pour l'application Supply Chain"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration de l'application"""
    
    # Base de données
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'supply_chain_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    # Interface
    PAGE_TITLE = "Supply Chain Management Dashboard"
    PAGE_ICON = "🚚"
    LAYOUT = "wide"
    
    # Pagination
    ITEMS_PER_PAGE = 50
    
    # KPIs
    STOCK_CRITICAL_THRESHOLD = 0.8
    OTIF_TARGET = 95.0
    SERVICE_LEVEL_TARGET = 98.0
    
    # Exports
    EXPORT_PATH = 'exports/'
    
    @classmethod
    def validate(cls):
        """Valide la configuration"""
        required = ['DB_HOST', 'DB_NAME', 'DB_USER']
        missing = [var for var in required if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Variables manquantes: {', '.join(missing)}")
        return True
