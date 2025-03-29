import streamlit as st
import json
import os
import pandas as pd
from pathlib import Path

# Import our utility functions
from query_generator import city_to_coordinates, generate_shodan_query
from vulnerability_analyzer import analyze_vulnerabilities, get_mitigation_recommendations

# Set page title and configuration
st.set_page_config(
    page_title="Port City Vulnerability Scanner",
    page_icon="🔍",
    layout="wide"
)

st.title("Port City Vulnerability Scanner")
st.markdown("Search for potentially vulnerable Industrial Control Systems (ICS) in port cities worldwide.")

# Create a two-column layout
col1, col2 = st.columns([1, 2])

# Input form in the first column
with col1:
    st.subheader("Search Parameters")
    with st.form("search_form"):
        city_name = st.text_input("Enter Port City Name:", "Vladivostok")
        search_term = st.text_input("Search Term:", "ICS")
        radius = st.slider("Search Radius (km):", 1, 20, 5)
        submitted = st.form_submit_button("Search")

# Display results in the second column
with col2:
    # When form is submitted
    if submitted:
        # Generate the query
        query, coords = generate_shodan_query(city_name, search_term, radius)
        
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
                
                # Run vulnerability analysis
                analysis = analyze_vulnerabilities(sample_data)
                recommendations = get_mitigation_recommendations(analysis)
                
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
                
            except Exception as e:
                st.error(f"Error processing data: {e}")
                st.info(f"Make sure the sample data is available at: {sample_path}")

# Add a footer with information
st.markdown("---")
st.markdown("""
**Note:** This is a simulation using sample data. In a production environment, 
this would connect to the Shodan API to retrieve real vulnerability data.
""") 