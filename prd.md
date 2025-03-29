# Product Requirements Document - Maritime Port Digital Twin

## Introduction
This product is a digital twin of a maritime port designed to visualize IoT devices, track vulnerabilities, and suggest potential attack vectors. The dashboard will serve port security teams, offering a real-time overview of vulnerabilities and security risks.

## Goals:
- Provide a comprehensive view of IoT device vulnerabilities.
- Visualize IoT devices on a port map with RAG statuses.
- Offer an AI-driven attack vector analysis based on device vulnerabilities.

## Features:
1. **IoT Device Visualization**: Map IoT devices with RAG statuses.
2. **Attack Vector Advisor**: Generate AI-based or rule-based attack vector suggestions.
3. **Ship Arrival Simulation**: Allow simulation of ship arrivals with new IoT devices.

## User Stories:
- **As a user**, I want to see a map of IoT devices on the port with their vulnerabilities, so I can identify the most critical devices.
- **As a security analyst**, I want to receive suggestions for potential attack vectors based on device vulnerabilities.

## Technical Requirements:
- Streamlit for UI.
- Python backend for data handling and logic.
- Integration with Shodan API for real-time data in Phase 1.2.
