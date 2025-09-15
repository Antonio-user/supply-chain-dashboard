"""Composants UI professionnels pour le dashboard Supply Chain"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

def render_professional_header(title: str, subtitle: str = None, icon: str = None):
    """Rendu d'un en-tête professionnel avec animation"""
    icon_html = f'<i class="fas fa-{icon}" style="margin-right: 1rem; color: var(--primary-color);"></i>' if icon else ''
    subtitle_html = f'<p class="header-subtitle">{subtitle}</p>' if subtitle else ''
    
    st.markdown(f'''
    <div class="professional-header fade-in">
        <h1 class="section-header">
            {icon_html}{title}
        </h1>
        {subtitle_html}
    </div>
    ''', unsafe_allow_html=True)

def render_metric_card(title: str, value: str, delta: str = None, delta_color: str = "normal", icon: str = None):
    """Rendu d'une carte métrique professionnelle"""
    delta_html = ""
    if delta:
        delta_class = "metric-delta-positive" if delta_color == "normal" else "metric-delta-negative"
        delta_html = f'<div class="{delta_class}">{delta}</div>'
    
    icon_html = f'<i class="fas fa-{icon} metric-icon"></i>' if icon else ''
    
    st.markdown(f'''
    <div class="metric-card fade-in">
        <div class="metric-header">
            {icon_html}
            <span class="metric-title">{title}</span>
        </div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    ''', unsafe_allow_html=True)

def render_action_buttons(edit_callback=None, delete_callback=None, custom_buttons=None):
    """Rendu de boutons d'action professionnels"""
    cols = st.columns(len([b for b in [edit_callback, delete_callback] + (custom_buttons or []) if b]))
    
    col_idx = 0
    if edit_callback:
        with cols[col_idx]:
            if st.button("✏️ Modifier", key=f"edit_{datetime.now().timestamp()}", 
                        help="Modifier cet élément"):
                edit_callback()
        col_idx += 1
    
    if delete_callback:
        with cols[col_idx]:
            if st.button("🗑️ Supprimer", key=f"delete_{datetime.now().timestamp()}", 
                        help="Supprimer cet élément"):
                delete_callback()
        col_idx += 1
    
    if custom_buttons:
        for button in custom_buttons:
            with cols[col_idx]:
                if st.button(button['label'], key=f"custom_{col_idx}_{datetime.now().timestamp()}", 
                           help=button.get('help', '')):
                    button['callback']()
            col_idx += 1

def render_professional_form(title: str, fields: list, submit_callback=None, cancel_callback=None):
    """Rendu d'un formulaire professionnel"""
    st.markdown(f'''
    <div class="form-container">
        <h3 class="form-title">
            <i class="fas fa-edit" style="margin-right: 0.5rem; color: var(--primary-color);"></i>
            {title}
        </h3>
    </div>
    ''', unsafe_allow_html=True)
    
    with st.form(f"professional_form_{datetime.now().timestamp()}"):
        # Rendu des champs
        field_values = {}
        cols = st.columns(2) if len(fields) > 2 else [st.container()]
        
        for i, field in enumerate(fields):
            col = cols[i % len(cols)]
            with col:
                if field['type'] == 'text':
                    field_values[field['key']] = st.text_input(
                        field['label'], 
                        value=field.get('value', ''),
                        help=field.get('help', '')
                    )
                elif field['type'] == 'textarea':
                    field_values[field['key']] = st.text_area(
                        field['label'], 
                        value=field.get('value', ''),
                        help=field.get('help', '')
                    )
                elif field['type'] == 'number':
                    field_values[field['key']] = st.number_input(
                        field['label'], 
                        value=field.get('value', 0.0),
                        help=field.get('help', '')
                    )
                elif field['type'] == 'selectbox':
                    field_values[field['key']] = st.selectbox(
                        field['label'], 
                        options=field['options'],
                        index=field.get('index', 0),
                        help=field.get('help', '')
                    )
                elif field['type'] == 'checkbox':
                    field_values[field['key']] = st.checkbox(
                        field['label'], 
                        value=field.get('value', False),
                        help=field.get('help', '')
                    )
        
        # Boutons d'action
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("💾 Sauvegarder", use_container_width=True)
            if submitted and submit_callback:
                submit_callback(field_values)
        
        with col2:
            cancelled = st.form_submit_button("❌ Annuler", use_container_width=True)
            if cancelled and cancel_callback:
                cancel_callback()

def render_professional_table(data, columns_config=None, actions=True):
    """Rendu d'un tableau professionnel avec actions"""
    if data.empty:
        st.info("📊 Aucune donnée disponible")
        return
    
    # Configuration des colonnes
    if columns_config:
        st.dataframe(
            data,
            column_config=columns_config,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.dataframe(data, use_container_width=True, hide_index=True)

def render_professional_chart(chart_type: str, data, title: str, **kwargs):
    """Rendu de graphiques professionnels"""
    fig = None
    
    if chart_type == "bar":
        fig = px.bar(data, title=title, **kwargs)
    elif chart_type == "line":
        fig = px.line(data, title=title, **kwargs)
    elif chart_type == "pie":
        fig = px.pie(data, title=title, **kwargs)
    elif chart_type == "scatter":
        fig = px.scatter(data, title=title, **kwargs)
    
    if fig:
        # Style professionnel
        fig.update_layout(
            title_font_size=20,
            title_font_color="#0f172a",
            title_x=0.5,
            font_family="Inter",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=60, b=40, l=40, r=40)
        )
        
        fig.update_traces(
            marker_line_width=0,
            selector=dict(type="bar")
        )
        
        st.plotly_chart(fig, use_container_width=True)

def render_status_badge(status: str, status_config: dict = None):
    """Rendu d'un badge de statut professionnel"""
    default_config = {
        "active": {"color": "#10b981", "bg": "#ecfdf5", "text": "Actif"},
        "inactive": {"color": "#ef4444", "bg": "#fef2f2", "text": "Inactif"},
        "pending": {"color": "#f59e0b", "bg": "#fffbeb", "text": "En attente"},
        "completed": {"color": "#10b981", "bg": "#ecfdf5", "text": "Terminé"},
        "cancelled": {"color": "#ef4444", "bg": "#fef2f2", "text": "Annulé"}
    }
    
    config = status_config or default_config
    style = config.get(status.lower(), config.get("pending", {}))
    
    st.markdown(f'''
    <span class="status-badge" style="
        background-color: {style.get('bg', '#f3f4f6')};
        color: {style.get('color', '#6b7280')};
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    ">
        {style.get('text', status)}
    </span>
    ''', unsafe_allow_html=True)

def render_loading_spinner(text: str = "Chargement..."):
    """Rendu d'un spinner de chargement professionnel"""
    st.markdown(f'''
    <div class="loading-container" style="
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        gap: 1rem;
    ">
        <div class="spinner" style="
            width: 24px;
            height: 24px;
            border: 3px solid #e2e8f0;
            border-top: 3px solid #2563eb;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        "></div>
        <span style="color: #64748b; font-weight: 500;">{text}</span>
    </div>
    <style>
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
    ''', unsafe_allow_html=True)

def render_alert_banner(message: str, alert_type: str = "info", dismissible: bool = False):
    """Rendu d'une bannière d'alerte professionnelle"""
    icons = {
        "info": "info-circle",
        "success": "check-circle", 
        "warning": "exclamation-triangle",
        "error": "exclamation-circle"
    }
    
    colors = {
        "info": {"bg": "#eff6ff", "border": "#2563eb", "text": "#1e40af"},
        "success": {"bg": "#ecfdf5", "border": "#10b981", "text": "#065f46"},
        "warning": {"bg": "#fffbeb", "border": "#f59e0b", "text": "#92400e"},
        "error": {"bg": "#fef2f2", "border": "#ef4444", "text": "#991b1b"}
    }
    
    style = colors.get(alert_type, colors["info"])
    icon = icons.get(alert_type, "info-circle")
    
    st.markdown(f'''
    <div class="alert-banner" style="
        background-color: {style['bg']};
        border-left: 4px solid {style['border']};
        color: {style['text']};
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    ">
        <i class="fas fa-{icon}" style="font-size: 1.25rem;"></i>
        <span style="font-weight: 500;">{message}</span>
    </div>
    ''', unsafe_allow_html=True)
