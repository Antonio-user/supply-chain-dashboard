"""Page de gestion des produits"""
import streamlit as st
from app.database import db

def render():
    """Affiche la page de gestion des produits"""
    
    st.markdown('<h2 class="section-header">🏷️ Gestion des Produits</h2>', 
                unsafe_allow_html=True)
    
    try:
        # Assurer la connexion
        if not db.connect():
            st.error("❌ Impossible de se connecter à la base de données")
            return
            
        products_query = """
            SELECT sku_id, sku_code, product_name, category, unit_cost
            FROM skus
            ORDER BY product_name
        """
        products_df = db.fetch_dataframe(products_query)
        
        # Debug info
        st.write(f"Debug: Nombre de produits trouvés: {len(products_df)}")
        
        if not products_df.empty:
            tab1, tab2, tab3 = st.tabs(["📊 Liste", "➕ Nouveau", "📁 Import CSV"])
            
            with tab1:
                # Filtres
                categories = ['Toutes'] + products_df['category'].unique().tolist()
                selected_category = st.selectbox("Catégorie:", categories)
                
                filtered_df = products_df.copy()
                if selected_category != 'Toutes':
                    filtered_df = filtered_df[filtered_df['category'] == selected_category]
                
                # Actions CRUD
                if st.checkbox("Mode édition"):
                    selected_product = st.selectbox(
                        "Sélectionner un produit:",
                        options=filtered_df['sku_id'].tolist(),
                        format_func=lambda x: f"{filtered_df[filtered_df['sku_id']==x]['sku_code'].iloc[0]} - {filtered_df[filtered_df['sku_id']==x]['product_name'].iloc[0]}"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✏️ Modifier"):
                            st.session_state.edit_product = selected_product
                    with col2:
                        if st.button("🗑️ Supprimer"):
                            st.session_state.delete_product = selected_product
                
                # Formulaire de modification
                if 'edit_product' in st.session_state:
                    product_data = filtered_df[filtered_df['sku_id'] == st.session_state.edit_product].iloc[0]
                    st.markdown("### ✏️ Modifier le Produit")
                    with st.form("edit_product_form"):
                        col1, col2 = st.columns(2)
                        with col1:
                            new_sku_code = st.text_input("Code SKU:", value=product_data['sku_code'])
                            new_product_name = st.text_input("Nom Produit:", value=product_data['product_name'])
                        with col2:
                            new_category = st.text_input("Catégorie:", value=product_data['category'])
                            new_unit_cost = st.number_input("Coût Unitaire:", value=float(product_data['unit_cost']))
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("💾 Sauvegarder"):
                                try:
                                    update_query = "UPDATE skus SET sku_code = %s, product_name = %s, category = %s, unit_cost = %s WHERE sku_id = %s"
                                    db.execute_query(update_query, (new_sku_code, new_product_name, new_category, new_unit_cost, st.session_state.edit_product))
                                    st.success("✅ Produit modifié!")
                                    del st.session_state.edit_product
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Erreur: {e}")
                        with col_cancel:
                            if st.form_submit_button("❌ Annuler"):
                                del st.session_state.edit_product
                                st.rerun()
                
                # Confirmation de suppression
                if 'delete_product' in st.session_state:
                    product_data = filtered_df[filtered_df['sku_id'] == st.session_state.delete_product].iloc[0]
                    st.warning(f"⚠️ Supprimer le produit **{product_data['product_name']}** ?")
                    col_confirm, col_cancel = st.columns(2)
                    with col_confirm:
                        if st.button("🗑️ Confirmer"):
                            try:
                                db.execute_query("DELETE FROM skus WHERE sku_id = %s", (st.session_state.delete_product,))
                                st.success("✅ Produit supprimé!")
                                del st.session_state.delete_product
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erreur: {e}")
                    with col_cancel:
                        if st.button("❌ Annuler"):
                            del st.session_state.delete_product
                            st.rerun()
                
                st.dataframe(
                    filtered_df,
                    column_config={
                        'sku_code': 'Code SKU',
                        'product_name': 'Nom Produit',
                        'category': 'Catégorie',
                        'unit_cost': st.column_config.NumberColumn(
                            'Coût Unitaire',
                            format="%.2f €"
                        ),
                    },
                    width='stretch'
                )
            
            with tab2:
                with st.form("new_product"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        sku_code = st.text_input("Code SKU *")
                        product_name = st.text_input("Nom Produit *")
                        category = st.text_input("Catégorie *")
                    
                    with col2:
                        unit_cost = st.number_input("Coût Unitaire (€):", min_value=0.0)
                    
                    if st.form_submit_button("Créer Produit"):
                        if sku_code and product_name and category:
                            try:
                                query = """
                                    INSERT INTO skus (sku_code, product_name, category, unit_cost)
                                    VALUES (%s, %s, %s, %s)
                                """
                                db.execute_query(query, (
                                    sku_code, product_name, category, unit_cost
                                ))
                                st.success("✅ Produit créé!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erreur: {e}")
                        else:
                            st.error("❌ Veuillez remplir les champs obligatoires")
            
            with tab3:
                st.subheader("📁 Import CSV - Produits")
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
                            sku_code_col = st.selectbox("Code SKU:", df.columns)
                            product_name_col = st.selectbox("Nom Produit:", df.columns)
                        
                        with col2:
                            category_col = st.selectbox("Catégorie:", df.columns)
                            unit_cost_col = st.selectbox("Coût Unitaire:", df.columns)
                        
                        if st.button("📥 Importer les données"):
                            success_count = 0
                            error_count = 0
                            
                            for _, row in df.iterrows():
                                try:
                                    query = "INSERT INTO skus (sku_code, product_name, category, unit_cost) VALUES (%s, %s, %s, %s) ON CONFLICT (sku_code) DO NOTHING"
                                    db.execute_query(query, (
                                        str(row[sku_code_col]),
                                        str(row[product_name_col]),
                                        str(row[category_col]),
                                        float(row[unit_cost_col])
                                    ))
                                    success_count += 1
                                except Exception as e:
                                    error_count += 1
                                    continue
                            
                            st.success(f"✅ Import terminé: {success_count} produits importés, {error_count} erreurs")
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la lecture du fichier: {e}")
                
                st.info("💡 Format CSV attendu: sku_code, product_name, category, unit_cost")
        else:
            st.warning("Aucun produit trouvé")
    
    except Exception as e:
        st.error(f"Erreur: {e}")
