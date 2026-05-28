import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import config
from detection import FastenerDetector
from dummy_camera import DummyCamera

# Konfigurasi halaman
st.set_page_config(
    page_title="Warehouse Fastener Monitor",
    page_icon="🔩",
    layout="wide"
)

# Custom CSS Industrial Style
st.markdown("""
<style>
    .stApp {
        background-color: #1e1e1e;
    }
    .status-full {
        background-color: #00FF00;
        padding: 20px;
        border-radius: 10px;
        color: black;
        font-weight: bold;
        text-align: center;
    }
    .status-medium {
        background-color: #FFFF00;
        padding: 20px;
        border-radius: 10px;
        color: black;
        font-weight: bold;
        text-align: center;
    }
    .status-low {
        background-color: #FFA500;
        padding: 20px;
        border-radius: 10px;
        color: black;
        font-weight: bold;
        text-align: center;
    }
    .status-empty {
        background-color: #FF0000;
        padding: 20px;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        text-align: center;
    }
    .warning-box {
        background-color: #FF4444;
        padding: 15px;
        border-radius: 5px;
        animation: blink 1s infinite;
    }
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🏭 AI Camera Monitoring System")
st.subheader("Fastener Stock Level - Polybox Area")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    use_dummy = st.checkbox("Use Dummy Camera (Simulation)", value=True)
    material_name = st.text_input("Material Name", value=config.MATERIAL_NAME)
    refresh_rate = st.slider("Refresh Rate (seconds)", 0.5, 5.0, 1.0)
    
    st.markdown("---")
    st.markdown("### Threshold Level")
    for level, cfg in config.LEVEL_CONFIG.items():
        st.metric(level, f"{cfg['min']}% - {cfg['max']}%")

# Main columns
col1, col2 = st.columns([2, 1])

# Inisialisasi detector
detector = FastenerDetector()

# Pilihan kamera
if use_dummy:
    cap = DummyCamera()
    is_dummy = True
else:
    try:
        cap = cv2.VideoCapture(0)
        is_dummy = False
    except:
        st.error("Webcam not found! Switching to dummy mode.")
        cap = DummyCamera()
        is_dummy = True

# Placeholder untuk live video
frame_placeholder = col1.empty()
status_placeholder = col2.empty()
warning_placeholder = st.empty()

# Monitoring loop
st.info("🟢 Monitoring Active... Press Stop to end.")

stop_button = st.button("⏹️ Stop Monitoring")

while not stop_button:
    # Baca frame
    ret, frame = cap.read()
    if not ret:
        if is_dummy:
            # Dummy camera continue
            pass
        else:
            st.error("Failed to capture frame")
            break
    
    # Process frame
    fill_ratio, level, vis_frame, _ = detector.process_frame(frame)
    
    # Display video
    if vis_frame is not None:
        vis_frame_rgb = cv2.cvtColor(vis_frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(vis_frame_rgb, channels="RGB", use_column_width=True)
    
    # Status display
    status_color = config.LEVEL_CONFIG[level]["color"]
    status_html = f"""
    <div class="status-{level.lower()}">
        <h2>{level}</h2>
        <h3>{fill_ratio:.1f}% Filled</h3>
    </div>
    """
    status_placeholder.markdown(status_html, unsafe_allow_html=True)
    
    # Metrics
    col2.metric("Fill Ratio", f"{fill_ratio:.1f}%")
    col2.metric("Material", material_name)
    col2.metric("Status", level)
    
    # Warning
    if level in ["LOW", "EMPTY"]:
        warning_placeholder.warning(f"⚠️ WARNING: Stock {level}! Immediate replenishment required for {material_name} ⚠️")
    else:
        warning_placeholder.empty()
    
    time.sleep(refresh_rate)

# Cleanup
if not is_dummy:
    cap.release()
st.success("Monitoring stopped.")