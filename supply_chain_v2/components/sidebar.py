"""Composant de barre latérale pour la navigation"""
import streamlit as st
from datetime import datetime

def render_sidebar():
    """Affiche la barre latérale de navigation professionnelle"""
    
    with st.sidebar:
        # Logo et titre
        st.markdown("""
        <div style="
            text-align: center;
            padding: 1.5rem 0;
            background: linear-gradient(135deg, #2563eb 0%, #8b5cf6 100%);
            margin: -1rem -1rem 2rem -1rem;
            border-radius: 0 0 1rem 1rem;
        ">
            <h2 style="
                color: white;
                margin: 0;
                font-weight: 700;
                font-size: 1.5rem;
                text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            ">
                <i class="fas fa-truck" style="margin-right: 0.5rem;"></i>
                Supply Chain
            </h2>
            <p style="
                color: rgba(255,255,255,0.8);
                margin: 0.5rem 0 0 0;
                font-size: 0.875rem;
                font-weight: 500;
            ">Management Dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Menu de navigation moderne
        st.markdown("### 🧭 Navigation")
        
        # Options de menu avec icônes et descriptions
        menu_options = {
            "dashboard": {
                "icon": "tachometer-alt",
                "title": "Tableau de Bord",
                "desc": "Vue d'ensemble et KPIs"
            },
            "stocks": {
                "icon": "boxes",
                "title": "Gestion des Stocks",
                "desc": "Inventaire et mouvements"
            },
            "orders": {
                "icon": "clipboard-list",
                "title": "Gestion des Commandes",
                "desc": "Commandes et livraisons"
            },
            "products": {
                "icon": "tags",
                "title": "Gestion des Produits",
                "desc": "Catalogue et références"
            },
            "warehouses": {
                "icon": "warehouse",
                "title": "Gestion des Entrepôts",
                "desc": "Sites et capacités"
            },
            "suppliers": {
                "icon": "handshake",
                "title": "Gestion des Fournisseurs",
                "desc": "Partenaires et contacts"
            },
            "clients": {
                "icon": "users",
                "title": "Gestion des Clients",
                "desc": "Base clients et relations"
            }
        }
        
        # Sélection de page avec style personnalisé
        selected_page = None
        for page_key, page_info in menu_options.items():
            if st.button(
                f"🔹 {page_info['title']}",
                key=f"nav_{page_key}",
                help=page_info['desc'],
                use_container_width=True
            ):
                selected_page = page_key
                st.session_state.current_page = page_key
        
        # Récupérer la page courante
        current_page = selected_page or st.session_state.get('current_page', 'dashboard')
        
        # Affichage de la page active
        if current_page in menu_options:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
                padding: 1rem;
                border-radius: 0.75rem;
                border-left: 4px solid #2563eb;
                margin: 1rem 0;
            ">
                <div style="
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    margin-bottom: 0.5rem;
                ">
                    <i class="fas fa-{menu_options[current_page]['icon']}" style="color: #2563eb;"></i>
                    <strong style="color: #1e40af;">{menu_options[current_page]['title']}</strong>
                </div>
                <small style="color: #3730a3;">{menu_options[current_page]['desc']}</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Statistiques rapides
        st.markdown("### 📊 Aperçu Rapide")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Produits", "1,234", "+12")
        with col2:
            st.metric("Commandes", "567", "+8")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Clients", "89", "+3")
        with col2:
            st.metric("Entrepôts", "5", "0")
        
        st.markdown("---")
        
        # Informations système avec style
        st.markdown("### ℹ️ Informations Système")
        
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            padding: 1rem;
            border-radius: 0.75rem;
            border-left: 4px solid #10b981;
        ">
            <div style="margin-bottom: 0.5rem;">
                <strong style="color: #065f46;">Version:</strong>
                <span style="color: #047857;">v2.0.0 Pro</span>
            </div>
            <div style="margin-bottom: 0.5rem;">
                <strong style="color: #065f46;">Status:</strong>
                <span style="color: #047857;">✅ Connecté</span>
            </div>
            <div style="margin-bottom: 0.5rem;">
                <strong style="color: #065f46;">Date:</strong>
                <span style="color: #047857;">{current_date}</span>
            </div>
            <div>
                <strong style="color: #065f46;">Heure:</strong>
                <span style="color: #047857;">{current_time}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bouton d'aide
        st.markdown("---")
        if st.button("❓ Aide & Support", use_container_width=True):
            st.info("""
            **Guide d'utilisation:**
            
            1. **Navigation:** Utilisez les boutons ci-dessus
            2. **CRUD:** Créer, lire, modifier, supprimer
            3. **Import:** Utilisez les onglets CSV
            4. **Export:** Téléchargez vos données
            
            **Support:** admin@supplychain.com
            """)
        
        return current_page
