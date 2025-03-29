# Port Security Intelligence Platform

A comprehensive platform that combines port city vulnerability scanning with maritime port digital twin visualization to provide security insights for port infrastructure.

## Project Overview

This application integrates two powerful tools:

1. **Port City Vulnerability Scanner**: For identifying and analyzing potentially vulnerable Industrial Control Systems (ICS) and SCADA devices in port cities worldwide using Shodan data.

2. **Maritime Port Digital Twin Dashboard**: A digital twin visualization of port IoT devices with vulnerability assessment and attack vector analysis.

## Key Features

### Port City Vulnerability Scanner
- Geographic search of port cities by name
- Conversion of city names to geographic coordinates
- Generation of Shodan-compatible search queries
- Security analysis of discovered devices
- Risk scoring based on multiple weighted factors
- Mitigation recommendations for identified vulnerabilities
- Interactive data visualization

### Maritime Port Digital Twin
- IoT Device Visualization on satellite imagery
- RAG (Red-Amber-Green) Status System for devices
- Device vulnerability tracking
- AI-powered attack vector analysis
- Ship arrival simulation
- Integrated risk assessment

## Technical Details

This application is built with:

- Python 3.8+
- Streamlit for the web interface
- Pandas for data processing
- Folium for interactive maps
- OpenAI API for AI-enhanced analysis (optional)
- Shodan API for real-world data (simulation mode available)

## Project Structure

```
src/
├── app.py                      # Original Port Scanner application
├── integrated_app.py           # Integrated platform with both tools
├── query_generator.py          # City lookup and query generation
├── vulnerability_analyzer.py   # Security analysis and recommendations
├── models/
│   └── attack_vector_analyzer.py # AI-enhanced attack vector analysis
├── data/
│   ├── dummy_data.json         # Sample IoT device data
│   └── shodan/
│       └── samples/            # Sample Shodan data
│           └── clean_sample.json
├── utils/
│   ├── shodan_parser.py        # Shodan API response parser
│   ├── convert_shodan_response.py  # Utility for converting raw responses
│   └── ai_utils.py             # OpenAI integration utilities
```

## Getting Started

### Prerequisites

- Python 3.8+
- Streamlit
- Pandas
- Folium
- OpenAI API key (optional, for AI-enhanced analysis)

### Installation

1. Clone the repository:
```
git clone <repository-url>
cd port-security-platform
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

### Running the Application

To run the integrated application in simulation mode (no API keys required):

```
cd src
streamlit run integrated_app.py
```

The application will be available at `http://localhost:8501`

### Using with Real Data

To use the application with real data:

1. Obtain a Shodan API key from https://account.shodan.io/
2. (Optional) Obtain an OpenAI API key for enhanced attack vector analysis
3. Set the API keys as environment variables:
```
export SHODAN_API_KEY=your_shodan_api_key
export OPENAI_API_KEY=your_openai_api_key
```

## Usage

1. Start on the Port Scanner page
2. Enter a port city name, search term, and radius
3. View the vulnerability analysis of discovered systems
4. Navigate to the Digital Twin Dashboard to visualize port IoT devices
5. Generate attack vector analysis to understand potential threats
6. Use the navigation sidebar to switch between tools

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Shodan for providing the API for ICS/SCADA discovery
- OpenAI for the AI capabilities
- The Streamlit team for their excellent data application framework

# Maritime Port Digital Twin Dashboard

A comprehensive dashboard for maritime port security monitoring, vulnerability assessment, and digital twin visualization.

## Features

- Port City Vulnerability Scanner: Search for potentially vulnerable systems in port cities
- Digital Twin Dashboard: Visualize IoT devices and their security status
- AI-Enhanced Attack Vector Analysis: Get detailed attack path and impact assessments
- Security Recommendations: Receive specific mitigation strategies

## Setup

### Prerequisites

- Python 3.8+
- Streamlit (`pip install streamlit`)
- OpenAI API key (optional, for enhanced AI analysis)
- Shodan API key (for production deployment)

### API Keys Setup

This application supports multiple ways to configure API keys:

#### For Local Development

1. Create a `.streamlit/secrets.toml` file in the project root:

```toml
OPENAI_API_KEY = "your-api-key-here"
SHODAN_API_KEY = "your-shodan-api-key-here"
```

2. The application will automatically detect this file and use the keys.

#### For Deployment on Render

When deploying to Render:

1. Fork this repository to your GitHub account
2. Go to [Render.com](https://render.com) and create an account if you don't have one
3. Click "New" and select "Blueprint" from the dropdown menu
4. Connect your GitHub account and select the forked repository
5. Add your API keys as environment variables in the Render dashboard:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `SHODAN_API_KEY`: Your Shodan API key

Render will automatically deploy your application using the `render.yaml` configuration file.

### Running the Application

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `cd src && streamlit run integrated_app.py`

## Development

This project maintains a clean separation between simulation and production modes:

- Any OpenAI key starting with "sk-demo" will trigger simulation mode
- Without valid API keys, the app falls back to rule-based analysis
- API keys are properly protected using `.gitignore` rules

### Git Security

The repository has been configured to prevent accidental commits of API keys:

- Both `.streamlit/secrets.toml` and `src/.streamlit/secrets.toml` are in `.gitignore`
- Never hardcode API keys directly in the source code

## Contributing

1. Create feature branches from `main`
2. Ensure API keys are never committed to the repository
3. Run tests before submitting pull requests
4. Update documentation as needed
