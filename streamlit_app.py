import streamlit as st
import random
import time

# Konfigurasi level stock
LEVEL_CONFIG = {
    "FULL": {"min": 75, "max": 100, "color": "#00FF00", "label": "🟢 FULL"},
    "MEDIUM": {"min": 50, "max": 75, "color": "#FFFF00", "label": "🟡 MEDIUM"},
    "LOW": {"min": 20, "max": 50, "color": "#FFA500", "label": "🟠 LOW"},
    "EMPTY": {"min": 0, "max": 20, "color": "#FF0000", "label": "🔴 EMPTY"},
}

# Konfigurasi halaman
st.set_page_config(
    page_title="Warehouse Fastener Monitor",
    page_icon="🔩",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #1e1e1e;
    }
    .status-card {
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🏭 AI Camera Monitoring System")
st.subheader("Fastener Stock Level - Polybox Area (Warehouse Produksi Motor Roda 3)")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("### Material Information")
    st.write("**Nama:** Hex Bolt M6 x 12mm")
    st.write("**Grade:** 8.8")
    st.write("**Lokasi:** Polybox Biru - Line A")
    st.markdown("---")
    st.markdown("### Stock Threshold")
    for level, cfg in LEVEL_CONFIG.items():
        st.markdown(f"{cfg['label']} : {cfg['min']}% - {cfg['max']}%")

# Main content
col1, col2 = st.columns([2, 1])

# Placeholder untuk auto refresh
placeholder = st.empty()

# Simulasi data (karena webcam tidak bisa di cloud)
st.info("📹 **Demo Mode Aktif** - Menampilkan simulasi level stock (karena cloud tidak punya akses webcam)")

# Auto-refresh loop
auto_refresh = st.checkbox("Auto Refresh (Real-time Monitoring)", value=True)
refresh_rate = st.slider("Refresh Rate (seconds)", 1, 5, 2) if auto_refresh else 0

def get_random_level():
    """Simulasi perubahan stock level"""
    # Simulasi lebih realistis: cenderung turun perlahan
    if 'current_level' not in st.session_state:
        st.session_state.current_level = "FULL"
        st.session_state.percentage = 85.0
    
    # Random change -5% sampai +2%
    change = random.uniform(-5, 2)
    st.session_state.percentage += change
    st.session_state.percentage = max(0, min(100, st.session_state.percentage))
    
    # Tentukan level berdasarkan percentage
    for level, cfg in LEVEL_CONFIG.items():
        if cfg["min"] <= st.session_state.percentage <= cfg["max"]:
            st.session_state.current_level = level
            break
    
    return st.session_state.current_level, st.session_state.percentage

if auto_refresh:
    level, percentage = get_random_level()
else:
    # Jika auto refresh mati, pilih manual
    level = st.selectbox("Pilih Level (Manual)", list(LEVEL_CONFIG.keys()))
    percentage = st.slider("Persentase Isi (%)", 0, 100, LEVEL_CONFIG[level]["min"])

# Tampilkan status
color = LEVEL_CONFIG[level]["color"]
label = LEVEL_CONFIG[level]["label"]

with col1:
    st.markdown(f"""
    <div class="status-card" style="background-color:{color};">
        <h1 style="font-size:48px; margin:0;">{label}</h1>
        <h2 style="font-size:36px;">{percentage:.1f}% Filled</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    st.progress(int(percentage))

with col2:
    st.metric("📦 Material Stock", f"{percentage:.1f}%", delta=None)
    st.metric("🏷️ Material Name", "Hex Bolt M6 x 12mm")
    st.metric("📍 Location", "Polybox Biru - Warehouse A")
    st.metric("📊 Status", level)

# Warning
if level in ["LOW", "EMPTY"]:
    st.error(f"⚠️ **WARNING!** Stock {level}! Segera lakukan replenishment baut M6 x 12mm. ⚠️")
else:
    st.success("✅ Stock aman. Monitoring berjalan normal.")

# Informasi tambahan
with st.expander("📋 Informasi Sistem"):
    st.write("""
    **Cara Kerja Sistem:**
    - Kamera mendeteksi polybox biru
    - AI menghitung persentase area yang terisi baut
    - Hasil diklasifikasikan: FULL, MEDIUM, LOW, EMPTY
    
    **Catatan untuk Implementasi Industri:**
    - Ganti mode dummy dengan webcam jika dijalankan lokal
    - Kalibrasi threshold sesuai jenis baut
    - Integrasi dengan ERP untuk reorder otomatis
    """)

# Auto refresh logic
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()