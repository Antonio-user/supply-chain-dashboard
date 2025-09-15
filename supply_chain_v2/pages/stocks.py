"""Page de gestion des stocks"""
import streamlit as st
import pandas as pd
from app.database import db

def render():
    """Affiche la page de gestion des stocks"""
    
    st.markdown('<h2 class="section-header">📦 Gestion des Stocks</h2>', 
                unsafe_allow_html=True)
    
    # Récupération des données
    try:
        stocks_query = """
            SELECT 
                i.inventory_id,
                w.warehouse_name,
                s.sku_code,
                s.product_name,
                s.category,
                i.quantity_available,
                i.quantity_reserved,
                i.safety_stock,
                i.reorder_point,
                s.unit_cost,
                (i.quantity_available * s.unit_cost) as stock_value
            FROM inventory i
            JOIN warehouses w ON i.warehouse_id = w.warehouse_id
            JOIN skus s ON i.sku_id = s.sku_id
            ORDER BY s.product_name
        """
        stocks_df = db.fetch_dataframe(stocks_query)
        
        if not stocks_df.empty:
            # Filtres
            col1, col2, col3 = st.columns(3)
            
            with col1:
                warehouses = ['Tous'] + stocks_df['warehouse_name'].unique().tolist()
                selected_warehouse = st.selectbox("Entrepôt:", warehouses)
            
            with col2:
                categories = ['Toutes'] + stocks_df['category'].unique().tolist()
                selected_category = st.selectbox("Catégorie:", categories)
            
            with col3:
                stock_status = st.selectbox("Statut:", 
                    ['Tous', 'Stock Normal', 'Stock Faible', 'Stock Critique'])
            
            # Application des filtres
            filtered_df = stocks_df.copy()
            
            if selected_warehouse != 'Tous':
                filtered_df = filtered_df[filtered_df['warehouse_name'] == selected_warehouse]
            
            if selected_category != 'Toutes':
                filtered_df = filtered_df[filtered_df['category'] == selected_category]
            
            if stock_status == 'Stock Critique':
                filtered_df = filtered_df[filtered_df['quantity_available'] <= filtered_df['safety_stock']]
            elif stock_status == 'Stock Faible':
                filtered_df = filtered_df[
                    (filtered_df['quantity_available'] > filtered_df['safety_stock']) &
                    (filtered_df['quantity_available'] <= filtered_df['reorder_point'])
                ]
            elif stock_status == 'Stock Normal':
                filtered_df = filtered_df[filtered_df['quantity_available'] > filtered_df['reorder_point']]
            
            # Onglets
            tab1, tab2, tab3 = st.tabs(["📊 Liste des Stocks", "➕ Mouvement de Stock", "📈 Statistiques"])
            
            with tab1:
                st.subheader(f"📋 Stocks ({len(filtered_df)} articles)")
                
                # Tableau des stocks
                if not filtered_df.empty:
                    # Ajout de colonnes de statut
                    def get_stock_status(row):
                        if row['quantity_available'] <= row['safety_stock']:
                            return "🔴 Critique"
                        elif row['quantity_available'] <= row['reorder_point']:
                            return "🟡 Faible"
                        else:
                            return "🟢 Normal"
                    
                    filtered_df['statut'] = filtered_df.apply(get_stock_status, axis=1)
                    
                    # Affichage du tableau
                    display_columns = [
                        'warehouse_name', 'sku_code', 'product_name', 'category',
                        'quantity_available', 'safety_stock', 'reorder_point', 
                        'stock_value', 'statut'
                    ]
                    
                    st.dataframe(
                        filtered_df[display_columns],
                        column_config={
                            'warehouse_name': 'Entrepôt',
                            'sku_code': 'Code SKU',
                            'product_name': 'Produit',
                            'category': 'Catégorie',
                            'quantity_available': 'Qté Disponible',
                            'safety_stock': 'Stock Sécurité',
                            'reorder_point': 'Point Commande',
                            'stock_value': st.column_config.NumberColumn(
                                'Valeur Stock',
                                format="%.2f €"
                            ),
                            'statut': 'Statut'
                        },
                        width='stretch'
                    )
                else:
                    st.warning("Aucun stock trouvé avec les filtres sélectionnés")
            
            with tab2:
                st.subheader("➕ Ajouter un Mouvement de Stock")
                
                with st.form("stock_movement_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Sélection du produit
                        products = stocks_df[['sku_code', 'product_name']].drop_duplicates()
                        product_options = [f"{row['sku_code']} - {row['product_name']}" 
                                         for _, row in products.iterrows()]
                        selected_product = st.selectbox("Produit:", product_options)
                        
                        movement_type = st.selectbox("Type de mouvement:", 
                                                   ["IN", "OUT", "ADJUSTMENT"])
                        quantity = st.number_input("Quantité:", min_value=1, value=1)
                    
                    with col2:
                        reason = st.text_area("Raison du mouvement:", 
                                            placeholder="Ex: Réception commande, Expédition client...")
                        
                        warehouse_options = stocks_df['warehouse_name'].unique().tolist()
                        selected_warehouse_move = st.selectbox("Entrepôt:", warehouse_options)
                    
                    if st.form_submit_button("➕ Enregistrer Mouvement"):
                        if selected_product and quantity > 0:
                            try:
                                # Extraction du SKU code
                                sku_code = selected_product.split(' - ')[0]
                                
                                # Insertion du mouvement
                                insert_query = """
                                    INSERT INTO stock_movements (sku_id, warehouse_id, movement_type, quantity, reason)
                                    SELECT s.sku_id, w.warehouse_id, %s, %s, %s
                                    FROM skus s, warehouses w
                                    WHERE s.sku_code = %s AND w.warehouse_name = %s
                                """
                                
                                db.execute_query(insert_query, (
                                    movement_type, quantity, reason, sku_code, selected_warehouse_move
                                ))
                                
                                # Mise à jour du stock
                                if movement_type == "IN":
                                    update_query = """
                                        UPDATE inventory 
                                        SET quantity_available = quantity_available + %s
                                        WHERE sku_id = (SELECT sku_id FROM skus WHERE sku_code = %s)
                                        AND warehouse_id = (SELECT warehouse_id FROM warehouses WHERE warehouse_name = %s)
                                    """
                                    db.execute_query(update_query, (quantity, sku_code, selected_warehouse_move))
                                elif movement_type == "OUT":
                                    update_query = """
                                        UPDATE inventory 
                                        SET quantity_available = quantity_available - %s
                                        WHERE sku_id = (SELECT sku_id FROM skus WHERE sku_code = %s)
                                        AND warehouse_id = (SELECT warehouse_id FROM warehouses WHERE warehouse_name = %s)
                                    """
                                    db.execute_query(update_query, (quantity, sku_code, selected_warehouse_move))
                                
                                st.success("✅ Mouvement de stock enregistré avec succès!")
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Erreur lors de l'enregistrement: {e}")
                        else:
                            st.error("❌ Veuillez remplir tous les champs obligatoires")
            
            with tab3:
                st.subheader("📈 Statistiques des Stocks")
                
                # Métriques
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    total_items = len(filtered_df)
                    st.metric("Articles Total", total_items)
                
                with col2:
                    total_value = filtered_df['stock_value'].sum()
                    st.metric("Valeur Totale", f"{total_value:,.0f}€")
                
                with col3:
                    critical_count = len(filtered_df[filtered_df['quantity_available'] <= filtered_df['safety_stock']])
                    st.metric("Stocks Critiques", critical_count)
                
                with col4:
                    avg_value = filtered_df['stock_value'].mean()
                    st.metric("Valeur Moyenne", f"{avg_value:,.0f}€")
        
        else:
            st.warning("Aucun stock trouvé dans la base de données")
    
    except Exception as e:
        st.error(f"Erreur lors de la récupération des stocks: {e}")
