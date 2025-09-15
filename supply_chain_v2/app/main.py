"""Point d'entrée principal de l'application Supply Chain Dashboard"""
import streamlit as st
import sys
import os

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import Config
from app.database import db
from components.sidebar import render_sidebar
from pages import dashboard, stocks, orders, products, warehouses, suppliers, clients

# Configuration de la page
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout=Config.LAYOUT,
    initial_sidebar_state="expanded"
)

# CSS personnalisé professionnel
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
    
    /* Variables CSS */
    :root {
        --primary-color: #2563eb;
        --primary-dark: #1d4ed8;
        --secondary-color: #64748b;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --background-light: #f8fafc;
        --background-white: #ffffff;
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --border-color: #e2e8f0;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    /* Reset et base */
    * {
        box-sizing: border-box;
    }
    
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
    }
    
    /* En-tête principal */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        color: var(--text-primary);
        text-align: center;
        margin: 2rem 0 3rem 0;
        background: linear-gradient(135deg, var(--primary-color) 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        position: relative;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(135deg, var(--primary-color) 0%, #8b5cf6 100%);
        border-radius: 2px;
    }
    
    /* Sections */
    .section-header {
        font-size: 1.875rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 2rem 0 1.5rem 0;
        padding: 1rem 0 0.75rem 0;
        border-bottom: 3px solid var(--primary-color);
        position: relative;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .section-header::before {
        content: '';
        width: 6px;
        height: 30px;
        background: linear-gradient(135deg, var(--primary-color) 0%, #8b5cf6 100%);
        border-radius: 3px;
    }
    
    /* Cards et containers */
    .metric-card {
        background: var(--background-white);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--border-color);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, var(--primary-color) 0%, #8b5cf6 100%);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
        border-color: var(--primary-color);
    }
    
    .form-container {
        background: var(--background-white);
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--border-color);
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .form-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, var(--success-color) 0%, #06b6d4 100%);
    }
    
    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.875rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-md);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4);
        background: linear-gradient(135deg, var(--primary-dark) 0%, #1e40af 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: var(--shadow-sm);
    }
    
    /* Boutons spécialisés */
    .edit-button {
        background: linear-gradient(135deg, var(--warning-color) 0%, #f97316 100%) !important;
    }
    
    .delete-button {
        background: linear-gradient(135deg, var(--error-color) 0%, #dc2626 100%) !important;
    }
    
    .success-button {
        background: linear-gradient(135deg, var(--success-color) 0%, #059669 100%) !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--background-white) 0%, #f8fafc 100%);
        border-right: 1px solid var(--border-color);
    }
    
    .sidebar .stSelectbox {
        margin-bottom: 1.5rem;
    }
    
    .sidebar .stSelectbox > div > div {
        background: var(--background-white);
        border: 2px solid var(--border-color);
        border-radius: 12px;
        transition: all 0.2s ease;
    }
    
    .sidebar .stSelectbox > div > div:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    /* DataFrames */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--border-color);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--background-white);
        padding: 0.5rem;
        border-radius: 12px;
        box-shadow: var(--shadow-sm);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: white;
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border: 2px solid var(--border-color);
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 0.875rem;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    /* Métriques */
    .metric {
        background: var(--background-white);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: var(--shadow-md);
        border-left: 4px solid var(--primary-color);
        transition: all 0.2s ease;
    }
    
    .metric:hover {
        transform: translateX(4px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Alertes et messages */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: var(--shadow-md);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-left: 4px solid var(--success-color);
    }
    
    .stError {
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
        border-left: 4px solid var(--error-color);
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fffbeb 0%, #fed7aa 100%);
        border-left: 4px solid var(--warning-color);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .section-header {
            font-size: 1.5rem;
        }
        
        .metric-card,
        .form-container {
            padding: 1.5rem;
        }
    }
    
    /* Scrollbar personnalisée */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--background-light);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--secondary-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-color);
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Fonction principale de l'application"""
    
    # Vérification de la configuration
    try:
        Config.validate()
    except ValueError as e:
        st.error(f"❌ Erreur de configuration: {e}")
        st.stop()
    
    # Connexion à la base de données
    if not db.connect():
        st.error("❌ Impossible de se connecter à la base de données")
        st.info("Vérifiez que PostgreSQL est démarré et configuré dans .env")
        st.stop()
    
    # En-tête principal avec animation
    st.markdown('''
    <div class="fade-in">
        <h1 class="main-header">
            <i class="fas fa-truck" style="margin-right: 1rem; color: #2563eb;"></i>
            Supply Chain Management Dashboard
        </h1>
    </div>
    ''', unsafe_allow_html=True)
    
    # Barre latérale
    page = render_sidebar()
    
    # Routage des pages
    if page == "dashboard":
        dashboard.render()
    elif page == "stocks":
        stocks.render()
    elif page == "orders":
        orders.render()
    elif page == "products":
        products.render()
    elif page == "warehouses":
        warehouses.render()
    elif page == "suppliers":
        suppliers.render()
    elif page == "clients":
        clients.render()
    
    # Note: Connexion fermée automatiquement par Streamlit

if __name__ == "__main__":
    main()
