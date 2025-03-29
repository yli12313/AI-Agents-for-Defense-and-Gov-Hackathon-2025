import streamlit as st
import json
import os
from pathlib import Path
import folium
from folium import plugins
from streamlit_folium import st_folium
import pandas as pd
import sys

# Add the current directory to the Python path to make imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

# Import our utility functions
from query_generator import city_to_coordinates, generate_shodan_query
from vulnerability_analyzer import analyze_vulnerabilities, get_mitigation_recommendations
from models.attack_vector_analyzer import AttackVectorAnalyzer

# Set page title and configuration
st.set_page_config(
    page_title="Port Security Intelligence Platform",
    page_icon="🛡️",
    layout="wide"
)

# Initialize session state for shared data between pages
if 'city_name' not in st.session_state:
    st.session_state.city_name = "Vladivostok"
if 'shodan_data' not in st.session_state:
    st.session_state.shodan_data = None
if 'vulnerability_analysis' not in st.session_state:
    st.session_state.vulnerability_analysis = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'coords' not in st.session_state:
    st.session_state.coords = None
if 'devices' not in st.session_state:
    st.session_state.devices = None
if 'page' not in st.session_state:
    st.session_state.page = "Port Scanner"

# Import OpenAI availability from ai_utils
try:
    from src.utils.ai_utils import OPENAI_AVAILABLE, SIMULATION_MODE
    print(f"[APP] OpenAI Available: {OPENAI_AVAILABLE}, Simulation Mode: {SIMULATION_MODE}")
except ImportError:
    OPENAI_AVAILABLE = False
    SIMULATION_MODE = False
    print("[APP] Failed to import from ai_utils, OpenAI functionality will be disabled")

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Port Scanner", "Digital Twin Dashboard"], index=0 if st.session_state.page == "Port Scanner" else 1)

# Update session state page to match navigation
st.session_state.page = page

# Functions for Digital Twin dashboard
def load_dummy_data():
    """Load dummy IoT device data from JSON file."""
    data_path = Path(__file__).parent / "data" / "dummy_data.json"
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

def create_port_map(devices, city_coords=None):
    """Create folium map with IoT devices."""
    # Use the city coordinates if provided, otherwise use San Diego as default
    if city_coords:
        center_lat = city_coords["lat"]
        center_lon = city_coords["lon"]
    else:
        # San Diego port coordinates as a default
        center_lat = 32.7157
        center_lon = -117.1611
        
    m = folium.Map(location=[center_lat, center_lon], zoom_start=15)
    
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
        norm_lat = center_lat + (device["location"][1] - 0.5) * 0.01
        norm_lng = center_lon + (device["location"][0] - 0.5) * 0.01
        
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
    
    # Add a marker for the shodan result if available
    if st.session_state.shodan_data:
        shodan_data = st.session_state.shodan_data
        if "latitude" in shodan_data and "longitude" in shodan_data:
            folium.Marker(
                [shodan_data["latitude"], shodan_data["longitude"]],
                popup=f"""
                <b>Shodan Result: {shodan_data.get('ip_str', 'Unknown')}</b><br>
                Organization: {shodan_data.get('org', 'Unknown')}<br>
                Country: {shodan_data.get('country_name', 'Unknown')}
                """,
                tooltip="Shodan Result",
                icon=folium.Icon(color="purple", icon="globe", prefix="fa")
            ).add_to(m)
    
    return m

def convert_shodan_to_device(shodan_data, vulnerability_analysis):
    """Convert Shodan data to a device format compatible with our system."""
    if not shodan_data or not vulnerability_analysis:
        return None
    
    # Create a device entry from Shodan data
    device = {
        "name": f"Port System {shodan_data.get('ip_str', 'Unknown')}",
        "device_type": "ICS/SCADA",
        "location": [0.5, 0.5],  # Center of the map (will be adjusted)
        "vuln_score": vulnerability_analysis.get("risk_score", 5.0) / 10.0 * 10.0,  # Convert to 0-10 scale
        "cves": shodan_data.get("vulns", []),
        "description": f"Port system in {shodan_data.get('city', 'Unknown')}, {shodan_data.get('country_name', 'Unknown')}"
    }
    
    return device

# Port Scanner Page
if page == "Port Scanner":
    st.title("Port City Vulnerability Scanner")
    st.markdown("Search for potentially vulnerable Industrial Control Systems (ICS) in port cities worldwide.")

    # Create a two-column layout
    col1, col2 = st.columns([1, 2])

    # Input form in the first column
    with col1:
        st.subheader("Search Parameters")
        with st.form("search_form"):
            city_name = st.text_input("Enter Port City Name:", st.session_state.city_name)
            search_term = st.text_input("Search Term:", "ICS")
            radius = st.slider("Search Radius (km):", 1, 20, 5)
            submitted = st.form_submit_button("Search")
            proceed_to_dashboard = st.form_submit_button("Search & View Dashboard")

    # Display results in the second column
    with col2:
        # When form is submitted
        if submitted or proceed_to_dashboard:
            # Update session state with city name
            st.session_state.city_name = city_name
            
            # Generate the query
            query, coords = generate_shodan_query(city_name, search_term, radius)
            
            # Store coordinates in session state
            st.session_state.coords = coords
            
            if not coords:
                st.error(query)  # Display error message
            else:
                # Display the query that would be sent to Shodan
                st.subheader("Generated Shodan Query:")
                st.code(query)
                
                # Display a map with the coordinates
                st.subheader("Search Location:")
                map_data = pd.DataFrame({
                    "lat": [coords["lat"]],
                    "lon": [coords["lon"]]
                })
                st.map(map_data)
                
                # In a real implementation, this would call the Shodan API
                # For our simulation, load the sample JSON
                st.subheader("Simulation Results:")
                
                # Load sample data - find the correct path
                current_dir = Path(__file__).parent
                sample_path = current_dir / "data" / "shodan" / "samples" / "clean_sample.json"
                
                try:
                    with open(sample_path, "r") as f:
                        sample_data = json.load(f)
                    
                    # Update the sample data with the searched city
                    sample_data["city"] = city_name
                    if "latitude" not in sample_data or "longitude" not in sample_data:
                        sample_data["latitude"] = coords["lat"]
                        sample_data["longitude"] = coords["lon"]
                    
                    # Run vulnerability analysis
                    analysis = analyze_vulnerabilities(sample_data)
                    recommendations = get_mitigation_recommendations(analysis)
                    
                    # Store results in session state for the dashboard
                    st.session_state.shodan_data = sample_data
                    st.session_state.vulnerability_analysis = analysis
                    st.session_state.recommendations = recommendations
                    
                    # Convert Shodan data to device format for the dashboard
                    shodan_device = convert_shodan_to_device(sample_data, analysis)
                    
                    # Load existing devices
                    devices = load_dummy_data()
                    
                    # Add the Shodan result as a device if it exists
                    if shodan_device:
                        devices = [d for d in devices if d.get("name") != shodan_device["name"]]  # Remove old version if exists
                        devices.append(shodan_device)
                    
                    # Store devices in session state
                    st.session_state.devices = devices
                    
                    # Display risk score with gauge
                    risk_score = analysis["risk_score"]
                    risk_level = analysis["risk_level"]
                    
                    # Color based on risk level
                    color = {
                        "HIGH": "red",
                        "MEDIUM": "orange",
                        "LOW": "green"
                    }.get(risk_level, "blue")
                    
                    st.markdown(f"### Risk Assessment: <span style='color:{color}'>{risk_level}</span>", unsafe_allow_html=True)
                    st.markdown(f"Risk Score: {risk_score}/10")
                    
                    # Create a progress bar for visual indication
                    st.progress(risk_score / 10)
                    
                    # Display basic info
                    st.markdown(f"**IP Address:** {sample_data['ip_str']}")
                    st.markdown(f"**Location:** {sample_data['city']}, {sample_data['country_name']}")
                    st.markdown(f"**Organization:** {sample_data['org']}")
                    
                    # Display vulnerabilities
                    if analysis["vulnerabilities"]:
                        st.subheader("Identified Vulnerabilities:")
                        for vuln in analysis["vulnerabilities"]:
                            severity_color = "red" if vuln["severity"] >= 9.0 else "orange" if vuln["severity"] >= 7.0 else "green"
                            st.markdown(f"* **{vuln['id']}** - <span style='color:{severity_color}'>{vuln['severity']}</span>/10: {vuln['description']}", unsafe_allow_html=True)
                    
                    # Display open services in a table
                    if analysis["open_services"]:
                        st.subheader("Open Services:")
                        service_data = []
                        for service in analysis["open_services"]:
                            service_data.append({
                                "Port": service["port"],
                                "Service": service["service"],
                                "Product": service["product"],
                                "Version": service["version"],
                                "Risk Level": f"{service['risk'] * 10:.1f}/10"
                            })
                        
                        st.table(pd.DataFrame(service_data))
                    
                    # Display recommendations
                    if recommendations:
                        with st.expander("Security Recommendations", expanded=True):
                            for rec in recommendations:
                                if rec.startswith("CRITICAL") or rec.startswith("URGENT"):
                                    st.markdown(f"🚨 **{rec}**")
                                elif rec.startswith("HIGH"):
                                    st.markdown(f"⚠️ **{rec}**")
                                else:
                                    st.markdown(f"ℹ️ {rec}")
                    
                    # Display the raw JSON in an expander
                    with st.expander("Raw JSON Response", expanded=False):
                        st.json(sample_data)
                        
                    # Add a button to view the digital twin dashboard
                    if proceed_to_dashboard or st.button("View Digital Twin Dashboard"):
                        st.session_state.page = "Digital Twin Dashboard"
                        st.rerun()
                    
                except Exception as e:
                    st.error(f"Error processing data: {e}")
                    st.info(f"Make sure the sample data is available at: {sample_path}")

    # Add a footer with information
    st.markdown("---")
    st.markdown("""
    **Note:** This is a simulation using sample data. In a production environment, 
    this would connect to the Shodan API to retrieve real vulnerability data.
    """)

# Digital Twin Dashboard Page
else:  # page == "Digital Twin Dashboard"
    st.title(f"Maritime Port Digital Twin: {st.session_state.city_name}")
    
    # Load devices from session state or from file if not available
    devices = st.session_state.devices if st.session_state.devices else load_dummy_data()
    
    # Initialize the attack vector analyzer with all devices
    analyzer = AttackVectorAnalyzer(devices)
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Port Map")
        if devices:
            port_map = create_port_map(devices, st.session_state.coords)
            st_folium(port_map, width=800)
        else:
            st.info("No device data available for map visualization")
        
        # Advanced Attack vector analysis section
        st.subheader("AI-Enhanced Attack Vector Analysis")
        
        use_ai = st.checkbox("Use AI for enhanced analysis", value=True)
        
        if 'shodan_data' in st.session_state and st.session_state.shodan_data:
            st.info(f"Including data from Shodan scan of {st.session_state.city_name} in the analysis")
        
        # Display OpenAI API status
        if use_ai:
            if OPENAI_AVAILABLE:
                if SIMULATION_MODE:
                    st.success("AI-enhanced analysis is available in simulation mode")
                else:
                    st.success("AI-enhanced analysis is available using the OpenAI API")
            else:
                st.warning("OpenAI package not installed - Using rule-based analysis instead")
        
        if st.button("Generate Attack Vector Analysis"):
            with st.spinner("Analyzing potential attack vectors..."):
                # Ensure the AttackVectorAnalyzer uses the same criteria we're displaying
                print(f"[APP] Generating attack vector analysis. Use AI: {use_ai}, OpenAI Available: {OPENAI_AVAILABLE}")
                analysis_result = analyzer.analyze(use_ai=use_ai and OPENAI_AVAILABLE)
                print(f"[APP] Analysis complete. Success: {analysis_result['success']}")
                
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
        
        # Show Shodan result first if available
        if 'shodan_data' in st.session_state and st.session_state.shodan_data and 'vulnerability_analysis' in st.session_state and st.session_state.vulnerability_analysis:
            shodan_data = st.session_state.shodan_data
            analysis = st.session_state.vulnerability_analysis
            
            risk_level = analysis["risk_level"]
            status_emoji = {
                "HIGH": "🔴",
                "MEDIUM": "🟡",
                "LOW": "🟢"
            }.get(risk_level, "⚪")
            
            with st.expander(f"Shodan Result: {shodan_data.get('ip_str', 'Unknown')} {status_emoji}", expanded=True):
                st.markdown(f"""
                **Type**: ICS/SCADA System  
                **Organization**: {shodan_data.get('org', 'Unknown')}  
                **Location**: {shodan_data.get('city', 'Unknown')}, {shodan_data.get('country_name', 'Unknown')}  
                **Risk Score**: {analysis.get('risk_score', 0)}/10  
                **Status**: {risk_level}  
                **Vulnerabilities**: {', '.join(shodan_data.get('vulns', ['None']))}
                """)
        
        # Show all other devices
        if devices:
            for device in devices:
                # Skip if this is the converted Shodan device and we already displayed it
                if 'shodan_data' in st.session_state and st.session_state.shodan_data:
                    shodan_ip = st.session_state.shodan_data.get('ip_str', '')
                    if shodan_ip in device.get('name', ''):
                        continue
                
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
        
        # Add a button to go back to the port scanner
        if st.button("Back to Port Scanner"):
            st.session_state.page = "Port Scanner"
            st.rerun()

# Add functionality to switch between pages based on session state
if 'page' in st.session_state and st.session_state.page != page:
    st.session_state.page = page
    st.rerun() 