import streamlit as st
import cv2
import numpy as np
import random
import time

# Konfigurasi level stock
LEVEL_CONFIG = {
    "FULL": {"min": 75, "max": 100, "color": "green", "label": "FULL"},
    "MEDIUM": {"min": 50, "max": 75, "color": "yellow", "label": "MEDIUM"},
    "LOW": {"min": 20, "max": 50, "color": "orange", "label": "LOW"},
    "EMPTY": {"min": 0, "max": 20, "color": "red", "label": "EMPTY"},
}

st.set_page_config(page_title="Warehouse Fastener Monitor", page_icon="🔩", layout="wide")

st.title("🏭 AI Camera Monitoring System")
st.subheader("Fastener Stock Level - Polybox Area")

# Mode dummy (karena webcam tidak bisa di cloud)
use_dummy = st.checkbox("Use Demo Mode", value=True)

if use_dummy:
    # Simulasi random level
    levels = ["FULL", "MEDIUM", "LOW", "EMPTY"]
    colors = {"FULL": "#00FF00", "MEDIUM": "#FFFF00", "LOW": "#FFA500", "EMPTY": "#FF0000"}
    
    # Auto refresh
    refresh = st.empty()
    
    while True:
        level = random.choice(levels)
        percentage = random.uniform(LEVEL_CONFIG[level]["min"], LEVEL_CONFIG[level]["max"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Current Stock Level", f"{percentage:.1f}%")
            st.markdown(f"""
            <div style="background-color:{colors[level]}; padding:20px; border-radius:10px; text-align:center">
                <h2>{level}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric("Material", "Hex Bolt M6 x 12mm")
            st.metric("Location", "Polybox A1 - Warehouse")
        
        if level in ["LOW", "EMPTY"]:
            st.warning(f"⚠️ WARNING: Stock {level}! Immediate replenishment required ⚠️")
        
        time.sleep(2)
        refresh.empty()
        with refresh.container():
            continue
else:
    st.info("Demo mode is recommended for cloud deployment. Webcam requires local execution.")

st.success("System Ready - Monitoring Fastener Stock")