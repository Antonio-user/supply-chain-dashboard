"""Page de gestion des commandes"""
import streamlit as st
from app.database import db

def render():
    """Affiche la page de gestion des commandes"""
    
    st.markdown('<h2 class="section-header">📋 Gestion des Commandes</h2>', 
                unsafe_allow_html=True)
    
    try:
        orders_query = """
            SELECT order_id, order_number, customer_id, order_date, 
                   status, priority, total_value
            FROM orders
            ORDER BY order_date DESC
            LIMIT 100
        """
        orders_df = db.fetch_dataframe(orders_query)
        
        if not orders_df.empty:
            tab1, tab2 = st.tabs(["📊 Liste", "➕ Nouvelle"])
            
            with tab1:
                st.dataframe(orders_df, width='stretch')
            
            with tab2:
                with st.form("new_order"):
                    order_number = st.text_input("N° Commande *")
                    customer_id = st.text_input("Client *")
                    status = st.selectbox("Statut:", ["PENDING", "PROCESSING", "SHIPPED"])
                    
                    if st.form_submit_button("Créer"):
                        if order_number and customer_id:
                            try:
                                query = """
                                    INSERT INTO orders (order_number, customer_id, status)
                                    VALUES (%s, %s, %s)
                                """
                                db.execute_query(query, (order_number, customer_id, status))
                                st.success("✅ Commande créée!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erreur: {e}")
        else:
            st.warning("Aucune commande trouvée")
    
    except Exception as e:
        st.error(f"Erreur: {e}")
