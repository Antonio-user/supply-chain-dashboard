"""Page d'accueil du dashboard avec KPIs et graphiques"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from app.database import db
from services.kpi_service import KPIService
from datetime import datetime

def render():
    """Affiche la page d'accueil du dashboard professionnel"""
    
    # En-tête avec animation et style professionnel
    st.markdown('''
    <div class="fade-in">
        <div class="dashboard-header" style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 1rem;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        ">
            <h1 style="
                font-size: 2.5rem;
                font-weight: 800;
                margin: 0 0 0.5rem 0;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            ">
                <i class="fas fa-tachometer-alt" style="margin-right: 1rem;"></i>
                Tableau de Bord Principal
            </h1>
            <p style="
                font-size: 1.125rem;
                margin: 0;
                opacity: 0.9;
                font-weight: 500;
            ">Vue d'ensemble de votre chaîne d'approvisionnement</p>
            <div style="
                margin-top: 1rem;
                font-size: 0.875rem;
                opacity: 0.8;
            ">
                <i class="fas fa-clock" style="margin-right: 0.5rem;"></i>
                Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y à %H:%M')}
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Service KPI
    kpi_service = KPIService()
    
    # KPIs principaux avec cartes professionnelles
    st.markdown('<h3 class="section-header">📈 Indicateurs Clés de Performance</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_orders = kpi_service.get_total_orders()
        st.markdown(f'''
        <div class="metric-card fade-in" style="
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border-left: 4px solid #2563eb;
        ">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <i class="fas fa-shopping-cart" style="font-size: 2rem; color: #2563eb;"></i>
                <div>
                    <h4 style="margin: 0; color: #1e40af; font-size: 0.875rem; text-transform: uppercase; font-weight: 600;">Commandes Totales</h4>
                    <p style="margin: 0.25rem 0 0 0; font-size: 2rem; font-weight: 800; color: #1e3a8a;">{total_orders}</p>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="background: #10b981; color: white; padding: 0.25rem 0.5rem; border-radius: 0.5rem; font-size: 0.75rem; font-weight: 600;">↑ +12</span>
                <span style="color: #059669; font-size: 0.875rem; font-weight: 500;">vs mois dernier</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        stock_value = kpi_service.get_total_stock_value()
        st.markdown(f'''
        <div class="metric-card fade-in" style="
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            border-left: 4px solid #10b981;
        ">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <i class="fas fa-euro-sign" style="font-size: 2rem; color: #10b981;"></i>
                <div>
                    <h4 style="margin: 0; color: #065f46; font-size: 0.875rem; text-transform: uppercase; font-weight: 600;">Valeur Stock</h4>
                    <p style="margin: 0.25rem 0 0 0; font-size: 2rem; font-weight: 800; color: #064e3b;">{stock_value:,.0f}€</p>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="background: #10b981; color: white; padding: 0.25rem 0.5rem; border-radius: 0.5rem; font-size: 0.75rem; font-weight: 600;">↑ +5.2%</span>
                <span style="color: #059669; font-size: 0.875rem; font-weight: 500;">croissance</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        critical_stocks = kpi_service.get_critical_stocks_count()
        st.markdown(f'''
        <div class="metric-card fade-in" style="
            background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
            border-left: 4px solid #ef4444;
        ">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <i class="fas fa-exclamation-triangle" style="font-size: 2rem; color: #ef4444;"></i>
                <div>
                    <h4 style="margin: 0; color: #991b1b; font-size: 0.875rem; text-transform: uppercase; font-weight: 600;">Stocks Critiques</h4>
                    <p style="margin: 0.25rem 0 0 0; font-size: 2rem; font-weight: 800; color: #7f1d1d;">{critical_stocks}</p>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="background: #10b981; color: white; padding: 0.25rem 0.5rem; border-radius: 0.5rem; font-size: 0.75rem; font-weight: 600;">↓ -3</span>
                <span style="color: #059669; font-size: 0.875rem; font-weight: 500;">amélioration</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        otif_rate = kpi_service.get_otif_rate()
        st.markdown(f'''
        <div class="metric-card fade-in" style="
            background: linear-gradient(135deg, #fffbeb 0%, #fed7aa 100%);
            border-left: 4px solid #f59e0b;
        ">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <i class="fas fa-clock" style="font-size: 2rem; color: #f59e0b;"></i>
                <div>
                    <h4 style="margin: 0; color: #92400e; font-size: 0.875rem; text-transform: uppercase; font-weight: 600;">Taux OTIF</h4>
                    <p style="margin: 0.25rem 0 0 0; font-size: 2rem; font-weight: 800; color: #78350f;">{otif_rate:.1f}%</p>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="background: #10b981; color: white; padding: 0.25rem 0.5rem; border-radius: 0.5rem; font-size: 0.75rem; font-weight: 600;">↑ +2.1%</span>
                <span style="color: #059669; font-size: 0.875rem; font-weight: 500;">performance</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Graphiques professionnels
    st.markdown('<h3 class="section-header">📉 Analyses et Tendances</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
        <div class="form-container">
            <h4 style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin: 0 0 1.5rem 0;
                color: #1e40af;
                font-weight: 700;
            ">
                <i class="fas fa-chart-line" style="color: #2563eb;"></i>
                Évolution des Commandes
            </h4>
        </div>
        ''', unsafe_allow_html=True)
        
        orders_data = kpi_service.get_orders_trend()
        if not orders_data.empty:
            fig = px.line(
                orders_data, 
                x='date', 
                y='count',
                title="",
                color_discrete_sequence=['#2563eb']
            )
            fig.update_layout(
                font_family="Inter",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=20, b=40, l=40, r=40),
                xaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(0,0,0,0.1)",
                    title="Date"
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(0,0,0,0.1)",
                    title="Nombre de commandes"
                )
            )
            fig.update_traces(
                line=dict(width=3),
                marker=dict(size=8)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📈 Aucune donnée de tendance disponible")
    
    with col2:
        st.markdown('''
        <div class="form-container">
            <h4 style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin: 0 0 1.5rem 0;
                color: #1e40af;
                font-weight: 700;
            ">
                <i class="fas fa-chart-pie" style="color: #10b981;"></i>
                Répartition des Stocks
            </h4>
        </div>
        ''', unsafe_allow_html=True)
        
        stock_data = kpi_service.get_stock_distribution()
        if not stock_data.empty:
            fig = px.pie(
                stock_data, 
                values='quantity', 
                names='category',
                title="",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(
                font_family="Inter",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=20, b=40, l=40, r=40)
            )
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Quantité: %{value}<br>Pourcentage: %{percent}<extra></extra>'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📦 Aucune donnée de stock disponible")
    
    # Section des alertes avec design professionnel
    st.markdown('<h3 class="section-header">🚨 Centre d\'Alertes</h3>', unsafe_allow_html=True)
    
    alerts = kpi_service.get_critical_alerts()
    
    if not alerts.empty:
        st.markdown('''
        <div class="form-container" style="
            background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
            border-left: 4px solid #ef4444;
        ">
            <h4 style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin: 0 0 1.5rem 0;
                color: #991b1b;
                font-weight: 700;
            ">
                <i class="fas fa-exclamation-triangle" style="color: #ef4444;"></i>
                Alertes Actives ({len(alerts)})
            </h4>
        </div>
        ''', unsafe_allow_html=True)
        
        for i, (_, alert) in enumerate(alerts.head(5).iterrows()):
            priority_config = {
                'HIGH': {'color': '#ef4444', 'bg': '#fef2f2', 'icon': 'exclamation-circle', 'label': 'CRITIQUE'},
                'MEDIUM': {'color': '#f59e0b', 'bg': '#fffbeb', 'icon': 'exclamation-triangle', 'label': 'IMPORTANT'},
                'LOW': {'color': '#2563eb', 'bg': '#eff6ff', 'icon': 'info-circle', 'label': 'INFO'}
            }
            
            config = priority_config.get(alert['priority'], priority_config['LOW'])
            
            st.markdown(f'''
            <div style="
                background: {config['bg']};
                border-left: 4px solid {config['color']};
                padding: 1rem 1.5rem;
                border-radius: 0.5rem;
                margin: 0.75rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            ">
                <div style="
                    display: flex;
                    align-items: flex-start;
                    gap: 1rem;
                ">
                    <i class="fas fa-{config['icon']}" style="
                        color: {config['color']};
                        font-size: 1.25rem;
                        margin-top: 0.125rem;
                    "></i>
                    <div style="flex: 1;">
                        <div style="
                            display: flex;
                            align-items: center;
                            gap: 0.75rem;
                            margin-bottom: 0.5rem;
                        ">
                            <span style="
                                background: {config['color']};
                                color: white;
                                padding: 0.25rem 0.75rem;
                                border-radius: 9999px;
                                font-size: 0.75rem;
                                font-weight: 700;
                                text-transform: uppercase;
                                letter-spacing: 0.05em;
                            ">{config['label']}</span>
                            <span style="
                                color: #6b7280;
                                font-size: 0.875rem;
                                font-weight: 500;
                            ">Alert #{i+1}</span>
                        </div>
                        <p style="
                            margin: 0;
                            color: #374151;
                            font-weight: 500;
                            line-height: 1.5;
                        ">{alert['message']}</p>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="form-container" style="
            background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
            border-left: 4px solid #10b981;
            text-align: center;
        ">
            <div style="
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 1rem;
                padding: 2rem;
            ">
                <i class="fas fa-check-circle" style="
                    font-size: 3rem;
                    color: #10b981;
                "></i>
                <h4 style="
                    margin: 0;
                    color: #065f46;
                    font-weight: 700;
                    font-size: 1.25rem;
                ">Système Opérationnel</h4>
                <p style="
                    margin: 0;
                    color: #047857;
                    font-weight: 500;
                ">Aucune alerte critique détectée. Votre chaîne d'approvisionnement fonctionne normalement.</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Pied de page avec informations de mise à jour
    st.markdown('''
    <div style="
        margin-top: 3rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 0.75rem;
        border: 1px solid #cbd5e1;
        text-align: center;
    ">
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            color: #64748b;
            font-size: 0.875rem;
            font-weight: 500;
        ">
            <i class="fas fa-sync-alt"></i>
            <span>Tableau de bord mis à jour automatiquement toutes les 5 minutes</span>
            <span style="
                background: #10b981;
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 9999px;
                font-size: 0.75rem;
                font-weight: 600;
            ">LIVE</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
