# AI-Agents-for-Defense-and-Gov-Hackathon-2025
This is the team's submission to the SCSP and AGI House Hackathon (Mar. 2025)!

# Maritime Port Digital Twin

A digital twin system for maritime ports that visualizes IoT devices, tracks vulnerabilities, and suggests potential attack vectors.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run src/app.py
```

## Project Structure

```
.
├── src/
│   ├── app.py              # Main Streamlit application
│   ├── data/               # Data files
│   │   └── dummy_data.json  # Sample IoT device data
│   ├── models/            # Data models and business logic
│   └── utils/             # Utility functions
├── tests/                 # Test files
├── requirements.txt       # Project dependencies
└── README.md            # This file
```

## Features

- IoT Device Visualization
- RAG (Red-Amber-Green) Status System
- Device Vulnerability Tracking
- Attack Vector Analysis (Coming Soon)

## Development Status

Currently in Phase 1:
- Basic UI implementation
- Dummy data integration
- RAG status calculation

Next steps:
- Map visualization
- Real-time data integration
- AI-driven attack vector analysis

## Features:
- **IoT Device Mapping**: Visualize IoT devices with their vulnerability scores.
- **RAG Status**: Devices are color-coded based on vulnerability score (Red, Amber, Green).
- **AI Attack Vector Advisor**: Recommends attack strategies based on device vulnerabilities.
- **Ship Arrival Simulation**: Simulate the addition of new IoT devices when ships arrive.

## Technology Stack:
- **Backend**: Python
- **Frontend**: Streamlit
- **Data**: Static JSON files for initial demonstration
- **AI**: OpenAI API (optional for attack vector analysis)

## Setup Instructions:
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
