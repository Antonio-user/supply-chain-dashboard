"""Page de gestion des entrepôts"""
import streamlit as st
from app.database import db

def render():
    """Affiche la page de gestion des entrepôts"""
    
    st.markdown('<h2 class="section-header">🏭 Gestion des Entrepôts</h2>', 
                unsafe_allow_html=True)
    
    try:
        warehouses_query = """
            SELECT warehouse_id, warehouse_name, location, capacity_m3
            FROM warehouses
            ORDER BY warehouse_name
        """
        warehouses_df = db.fetch_dataframe(warehouses_query)
        
        if not warehouses_df.empty:
            tab1, tab2, tab3 = st.tabs(["📊 Liste", "➕ Nouveau", "📁 Import CSV"])
            
            with tab1:
                # Actions CRUD
                if st.checkbox("Mode édition"):
                    selected_warehouse = st.selectbox(
                        "Sélectionner un entrepôt:",
                        options=warehouses_df['warehouse_id'].tolist(),
                        format_func=lambda x: f"{warehouses_df[warehouses_df['warehouse_id']==x]['warehouse_name'].iloc[0]}"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✏️ Modifier"):
                            st.session_state.edit_warehouse = selected_warehouse
                    with col2:
                        if st.button("🗑️ Supprimer"):
                            st.session_state.delete_warehouse = selected_warehouse
                
                # Formulaire de modification
                if 'edit_warehouse' in st.session_state:
                    warehouse_data = warehouses_df[warehouses_df['warehouse_id'] == st.session_state.edit_warehouse].iloc[0]
                    st.markdown("### ✏️ Modifier l'Entrepôt")
                    with st.form("edit_warehouse_form"):
                        col1, col2 = st.columns(2)
                        with col1:
                            new_warehouse_name = st.text_input("Nom Entrepôt:", value=warehouse_data['warehouse_name'])
                            new_location = st.text_input("Localisation:", value=warehouse_data['location'])
                        with col2:
                            new_capacity_m3 = st.number_input("Capacité (m³):", value=float(warehouse_data['capacity_m3']))
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("💾 Sauvegarder"):
                                try:
                                    update_query = "UPDATE warehouses SET warehouse_name = %s, location = %s, capacity_m3 = %s WHERE warehouse_id = %s"
                                    db.execute_query(update_query, (new_warehouse_name, new_location, new_capacity_m3, st.session_state.edit_warehouse))
                                    st.success("✅ Entrepôt modifié!")
                                    del st.session_state.edit_warehouse
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Erreur: {e}")
                        with col_cancel:
                            if st.form_submit_button("❌ Annuler"):
                                del st.session_state.edit_warehouse
                                st.rerun()
                
                # Confirmation de suppression
                if 'delete_warehouse' in st.session_state:
                    warehouse_data = warehouses_df[warehouses_df['warehouse_id'] == st.session_state.delete_warehouse].iloc[0]
                    st.warning(f"⚠️ Supprimer l'entrepôt **{warehouse_data['warehouse_name']}** ?")
                    col_confirm, col_cancel = st.columns(2)
                    with col_confirm:
                        if st.button("🗑️ Confirmer"):
                            try:
                                db.execute_query("DELETE FROM warehouses WHERE warehouse_id = %s", (st.session_state.delete_warehouse,))
                                st.success("✅ Entrepôt supprimé!")
                                del st.session_state.delete_warehouse
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erreur: {e}")
                    with col_cancel:
                        if st.button("❌ Annuler"):
                            del st.session_state.delete_warehouse
                            st.rerun()
                
                st.dataframe(
                    warehouses_df,
                    column_config={
                        'warehouse_name': 'Nom Entrepôt',
                        'location': 'Localisation',
                        'capacity_m3': 'Capacité (m³)'
                    },
                    width='stretch'
                )
            
            with tab2:
                with st.form("new_warehouse"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        warehouse_name = st.text_input("Nom Entrepôt *")
                        location = st.text_input("Localisation *")
                    
                    with col2:
                        capacity_m3 = st.number_input("Capacité (m³):", min_value=0.0)
                    
                    if st.form_submit_button("Créer Entrepôt"):
                        if warehouse_name and location:
                            try:
                                query = """
                                    INSERT INTO warehouses (warehouse_name, location, capacity_m3)
                                    VALUES (%s, %s, %s)
                                """
                                db.execute_query(query, (
                                    warehouse_name, location, capacity_m3
                                ))
                                st.success("✅ Entrepôt créé!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erreur: {e}")
                        else:
                            st.error("❌ Veuillez remplir les champs obligatoires")
            
            with tab3:
                st.subheader("📁 Import CSV - Entrepôts")
                uploaded_file = st.file_uploader("Choisir un fichier CSV", type="csv")
                
                if uploaded_file is not None:
                    try:
                        import pandas as pd
                        df = pd.read_csv(uploaded_file)
                        
                        st.write("Aperçu des données:")
                        st.dataframe(df.head())
                        
                        # Mapping des colonnes
                        st.write("Mapping des colonnes:")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            warehouse_name_col = st.selectbox("Nom Entrepôt:", df.columns)
                            location_col = st.selectbox("Localisation:", df.columns)
                        
                        with col2:
                            capacity_col = st.selectbox("Capacité (m³):", df.columns)
                        
                        if st.button("📥 Importer les données"):
                            success_count = 0
                            error_count = 0
                            
                            for _, row in df.iterrows():
                                try:
                                    query = "INSERT INTO warehouses (warehouse_name, location, capacity_m3) VALUES (%s, %s, %s)"
                                    db.execute_query(query, (
                                        str(row[warehouse_name_col]),
                                        str(row[location_col]),
                                        float(row[capacity_col])
                                    ))
                                    success_count += 1
                                except Exception as e:
                                    error_count += 1
                                    continue
                            
                            st.success(f"✅ Import terminé: {success_count} entrepôts importés, {error_count} erreurs")
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la lecture du fichier: {e}")
                
                st.info("💡 Format CSV attendu: warehouse_name, location, capacity_m3")
        else:
            st.warning("Aucun entrepôt trouvé")
    
    except Exception as e:
        st.error(f"Erreur: {e}")
