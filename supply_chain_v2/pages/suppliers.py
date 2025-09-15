"""Page de gestion des fournisseurs"""
import streamlit as st
from app.database import db

def render():
    """Affiche la page de gestion des fournisseurs"""
    
    st.markdown('<h2 class="section-header">🤝 Gestion des Fournisseurs</h2>', 
                unsafe_allow_html=True)
    
    try:
        suppliers_query = """
            SELECT supplier_id, supplier_name, contact_person, 
                   email, phone, address, country, is_active
            FROM suppliers
            ORDER BY supplier_name
        """
        suppliers_df = db.fetch_dataframe(suppliers_query)
        
        if not suppliers_df.empty:
            tab1, tab2, tab3 = st.tabs(["📊 Liste", "➕ Nouveau", "📁 Import CSV"])
            
            with tab1:
                # Actions CRUD
                if st.checkbox("Mode édition"):
                    selected_supplier = st.selectbox(
                        "Sélectionner un fournisseur:",
                        options=suppliers_df['supplier_id'].tolist(),
                        format_func=lambda x: f"{suppliers_df[suppliers_df['supplier_id']==x]['supplier_name'].iloc[0]}"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✏️ Modifier"):
                            st.session_state.edit_supplier = selected_supplier
                    with col2:
                        if st.button("🗑️ Supprimer"):
                            st.session_state.delete_supplier = selected_supplier
                
                # Formulaire de modification
                if 'edit_supplier' in st.session_state:
                    supplier_data = suppliers_df[suppliers_df['supplier_id'] == st.session_state.edit_supplier].iloc[0]
                    st.markdown("### ✏️ Modifier le Fournisseur")
                    with st.form("edit_supplier_form"):
                        col1, col2 = st.columns(2)
                        with col1:
                            new_supplier_name = st.text_input("Nom Fournisseur:", value=supplier_data['supplier_name'])
                            new_contact_person = st.text_input("Contact:", value=supplier_data['contact_person'] or '')
                            new_email = st.text_input("Email:", value=supplier_data['email'] or '')
                            new_phone = st.text_input("Téléphone:", value=supplier_data['phone'] or '')
                        with col2:
                            new_address = st.text_area("Adresse:", value=supplier_data['address'] or '')
                            new_country = st.text_input("Pays:", value=supplier_data['country'] or '')
                            new_is_active = st.checkbox("Actif", value=bool(supplier_data['is_active']))
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("💾 Sauvegarder"):
                                try:
                                    update_query = "UPDATE suppliers SET supplier_name = %s, contact_person = %s, email = %s, phone = %s, address = %s, country = %s, is_active = %s WHERE supplier_id = %s"
                                    db.execute_query(update_query, (new_supplier_name, new_contact_person, new_email, new_phone, new_address, new_country, new_is_active, st.session_state.edit_supplier))
                                    st.success("✅ Fournisseur modifié!")
                                    del st.session_state.edit_supplier
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Erreur: {e}")
                        with col_cancel:
                            if st.form_submit_button("❌ Annuler"):
                                del st.session_state.edit_supplier
                                st.rerun()
                
                # Confirmation de suppression
                if 'delete_supplier' in st.session_state:
                    supplier_data = suppliers_df[suppliers_df['supplier_id'] == st.session_state.delete_supplier].iloc[0]
                    st.warning(f"⚠️ Supprimer le fournisseur **{supplier_data['supplier_name']}** ?")
                    col_confirm, col_cancel = st.columns(2)
                    with col_confirm:
                        if st.button("🗑️ Confirmer"):
                            try:
                                db.execute_query("DELETE FROM suppliers WHERE supplier_id = %s", (st.session_state.delete_supplier,))
                                st.success("✅ Fournisseur supprimé!")
                                del st.session_state.delete_supplier
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erreur: {e}")
                    with col_cancel:
                        if st.button("❌ Annuler"):
                            del st.session_state.delete_supplier
                            st.rerun()
                
                st.dataframe(
                    suppliers_df,
                    column_config={
                        'supplier_name': 'Nom Fournisseur',
                        'contact_person': 'Contact',
                        'email': 'Email',
                        'phone': 'Téléphone',
                        'address': 'Adresse',
                        'country': 'Pays',
                        'is_active': 'Actif'
                    },
                    width='stretch'
                )
            
            with tab2:
                with st.form("new_supplier"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        supplier_name = st.text_input("Nom Fournisseur *")
                        contact_person = st.text_input("Personne Contact")
                        email = st.text_input("Email")
                        phone = st.text_input("Téléphone")
                    
                    with col2:
                        address = st.text_area("Adresse")
                        country = st.text_input("Pays")
                        is_active = st.checkbox("Actif", value=True)
                    
                    if st.form_submit_button("Créer Fournisseur"):
                        if supplier_name:
                            try:
                                query = """
                                    INSERT INTO suppliers (supplier_name, contact_person, 
                                                         email, phone, address, country, is_active)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """
                                db.execute_query(query, (
                                    supplier_name, contact_person, email, 
                                    phone, address, country, is_active
                                ))
                                st.success("✅ Fournisseur créé!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erreur: {e}")
                        else:
                            st.error("❌ Le nom du fournisseur est obligatoire")
            
            with tab3:
                st.subheader("📁 Import CSV - Fournisseurs")
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
                            supplier_name_col = st.selectbox("Nom Fournisseur:", df.columns)
                            contact_person_col = st.selectbox("Contact:", df.columns)
                            email_col = st.selectbox("Email:", df.columns)
                            phone_col = st.selectbox("Téléphone:", df.columns)
                        
                        with col2:
                            address_col = st.selectbox("Adresse:", df.columns)
                            country_col = st.selectbox("Pays:", df.columns)
                            is_active_col = st.selectbox("Actif (true/false):", df.columns)
                        
                        if st.button("📥 Importer les données"):
                            success_count = 0
                            error_count = 0
                            
                            for _, row in df.iterrows():
                                try:
                                    query = "INSERT INTO suppliers (supplier_name, contact_person, email, phone, address, country, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                                    is_active_val = str(row[is_active_col]).lower() in ['true', '1', 'yes', 'oui']
                                    db.execute_query(query, (
                                        str(row[supplier_name_col]),
                                        str(row[contact_person_col]),
                                        str(row[email_col]),
                                        str(row[phone_col]),
                                        str(row[address_col]),
                                        str(row[country_col]),
                                        is_active_val
                                    ))
                                    success_count += 1
                                except Exception as e:
                                    error_count += 1
                                    continue
                            
                            st.success(f"✅ Import terminé: {success_count} fournisseurs importés, {error_count} erreurs")
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la lecture du fichier: {e}")
                
                st.info("💡 Format CSV attendu: supplier_name, contact_person, email, phone, address, country, is_active")
        else:
            st.warning("Aucun fournisseur trouvé")
    
    except Exception as e:
        st.error(f"Erreur: {e}")
