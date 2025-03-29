import streamlit as st
import json
from pathlib import Path
import folium
from streamlit_folium import folium_static
import numpy as np
import os
import sys

# Add the current directory to the Python path to make imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

from src.models.attack_vector_analyzer import AttackVectorAnalyzer

# Set page config
st.set_page_config(
    page_title="Maritime Port Digital Twin",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply dark theme CSS
st.markdown("""
<style>
    /* Dark mode for the entire app */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Dark mode for sidebar */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #262730;
    }
    
    /* Dark mode for widgets */
    .stButton>button, .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #262730;
        color: white;
        border-color: #4e4e4e;
    }
    
    /* Dark mode for expanders */
    .streamlit-expanderHeader {
        background-color: #262730;
        color: white;
    }
    
    /* Dark mode for the folium map container */
    .folium-map {
        background-color: #0e1117 !important;
    }
    
    /* Remove white space around the map */
    .leaflet-container {
        background-color: #0e1117 !important;
        border: none !important;
    }
    
    /* Dark theme for map controls */
    .leaflet-control-zoom, .leaflet-control-layers {
        background-color: #262730 !important;
        border-color: #4e4e4e !important;
    }
    
    .leaflet-control-zoom a, .leaflet-control-layers a {
        color: #ffffff !important;
        background-color: #262730 !important;
    }
    
    /* Remove any white borders */
    .leaflet-container .leaflet-overlay-pane svg, 
    .leaflet-container .leaflet-marker-pane img, 
    .leaflet-container .leaflet-shadow-pane img, 
    .leaflet-container .leaflet-tile-pane img, 
    .leaflet-container img.leaflet-image-layer {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* Make the map fill the available space */
    .element-container:has(.folium-map) {
        width: 100% !important;
    }
    
    /* Dark theme for map popups */
    .leaflet-popup-content-wrapper, .leaflet-popup-tip {
        background-color: #262730 !important;
        color: white !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Set a default OpenAI API key for demonstration
# In production, this should be set via environment variables
if "OPENAI_API_KEY" not in os.environ:
    # Try to get from secrets, but handle the case when no secrets file exists
    try:
        os.environ["OPENAI_API_KEY"] = st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        os.environ["OPENAI_API_KEY"] = ""  # Set to empty string if no secrets found

def load_dummy_data():
    """Load dummy IoT device data from JSON file."""
    data_path = Path("src/data/dummy_data.json")
    if data_path.exists():
        with open(data_path, "r") as f:
            return json.load(f)
    return []

def calculate_rag_status(vuln_score):
    """Calculate RAG (Red-Amber-Green) status based on vulnerability score."""
    if vuln_score >= 7:
        return "RED"
    elif vuln_score >= 4:
        return "AMBER"
    return "GREEN"

def get_status_color(status):
    """Get color based on RAG status."""
    return {
        "RED": "red",
        "AMBER": "orange",
        "GREEN": "green"
    }.get(status, "blue")

def create_port_map(devices):
    """Create folium map with IoT devices."""
    # Create a map centered on an example maritime port with dark theme
    # San Diego port coordinates as an example
    m = folium.Map(
        location=[32.7157, -117.1611], 
        zoom_start=15,
        tiles="CartoDB dark_matter",  # Use dark tiles
        attr="CartoDB"
    )
    
    # Add dark satellite imagery
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Dark Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Plot devices on the map
    for device in devices:
        # Normalize coordinates to map view (dummy data uses 0-1 range)
        # In real implementation, use actual lat/long
        norm_lat = 32.7157 + (device["location"][1] - 0.5) * 0.01
        norm_lng = -117.1611 + (device["location"][0] - 0.5) * 0.01
        
        status = calculate_rag_status(device.get("vuln_score", 0))
        color = get_status_color(status)
        
        # Add marker for each device
        folium.Marker(
            [norm_lat, norm_lng],
            popup=f"""
            <div style="background-color: #262730; color: white; padding: 5px; border-radius: 3px;">
                <b>{device.get('name', 'Unknown')}</b><br>
                Type: {device.get('device_type', 'Unknown')}<br>
                Vulnerability Score: {device.get('vuln_score', 0)}<br>
                Status: {status}
            </div>
            """,
            tooltip=device.get("name", "Device"),
            icon=folium.Icon(color=color, icon="server", prefix="fa")
        ).add_to(m)
    
    return m

def main():
    st.title("Maritime Port Digital Twin")
    
    # Load dummy data
    devices = load_dummy_data()
    
    # Initialize the attack vector analyzer
    analyzer = AttackVectorAnalyzer(devices)
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Port Map")
        if devices:
            port_map = create_port_map(devices)
            # Use the full width available and add custom CSS for the map
            folium_static(port_map, width=800)
        else:
            st.info("No device data available for map visualization")
        
        # Advanced Attack vector analysis section
        st.subheader("AI-Enhanced Attack Vector Analysis")
        
        use_ai = st.checkbox("Use AI for enhanced analysis", value=True)
        
        if st.button("Generate Attack Vector Analysis"):
            with st.spinner("Analyzing potential attack vectors..."):
                # Check if OpenAI API key is available
                if use_ai and not os.environ.get("OPENAI_API_KEY"):
                    st.warning("No OpenAI API key found. Using rule-based analysis instead.")
                    use_ai = False
                
                # Perform the analysis
                analysis_result = analyzer.analyze(use_ai=use_ai)
                
                if analysis_result["success"]:
                    # Display risk score with gauge
                    risk_score = analysis_result["risk_score"]
                    st.markdown(f"### Overall Risk Score: {risk_score}/10")
                    
                    # Create a simple gauge visualization
                    risk_color = "green" if risk_score < 4 else "orange" if risk_score < 7 else "red"
                    st.progress(risk_score / 10)
                    
                    # Display statistics
                    stats_col1, stats_col2 = st.columns(2)
                    with stats_col1:
                        st.metric("High Vulnerability Devices", analysis_result["high_vuln_count"])
                    with stats_col2:
                        st.metric("Average Vulnerability Score", analysis_result["avg_vuln_score"])
                    
                    # Display attack vector
                    st.markdown("## Attack Vector Analysis")
                    st.markdown(analysis_result["attack_vector"])
                    
                    # Option to save analysis
                    if st.button("Save Analysis"):
                        output_path = analyzer.save_analysis(analysis_result)
                        st.success(f"Analysis saved to {output_path}")
                else:
                    st.error(f"Analysis failed: {analysis_result['error']}")
    
    with col2:
        st.subheader("Device List")
        if devices:
            for device in devices:
                status = calculate_rag_status(device.get("vuln_score", 0))
                status_color = {
                    "RED": "🔴",
                    "AMBER": "🟡",
                    "GREEN": "🟢"
                }.get(status, "⚪")
                
                with st.expander(f"{device.get('name', 'Unknown Device')} {status_color}"):
                    st.markdown(f"""
                    **Type**: {device.get('device_type', 'Unknown')}  
                    **Vulnerability Score**: {device.get('vuln_score', 0)}  
                    **Status**: {status}  
                    **CVEs**: {', '.join(device.get('cves', ['None']))}
                    """)
        else:
            st.warning("No device data available")
        
        # Simulate ship arrival
        st.subheader("Simulate Ship Arrival")
        if st.button("Add Ship with IoT Devices"):
            st.info("Ship arrival simulation will be implemented by frontend team")

if __name__ == "__main__":
    main()