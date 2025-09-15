"""Page de gestion des clients"""
import streamlit as st
from app.database import db

def render():
    """Affiche la page de gestion des clients"""
    
    st.markdown('<h2 class="section-header">👥 Gestion des Clients</h2>', 
                unsafe_allow_html=True)
    
    try:
        clients_query = """
            SELECT customer_id, customer_name, contact_person, 
                   email, phone, address, city, country
            FROM customers
            ORDER BY customer_name
        """
        clients_df = db.fetch_dataframe(clients_query)
        
        # Debug: afficher le nombre de clients trouvés
        st.write(f"**Nombre de clients dans la base:** {len(clients_df)}")
        
        if not clients_df.empty:
            tab1, tab2, tab3 = st.tabs(["📊 Liste", "➕ Nouveau", "📁 Import CSV"])
            
            with tab1:
                # Actions CRUD
                if st.checkbox("Mode édition"):
                    selected_client = st.selectbox(
                        "Sélectionner un client:",
                        options=clients_df['customer_id'].tolist(),
                        format_func=lambda x: f"{clients_df[clients_df['customer_id']==x]['customer_name'].iloc[0]}"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✏️ Modifier"):
                            st.session_state.edit_client = selected_client
                    with col2:
                        if st.button("🗑️ Supprimer"):
                            st.session_state.delete_client = selected_client
                
                # Formulaire de modification
                if 'edit_client' in st.session_state:
                    client_data = clients_df[clients_df['customer_id'] == st.session_state.edit_client].iloc[0]
                    st.markdown("### ✏️ Modifier le Client")
                    with st.form("edit_client_form"):
                        col1, col2 = st.columns(2)
                        with col1:
                            new_customer_name = st.text_input("Nom Client:", value=client_data['customer_name'])
                            new_contact_person = st.text_input("Contact:", value=client_data['contact_person'] or '')
                            new_email = st.text_input("Email:", value=client_data['email'] or '')
                            new_phone = st.text_input("Téléphone:", value=client_data['phone'] or '')
                        with col2:
                            new_address = st.text_area("Adresse:", value=client_data['address'] or '')
                            new_city = st.text_input("Ville:", value=client_data['city'] or '')
                            new_country = st.text_input("Pays:", value=client_data['country'] or '')
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("💾 Sauvegarder"):
                                try:
                                    update_query = "UPDATE customers SET customer_name = %s, contact_person = %s, email = %s, phone = %s, address = %s, city = %s, country = %s WHERE customer_id = %s"
                                    db.execute_query(update_query, (new_customer_name, new_contact_person, new_email, new_phone, new_address, new_city, new_country, st.session_state.edit_client))
                                    st.success("✅ Client modifié!")
                                    del st.session_state.edit_client
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Erreur: {e}")
                        with col_cancel:
                            if st.form_submit_button("❌ Annuler"):
                                del st.session_state.edit_client
                                st.rerun()
                
                # Confirmation de suppression
                if 'delete_client' in st.session_state:
                    client_data = clients_df[clients_df['customer_id'] == st.session_state.delete_client].iloc[0]
                    st.warning(f"⚠️ Supprimer le client **{client_data['customer_name']}** ?")
                    col_confirm, col_cancel = st.columns(2)
                    with col_confirm:
                        if st.button("🗑️ Confirmer"):
                            try:
                                db.execute_query("DELETE FROM customers WHERE customer_id = %s", (st.session_state.delete_client,))
                                st.success("✅ Client supprimé!")
                                del st.session_state.delete_client
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erreur: {e}")
                    with col_cancel:
                        if st.button("❌ Annuler"):
                            del st.session_state.delete_client
                            st.rerun()
                
                st.dataframe(
                    clients_df,
                    column_config={
                        'customer_name': 'Nom Client',
                        'contact_person': 'Contact',
                        'email': 'Email',
                        'phone': 'Téléphone',
                        'address': 'Adresse',
                        'city': 'Ville',
                        'country': 'Pays',
                    },
                    width='stretch'
                )
            
            with tab2:
                with st.form("new_client"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        customer_name = st.text_input("Nom Client *")
                        contact_person = st.text_input("Personne Contact")
                        email = st.text_input("Email")
                        phone = st.text_input("Téléphone")
                    
                    with col2:
                        address = st.text_area("Adresse")
                        city = st.text_input("Ville")
                        country = st.text_input("Pays")
                    
                    if st.form_submit_button("Créer Client"):
                        if customer_name:
                            try:
                                query = """
                                    INSERT INTO customers (customer_name, contact_person, 
                                                         email, phone, address, city, country)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """
                                result = db.execute_query(query, (
                                    customer_name, contact_person, email, 
                                    phone, address, city, country
                                ))
                                if result:
                                    st.success("✅ Client créé avec succès!")
                                    # Attendre un peu pour que la base soit mise à jour
                                    import time
                                    time.sleep(0.5)
                                    st.rerun()
                                else:
                                    st.error("❌ Erreur lors de la création du client")
                            except Exception as e:
                                st.error(f"❌ Erreur: {e}")
                        else:
                            st.error("❌ Le nom du client est obligatoire")
            
            with tab3:
                st.subheader("📁 Import CSV - Clients")
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
                            customer_name_col = st.selectbox("Nom Client:", df.columns)
                            contact_person_col = st.selectbox("Contact:", df.columns)
                            email_col = st.selectbox("Email:", df.columns)
                            phone_col = st.selectbox("Téléphone:", df.columns)
                        
                        with col2:
                            address_col = st.selectbox("Adresse:", df.columns)
                            city_col = st.selectbox("Ville:", df.columns)
                            country_col = st.selectbox("Pays:", df.columns)
                        
                        if st.button("📥 Importer les données"):
                            success_count = 0
                            error_count = 0
                            
                            for _, row in df.iterrows():
                                try:
                                    query = "INSERT INTO customers (customer_name, contact_person, email, phone, address, city, country) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                                    db.execute_query(query, (
                                        str(row[customer_name_col]),
                                        str(row[contact_person_col]),
                                        str(row[email_col]),
                                        str(row[phone_col]),
                                        str(row[address_col]),
                                        str(row[city_col]),
                                        str(row[country_col])
                                    ))
                                    success_count += 1
                                except Exception as e:
                                    error_count += 1
                                    continue
                            
                            st.success(f"✅ Import terminé: {success_count} clients importés, {error_count} erreurs")
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la lecture du fichier: {e}")
                
                st.info("💡 Format CSV attendu: customer_name, contact_person, email, phone, address, city, country")
        else:
            st.warning("Aucun client trouvé dans la base de données")
            # Afficher un formulaire pour créer le premier client
            st.markdown("### ➕ Créer votre premier client")
            with st.form("first_client"):
                col1, col2 = st.columns(2)
                
                with col1:
                    customer_name = st.text_input("Nom Client *")
                    contact_person = st.text_input("Personne Contact")
                    email = st.text_input("Email")
                    phone = st.text_input("Téléphone")
                
                with col2:
                    address = st.text_area("Adresse")
                    city = st.text_input("Ville")
                    country = st.text_input("Pays")
                
                if st.form_submit_button("Créer Premier Client"):
                    if customer_name:
                        try:
                            query = """
                                INSERT INTO customers (customer_name, contact_person, 
                                                     email, phone, address, city, country)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """
                            result = db.execute_query(query, (
                                customer_name, contact_person, email, 
                                phone, address, city, country
                            ))
                            if result:
                                st.success("✅ Premier client créé!")
                                import time
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error("❌ Erreur lors de la création")
                        except Exception as e:
                            st.error(f"❌ Erreur: {e}")
                    else:
                        st.error("❌ Le nom du client est obligatoire")
    
    except Exception as e:
        st.error(f"Erreur: {e}")
