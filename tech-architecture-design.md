# Technical Architecture Design

## Overview

This architecture is designed for a maritime port digital twin system. The core components of the system include data ingestion, data visualization, and AI-driven insights. The system provides a real-time security dashboard with vulnerability analysis, attack vector recommendation, and dynamic IoT device tracking. We will use Render as the hosting platform, with a focus on simplicity and scalability for the MVP.

## Technology Stack

### Backend
- **Programming Language**: Python (for ease of development and integration with AI models)
- **Framework**: 
  - Streamlit for the front-end UI
  - Flask for backend API (if needed in Phase 2 for integrating real-time data or advanced operations)
- **Data Source**: 
  - JSON files for initial dummy data
  - Integration with Shodan API for Phase 1.2 (to retrieve IoT device vulnerability data)
- **Storage**: 
  - In-memory JSON or a simple file-based system (for initial prototypes)
  - Local storage or cloud storage (for future scalability)
  
### Frontend (UI)
- **Framework**: 
  - Streamlit for rapid prototyping and front-end development
- **Libraries**:
  - PIL (Pillow) for image handling
  - `folium` or `st_canvas` (optional for advanced visualizations)
  - OpenAI API integration (if required for AI-driven attack vector recommendations)
- **Visualization**: 
  - Static map overlays for IoT devices
  - Color-coded RAG (Red-Amber-Green) visual status for devices
  - AI-driven Attack Vector Advisor

### Hosting/Deployment
- **Platform**: Render (for simplicity, scalability, and ease of deployment)
  - **Render Hosting**: We'll use Render to deploy the Streamlit app with backend services (if needed) and host the static data.
  - **Rendering Data**: The backend will be responsible for loading IoT device data from JSON files and integrating it with Streamlit.
  - **Live Monitoring**: Render will support the easy deployment and live updates of the dashboard.
  
### Additional Components
- **Version Control**: GitHub for version control and collaboration during development.
- **CI/CD**: GitHub Actions (for automatic deployment to Render on commits).
- **API Integration**: Integration with Shodan API (for real-time data in Phase 1.2).

## Architecture Flow

1. **Frontend (Streamlit App)**: 
   - Streamlit displays the map and IoT devices with RAG scores.
   - Users can interact with the application to trigger analysis, visualize attack vectors, and simulate ship arrivals.

2. **Backend**: 
   - The backend will fetch the device data (either static or real-time) and serve it to the frontend.
   - In Phase 1.1, static JSON will simulate device data.
   - In Phase 1.2, data will be fetched dynamically using the Shodan API, representing live data from IoT devices.
   
3. **Deployment on Render**: 
   - The app will be hosted on Render, which provides a scalable environment for deploying both the backend and frontend.
   - Continuous deployment through GitHub Actions for streamlined updates.

## Flow Diagram

```plaintext
+--------------------+         +-------------------+
|  User Interface    |         |    Backend API    |
|   (Streamlit)      | <-----> | (Flask/Streamlit) |
+--------------------+         +-------------------+
             |                           |
             v                           v
     +---------------+        +-------------------+
     |  Render Hosting|        |    Shodan API    |
     |   Platform    | <-----> |    (Real-time)   |
     +---------------+        +-------------------+
