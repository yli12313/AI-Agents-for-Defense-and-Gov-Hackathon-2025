import streamlit as st
import json
from pathlib import Path
import folium
from streamlit_folium import folium_static
import numpy as np

# Set page config
st.set_page_config(
    page_title="Maritime Port Digital Twin",
    page_icon="🚢",
    layout="wide"
)

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
    # Create a map centered on an example maritime port
    # San Diego port coordinates as an example
    m = folium.Map(location=[32.7157, -117.1611], zoom_start=15)
    
    # Add background satellite imagery
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite',
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
            <b>{device.get('name', 'Unknown')}</b><br>
            Type: {device.get('device_type', 'Unknown')}<br>
            Vulnerability Score: {device.get('vuln_score', 0)}<br>
            Status: {status}
            """,
            tooltip=device.get("name", "Device"),
            icon=folium.Icon(color=color, icon="server", prefix="fa")
        ).add_to(m)
    
    return m

def generate_attack_vector(devices):
    """Generate a basic attack vector based on device vulnerabilities."""
    if not devices:
        return "No devices available for attack vector analysis."
    
    # Sort devices by vulnerability score in descending order
    vulnerable_devices = sorted(devices, key=lambda x: x.get("vuln_score", 0), reverse=True)
    
    # If any device has a high vulnerability score (RED status)
    high_vuln_devices = [d for d in vulnerable_devices if d.get("vuln_score", 0) >= 7]
    if high_vuln_devices:
        entry_point = high_vuln_devices[0]
        
        # Find other vulnerable devices for lateral movement
        lateral_targets = [d for d in vulnerable_devices if d != entry_point and d.get("vuln_score", 0) >= 4]
        
        attack_vector = f"""
        ### Potential Attack Path

        1. **Entry Point**: {entry_point.get('name', 'Unknown Device')} ({entry_point.get('device_type', 'Unknown')})
           - Vulnerability Score: {entry_point.get('vuln_score', 0)}
           - CVEs: {', '.join(entry_point.get('cves', ['None']))}
        
        2. **Attack Strategy**:
           - Exploit vulnerabilities in {entry_point.get('name', 'entry point')} to gain initial access
        """
        
        if lateral_targets:
            attack_vector += "\n3. **Lateral Movement Targets**:"
            for i, target in enumerate(lateral_targets[:3]):
                attack_vector += f"""
           - {target.get('name', 'Unknown')} ({target.get('device_type', 'Unknown')}) - Vuln Score: {target.get('vuln_score', 0)}"""
        
        return attack_vector
    else:
        return "No high-vulnerability devices detected. Focus on hardening medium vulnerability devices."

def main():
    st.title("Maritime Port Digital Twin")
    
    # Load dummy data
    devices = load_dummy_data()
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Port Map")
        if devices:
            port_map = create_port_map(devices)
            folium_static(port_map, width=800)
        else:
            st.info("No device data available for map visualization")
        
        # Attack vector analysis section
        st.subheader("Attack Vector Analysis")
        if st.button("Generate Attack Vector Analysis"):
            with st.spinner("Analyzing potential attack vectors..."):
                attack_vector = generate_attack_vector(devices)
                st.markdown(attack_vector)
    
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