# UML Diagram - Maritime Port Digital Twin

## Class Diagram:
- **IoT Device**:
   - **Attributes**:
     - `name`: String
     - `device_type`: String
     - `location`: List (float)
     - `vuln_score`: Float
     - `status`: String (Red, Amber, Green)
     - `cves`: List (String)
   - **Methods**:
     - `calculate_rag_status()`: Calculates the RAG status based on the `vuln_score`.
     - `generate_attack_vector()`: Suggests an attack vector based on device vulnerability.
   
- **Port Map**:
   - **Attributes**:
     - `map_image`: String (file path to port image)
     - `devices`: List of IoT Devices
   - **Methods**:
     - `render_map()`: Displays the map with devices overlaid.

- **Attack Vector Advisor**:
   - **Attributes**:
     - `attack_strategies`: List of potential attack vectors
   - **Methods**:
     - `generate_attack_vector(device)`: Generates a specific attack vector for the provided device.
   
## Use Case Diagram:
- **User**: Interacts with the app to visualize IoT devices, view attack vectors, and simulate ship arrivals.
- **Admin**: Provides attack vector analysis, reviews high-vulnerability devices, and controls port security.
- **AI Module**: Suggests attack vectors and potentially identifies interdependencies among devices for attack strategies.

### Data Flow:
1. **Port Map** receives the IoT device list and calculates RAG status.
2. **User** interacts with the map to view IoT devices and their vulnerabilities.
3. **Attack Vector Advisor** uses AI to suggest possible attack vectors based on the device data.

## Diagram Example:
