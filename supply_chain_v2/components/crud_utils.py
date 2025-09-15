"""Utilitaires CRUD réutilisables pour toutes les pages"""
import streamlit as st
import pandas as pd
from app.database import db

def render_edit_delete_buttons(items_df, item_id_col, item_name_col, edit_key, delete_key):
    """Affiche les boutons d'édition et suppression avec sélection"""
    if st.checkbox("Mode édition"):
        selected_item = st.selectbox(
            "Sélectionner un élément:",
            options=items_df[item_id_col].tolist(),
            format_func=lambda x: f"{items_df[items_df[item_id_col]==x][item_name_col].iloc[0]}"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Modifier"):
                st.session_state[edit_key] = selected_item
        with col2:
            if st.button("🗑️ Supprimer"):
                st.session_state[delete_key] = selected_item

def render_csv_import(table_name, columns_mapping, sample_format):
    """Affiche l'interface d'import CSV générique"""
    st.subheader(f"📁 Import CSV - {table_name}")
    uploaded_file = st.file_uploader("Choisir un fichier CSV", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            st.write("Aperçu des données:")
            st.dataframe(df.head())
            
            # Mapping des colonnes
            st.write("Mapping des colonnes:")
            col1, col2 = st.columns(2)
            
            mapped_columns = {}
            col_keys = list(columns_mapping.keys())
            
            with col1:
                for i, (key, label) in enumerate(columns_mapping.items()):
                    if i < len(col_keys) // 2 + len(col_keys) % 2:
                        mapped_columns[key] = st.selectbox(f"{label}:", df.columns)
            
            with col2:
                for i, (key, label) in enumerate(columns_mapping.items()):
                    if i >= len(col_keys) // 2 + len(col_keys) % 2:
                        mapped_columns[key] = st.selectbox(f"{label}:", df.columns)
            
            return df, mapped_columns
            
        except Exception as e:
            st.error(f"❌ Erreur lors de la lecture du fichier: {e}")
            return None, None
    
    st.info(f"💡 Format CSV attendu: {sample_format}")
    return None, None

def execute_bulk_insert(df, mapped_columns, table_name, insert_query, conflict_resolution="DO NOTHING"):
    """Exécute l'insertion en lot avec gestion d'erreurs"""
    success_count = 0
    error_count = 0
    
    for _, row in df.iterrows():
        try:
            values = []
            for key in mapped_columns.keys():
                col_name = mapped_columns[key]
                value = row[col_name]
                
                # Conversion de type basique
                if pd.isna(value):
                    values.append(None)
                elif isinstance(value, (int, float)):
                    values.append(value)
                else:
                    values.append(str(value))
            
            db.execute_query(insert_query, tuple(values))
            success_count += 1
            
        except Exception as e:
            error_count += 1
            continue
    
    return success_count, error_count
