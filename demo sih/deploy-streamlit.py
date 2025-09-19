#!/usr/bin/env python3
"""
Solar Microgrid Dashboard - Complete Streamlit Deployment
SIH Demo - IoT-based Solar Microgrid Monitoring System

This is a complete single-file Streamlit application that includes:
- Real-time data simulation
- Authentication system
- Alert management
- Beautiful dashboard with animations
- All backend and frontend functionality

Deployment Instructions:
1. pip install streamlit plotly pandas numpy
2. streamlit run deploy-streamlit.py
3. Open http://localhost:8501
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time
import json
from typing import Dict, List, Optional
import hashlib

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Solar Microgrid Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo',
        'Report a bug': "https://github.com/your-repo/issues",
        'About': "# Solar Microgrid Monitoring System\nSIH Demo - IoT-based monitoring for rural microgrids"
    }
)

# ============================================================================
# CUSTOM CSS FOR BEAUTIFUL UI
# ============================================================================

st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
        --success-color: #2ca02c;
        --warning-color: #d62728;
        --critical-color: #dc2626;
        --info-color: #9467bd;
        --light-bg: #f8f9fa;
        --dark-bg: #2c3e50;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom header */
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e, #2ca02c);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid var(--primary-color);
        margin: 1rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--primary-color);
        margin: 0;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #666;
        margin: 0.5rem 0 0 0;
    }

    /* Alert cards */
    .alert-critical {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        animation: pulse 2s infinite;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #ffa726, #ff9800);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #66bb6a, #4caf50);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .alert-info {
        background: linear-gradient(135deg, #42a5f5, #2196f3);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }

    /* Login form */
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }

    /* Animations */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }

    /* Status indicators */
    .status-online {
        display: inline-block;
        width: 12px;
        height: 12px;
        background: #4caf50;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    .status-warning {
        display: inline-block;
        width: 12px;
        height: 12px;
        background: #ff9800;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    .status-critical {
        display: inline-block;
        width: 12px;
        height: 12px;
        background: #f44336;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 1s infinite;
    }

    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50, #34495e);
    }
    
    .sidebar .sidebar-content .block-container {
        padding-top: 2rem;
    }

    /* Chart containers */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA SIMULATION AND STORAGE
# ============================================================================

@st.cache_data
def generate_historical_data():
    """Generate historical data for simulation with grid shifting and health monitoring"""
    np.random.seed(42)
    
    # Generate 1000 data points
    hours = np.arange(1000)
    
    # Energy data with daily patterns and night-time grid shifting
    generation = 1800 + 600 * np.sin(2 * np.pi * hours / 24) + np.random.normal(0, 100, 1000)
    generation = np.maximum(0, generation)
    
    # Add night-time periods with zero generation (simulating no solar)
    # Solar hours: 6 AM to 6 PM (hours 6-18), night hours: 6 PM to 6 AM (hours 18-30)
    night_mask = (hours % 24) >= 18  # 6 PM to 6 AM (night time)
    generation[night_mask] = 0
    
    storage_soc = 70 + 20 * np.sin(2 * np.pi * hours / 24) + np.random.normal(0, 5, 1000)
    load = 1500 + 400 * np.sin(2 * np.pi * hours / 24) + np.random.normal(0, 80, 1000)
    efficiency = 85 + 10 * np.sin(2 * np.pi * hours / 24) + np.random.normal(0, 3, 1000)
    
    # Grid power calculation (when solar is insufficient)
    grid_power = np.maximum(0, load - generation - storage_soc * 10)  # 10W per 1% SOC
    grid_power = np.where(generation == 0, load, grid_power)  # Full grid when no solar
    
    # System health calculation
    health_score = np.ones(1000) * 100
    health_score = np.where(storage_soc < 30, health_score - 30, health_score)
    health_score = np.where(efficiency < 75, health_score - 20, health_score)
    health_score = np.where(generation == 0, health_score - 10, health_score)  # Grid dependency
    health_score = np.clip(health_score, 0, 100)
    
    # Weather data
    temperature = 25 + 15 * np.sin(2 * np.pi * hours / 24) + np.random.normal(0, 2, 1000)
    irradiance = 1000 * np.sin(2 * np.pi * hours / 24) + np.random.normal(0, 50, 1000)
    irradiance = np.maximum(0, irradiance)
    
    # Create DataFrames
    energy_df = pd.DataFrame({
        'timestamp': pd.date_range(start='2024-01-01', periods=1000, freq='5min'),
        'generation_watt': generation,
        'storage_soc_percent': np.clip(storage_soc, 0, 100),
        'load_watt': np.maximum(0, load),
        'efficiency_percent': np.clip(efficiency, 0, 100),
        'grid_power_watt': grid_power,
        'health_score': health_score,
        'is_grid_mode': generation == 0
    })
    
    weather_df = pd.DataFrame({
        'timestamp': pd.date_range(start='2024-01-01', periods=1000, freq='5min'),
        'temp_c': temperature,
        'irradiance_wm2': irradiance
    })
    
    return energy_df, weather_df

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'operator' not in st.session_state:
    st.session_state.operator = None
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now()
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'last_alert_times' not in st.session_state:
    st.session_state.last_alert_times = {}
if 'predictive_enabled' not in st.session_state:
    st.session_state.predictive_enabled = False
if 'load_predictions' not in st.session_state:
    st.session_state.load_predictions = []

# ============================================================================
# AUTHENTICATION SYSTEM
# ============================================================================

def generate_otp():
    """Generate OTP for demo"""
    return "123456"

def verify_otp(phone_number: str, provided_otp: str) -> bool:
    """Verify OTP"""
    return provided_otp == generate_otp()

def create_operator(phone_number: str) -> Dict:
    """Create operator profile"""
    return {
        'id': len(st.session_state.get('operators', {})) + 1,
        'phone_number': phone_number,
        'name': f"Operator {len(st.session_state.get('operators', {})) + 1}",
        'email': f"operator{len(st.session_state.get('operators', {})) + 1}@microgrid.com",
        'role': 'operator'
    }

def login_form():
    """Display login form"""
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-header">
        <h1>☀️ Solar Microgrid</h1>
        <p>IoT Monitoring Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔐 Operator Login")
    
    with st.form("login_form"):
        phone_number = st.text_input("📱 Phone Number", placeholder="Enter your phone number")
        otp = st.text_input("🔑 OTP", placeholder="Enter OTP (Demo: 123456)")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("📤 Send OTP", use_container_width=True):
                if phone_number:
                    st.success(f"OTP sent to {phone_number}")
                    st.info("Demo OTP: 123456")
                else:
                    st.error("Please enter phone number")
        
        with col2:
            if st.form_submit_button("🚀 Login", use_container_width=True):
                if phone_number and otp:
                    if verify_otp(phone_number, otp):
                        st.session_state.authenticated = True
                        st.session_state.operator = create_operator(phone_number)
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid OTP. Demo OTP: 123456")
                else:
                    st.error("Please enter both phone number and OTP")
    
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; color: #666;">
        <p><strong>Demo Credentials:</strong></p>
        <p>📱 Phone: Any number</p>
        <p>🔑 OTP: 123456</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PREDICTIVE LOAD MANAGEMENT
# ============================================================================

def predict_load_management(energy_df: pd.DataFrame, current_idx: int) -> Dict:
    """Predict load management recommendations"""
    # Get recent data for prediction
    recent_data = energy_df.iloc[max(0, current_idx-24):current_idx+1]
    
    # Simple prediction based on historical patterns
    avg_load = recent_data['load_watt'].mean()
    avg_generation = recent_data['generation_watt'].mean()
    current_soc = energy_df.iloc[current_idx]['storage_soc_percent']
    
    # Predict next 6 hours
    next_6h_generation = avg_generation * 0.3  # Assume 30% of average (evening/night)
    next_6h_load = avg_load * 1.1  # Assume 10% increase in load
    
    # Calculate energy deficit
    energy_deficit = max(0, next_6h_load - next_6h_generation - current_soc * 10)
    
    recommendations = []
    
    if energy_deficit > 500:
        recommendations.append("🔋 Consider reducing non-essential loads")
        recommendations.append("⚡ Activate energy-saving mode")
        recommendations.append("🌙 Schedule heavy loads during peak generation")
    
    if current_soc < 40:
        recommendations.append("🔌 Switch to grid power to preserve battery")
        recommendations.append("⚡ Reduce current load by 20%")
    
    if energy_df.iloc[current_idx]['is_grid_mode']:
        recommendations.append("🌞 Solar generation will resume at 6 AM")
        recommendations.append("💰 Current grid consumption: {:.0f}W".format(energy_df.iloc[current_idx]['grid_power_watt']))
    
    return {
        'energy_deficit': energy_deficit,
        'recommendations': recommendations,
        'next_6h_generation': next_6h_generation,
        'next_6h_load': next_6h_load,
        'grid_mode': energy_df.iloc[current_idx]['is_grid_mode']
    }

def display_predictive_management(predictions: Dict):
    """Display predictive load management recommendations"""
    st.markdown("### 🤖 Predictive Load Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-value">📊 {predictions['energy_deficit']:.0f}W</div>
            <div class="metric-label">Predicted Energy Deficit (6h)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        mode_text = "🔌 Grid Mode" if predictions['grid_mode'] else "☀️ Solar Mode"
        mode_color = "var(--warning-color)" if predictions['grid_mode'] else "var(--success-color)"
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-value" style="color: {mode_color}">{mode_text}</div>
            <div class="metric-label">Current Power Mode</div>
        </div>
        """, unsafe_allow_html=True)
    
    if predictions['recommendations']:
        st.markdown("#### 💡 Recommendations:")
        for rec in predictions['recommendations']:
            st.markdown(f"• {rec}")

# ============================================================================
# ALERT SYSTEM
# ============================================================================

def check_alerts(energy_data: Dict, weather_data: Dict) -> List[Dict]:
    """Check for alert conditions"""
    alerts = []
    current_time = datetime.now()
    
    # Battery alerts
    if energy_data['storage_soc_percent'] < 30:
        alerts.append({
            'type': 'critical',
            'message': '🔋 CRITICAL: Low battery storage - please charge or reduce load immediately!',
            'timestamp': current_time
        })
    elif energy_data['storage_soc_percent'] < 50:
        alerts.append({
            'type': 'warning',
            'message': '⚠️ Battery storage below 50% - monitor closely.',
            'timestamp': current_time
        })
    
    # Temperature alerts
    if weather_data['temp_c'] > 40:
        alerts.append({
            'type': 'critical',
            'message': '🌡️ CRITICAL: High panel temperature detected - consider cooling measures!',
            'timestamp': current_time
        })
    elif weather_data['temp_c'] > 35:
        alerts.append({
            'type': 'warning',
            'message': '⚠️ Panel temperature rising - monitor for overheating.',
            'timestamp': current_time
        })
    
    # Generation alerts
    if energy_data['generation_watt'] < 1000 and energy_data['generation_watt'] > 0:
        alerts.append({
            'type': 'warning',
            'message': '⚡ Low power generation - check panel condition.',
            'timestamp': current_time
        })
    
    # Grid mode alerts
    if energy_data.get('is_grid_mode', False):
        alerts.append({
            'type': 'info',
            'message': '🔌 Grid mode active - no solar generation available. Grid power: {:.0f}W'.format(energy_data.get('grid_power_watt', 0)),
            'timestamp': current_time
        })
    
    # Efficiency alerts
    if energy_data['efficiency_percent'] < 75:
        alerts.append({
            'type': 'warning',
            'message': '📊 System efficiency below optimal - maintenance recommended.',
            'timestamp': current_time
        })
    
    # Health score alerts
    if energy_data.get('health_score', 100) < 70:
        alerts.append({
            'type': 'warning',
            'message': '🏥 System health below optimal - review all parameters.',
            'timestamp': current_time
        })
    
    # All systems healthy
    if not alerts:
        alerts.append({
            'type': 'success',
            'message': '✅ All systems healthy and operating normally.',
            'timestamp': current_time
        })
    
    return alerts

def display_alerts(alerts: List[Dict]):
    """Display alerts with appropriate styling"""
    if not alerts:
        return
    
    st.markdown("### 🚨 System Alerts")
    
    for alert in alerts:
        alert_class = f"alert-{alert['type']}"
        st.markdown(f"""
        <div class="{alert_class} fade-in">
            <strong>{alert['message']}</strong><br>
            <small>{alert['timestamp'].strftime('%H:%M:%S')}</small>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# DASHBOARD COMPONENTS
# ============================================================================

def display_metrics(energy_data: Dict, weather_data: Dict):
    """Display key metrics with grid power and health score"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        gen_color = "var(--success-color)" if energy_data['generation_watt'] > 0 else "var(--warning-color)"
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-value" style="color: {gen_color}">⚡ {energy_data['generation_watt']:.0f}W</div>
            <div class="metric-label">Solar Generation</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        soc_color = "var(--success-color)" if energy_data['storage_soc_percent'] > 50 else "var(--warning-color)"
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-value" style="color: {soc_color}">🔋 {energy_data['storage_soc_percent']:.1f}%</div>
            <div class="metric-label">Battery Storage</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-value">🏠 {energy_data['load_watt']:.0f}W</div>
            <div class="metric-label">Load Consumption</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        grid_color = "var(--warning-color)" if energy_data.get('is_grid_mode', False) else "var(--info-color)"
        grid_text = f"🔌 {energy_data.get('grid_power_watt', 0):.0f}W" if energy_data.get('is_grid_mode', False) else "☀️ Solar"
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-value" style="color: {grid_color}">{grid_text}</div>
            <div class="metric-label">Power Source</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        health_score = energy_data.get('health_score', 100)
        health_color = "var(--success-color)" if health_score > 80 else "var(--warning-color)" if health_score > 60 else "var(--critical-color)"
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-value" style="color: {health_color}">🏥 {health_score:.0f}%</div>
            <div class="metric-label">System Health</div>
        </div>
        """, unsafe_allow_html=True)

def display_weather_card(weather_data: Dict):
    """Display weather information"""
    st.markdown("### 🌤️ Weather Conditions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        temp_color = "var(--warning-color)" if weather_data['temp_c'] > 35 else "var(--info-color)"
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-value" style="color: {temp_color}">🌡️ {weather_data['temp_c']:.1f}°C</div>
            <div class="metric-label">Panel Temperature</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-value">☀️ {weather_data['irradiance_wm2']:.0f} W/m²</div>
            <div class="metric-label">Solar Irradiance</div>
        </div>
        """, unsafe_allow_html=True)

def create_energy_chart(energy_df: pd.DataFrame, current_idx: int):
    """Create energy generation chart"""
    # Get last 24 hours of data
    recent_data = energy_df.iloc[max(0, current_idx-288):current_idx+1]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=recent_data['timestamp'],
        y=recent_data['generation_watt'],
        mode='lines',
        name='Generation',
        line=dict(color='#ff7f0e', width=3),
        fill='tonexty'
    ))
    
    fig.add_trace(go.Scatter(
        x=recent_data['timestamp'],
        y=recent_data['load_watt'],
        mode='lines',
        name='Load',
        line=dict(color='#1f77b4', width=3),
        fill='tozeroy'
    ))
    
    fig.update_layout(
        title="⚡ Energy Generation vs Load (Last 24 Hours)",
        xaxis_title="Time",
        yaxis_title="Power (W)",
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig

def create_battery_chart(energy_df: pd.DataFrame, current_idx: int):
    """Create battery SOC chart"""
    recent_data = energy_df.iloc[max(0, current_idx-288):current_idx+1]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=recent_data['timestamp'],
        y=recent_data['storage_soc_percent'],
        mode='lines',
        name='Battery SOC',
        line=dict(color='#2ca02c', width=3),
        fill='tonexty'
    ))
    
    # Add threshold lines
    fig.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="Critical (30%)")
    fig.add_hline(y=50, line_dash="dash", line_color="orange", annotation_text="Warning (50%)")
    
    fig.update_layout(
        title="🔋 Battery State of Charge (Last 24 Hours)",
        xaxis_title="Time",
        yaxis_title="SOC (%)",
        yaxis=dict(range=[0, 100]),
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig

def create_efficiency_chart(energy_df: pd.DataFrame, current_idx: int):
    """Create system efficiency chart"""
    recent_data = energy_df.iloc[max(0, current_idx-288):current_idx+1]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=recent_data['timestamp'],
        y=recent_data['efficiency_percent'],
        mode='lines',
        name='Efficiency',
        line=dict(color='#9467bd', width=3),
        fill='tonexty'
    ))
    
    # Add threshold line
    fig.add_hline(y=75, line_dash="dash", line_color="orange", annotation_text="Optimal (75%)")
    
    fig.update_layout(
        title="📊 System Efficiency (Last 24 Hours)",
        xaxis_title="Time",
        yaxis_title="Efficiency (%)",
        yaxis=dict(range=[0, 100]),
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig

def create_grid_power_chart(energy_df: pd.DataFrame, current_idx: int):
    """Create grid power and health score chart"""
    recent_data = energy_df.iloc[max(0, current_idx-288):current_idx+1]
    
    fig = go.Figure()
    
    # Grid power
    fig.add_trace(go.Scatter(
        x=recent_data['timestamp'],
        y=recent_data['grid_power_watt'],
        mode='lines',
        name='Grid Power',
        line=dict(color='#ff6b6b', width=3),
        fill='tonexty'
    ))
    
    # Health score (secondary y-axis)
    fig.add_trace(go.Scatter(
        x=recent_data['timestamp'],
        y=recent_data['health_score'],
        mode='lines',
        name='Health Score',
        line=dict(color='#4ecdc4', width=3),
        yaxis='y2'
    ))
    
    # Add threshold lines
    fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="No Grid")
    fig.add_hline(y=70, line_dash="dash", line_color="orange", annotation_text="Health Warning (70%)", yref='y2')
    
    fig.update_layout(
        title="🔌 Grid Power & System Health (Last 24 Hours)",
        xaxis_title="Time",
        yaxis_title="Grid Power (W)",
        yaxis2=dict(title="Health Score (%)", overlaying='y', side='right', range=[0, 100]),
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

def main_dashboard():
    """Main dashboard interface"""
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>☀️ Solar Microgrid Dashboard</h1>
        <p>Welcome, {st.session_state.operator['name']} | {st.session_state.operator['role'].title()}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 Operator Info")
        st.info(f"""
        **Name:** {st.session_state.operator['name']}  
        **Phone:** {st.session_state.operator['phone_number']}  
        **Role:** {st.session_state.operator['role'].title()}  
        **Email:** {st.session_state.operator['email']}
        """)
        
        st.markdown("### ⚙️ Controls")
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.operator = None
            st.rerun()
        
        st.markdown("### 📊 System Status")
        st.markdown('<span class="status-online"></span> Online', unsafe_allow_html=True)
        st.markdown(f"**Uptime:** {(datetime.now() - st.session_state.start_time).days} days")
        st.markdown(f"**Last Update:** {datetime.now().strftime('%H:%M:%S')}")
    
    # Get current data
    energy_df, weather_df = generate_historical_data()
    current_idx = int((datetime.now() - st.session_state.start_time).total_seconds() // 5) % len(energy_df)
    
    current_energy = energy_df.iloc[current_idx]
    current_weather = weather_df.iloc[current_idx]
    
    # Convert to dict for easier access
    energy_data = {
        'generation_watt': current_energy['generation_watt'],
        'storage_soc_percent': current_energy['storage_soc_percent'],
        'load_watt': current_energy['load_watt'],
        'efficiency_percent': current_energy['efficiency_percent'],
        'grid_power_watt': current_energy['grid_power_watt'],
        'health_score': current_energy['health_score'],
        'is_grid_mode': current_energy['is_grid_mode']
    }
    
    weather_data = {
        'temp_c': current_weather['temp_c'],
        'irradiance_wm2': current_weather['irradiance_wm2']
    }
    
    # Display metrics
    display_metrics(energy_data, weather_data)
    
    # Display alerts
    alerts = check_alerts(energy_data, weather_data)
    display_alerts(alerts)
    
    # Predictive Load Management
    if st.session_state.predictive_enabled:
        predictions = predict_load_management(energy_df, current_idx)
        display_predictive_management(predictions)
    else:
        st.markdown("### 🤖 Predictive Load Management")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info("🤖 Enable predictive load management to get AI-powered recommendations for optimal energy usage.")
        with col2:
            if st.button("Enable AI Predictions", use_container_width=True):
                st.session_state.predictive_enabled = True
                st.rerun()
    
    # Charts section
    st.markdown("### 📈 Real-time Monitoring")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        energy_chart = create_energy_chart(energy_df, current_idx)
        st.plotly_chart(energy_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        battery_chart = create_battery_chart(energy_df, current_idx)
        st.plotly_chart(battery_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Grid power and health chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    grid_chart = create_grid_power_chart(energy_df, current_idx)
    st.plotly_chart(grid_chart, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Efficiency chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    efficiency_chart = create_efficiency_chart(energy_df, current_idx)
    st.plotly_chart(efficiency_chart, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Weather card
    display_weather_card(weather_data)
    
    # Auto-refresh
    time.sleep(5)
    st.rerun()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application function"""
    if not st.session_state.authenticated:
        login_form()
    else:
        main_dashboard()

def main():
    """Main function to run the Streamlit app"""
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.operator = None
        st.session_state.start_time = datetime.now()
        st.session_state.last_alert_time = {}
        st.session_state.predictive_enabled = False
        st.session_state.load_predictions = None
    
    # Main app logic
    if not st.session_state.authenticated:
        login_form()
    else:
        main_dashboard()

if __name__ == "__main__":
    main()
