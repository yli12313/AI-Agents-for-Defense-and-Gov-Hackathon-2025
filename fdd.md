# Feature-Driven Development - Maritime Port Digital Twin

## Feature 1: IoT Device Mapping
- **Description**: Display a map of the port with IoT devices overlaid.
- **Acceptance Criteria**:
  - IoT devices are shown on the port map with their names, types, and location.
  - Devices are color-coded based on RAG status.

## Feature 2: RAG Status Calculation
- **Description**: Assign a Red, Amber, or Green status to each device based on its vulnerability score.
- **Acceptance Criteria**:
  - Devices with a `vuln_score >= 7` are marked as "RED".
  - Devices with a `vuln_score >= 4` are marked as "AMBER".
  - Devices with a `vuln_score < 4` are marked as "GREEN".

## Feature 3: Attack Vector Analysis
- **Description**: Generate an AI-based or rule-based attack vector analysis.
- **Acceptance Criteria**:
  - Display the most vulnerable device as the entry point.
  - Provide a simple attack strategy involving lateral movement.

## Feature 4: Ship Arrival Simulation (Optional)
- **Description**: Simulate the addition of new devices when ships arrive.
- **Acceptance Criteria**:
  - Button to add new devices from `ship_data.json`.
  - Recalculate RAG statuses and attack vectors after devices are added.

## Future Features:
- Integration with Shodan API for real-time data.
- More advanced attack vector analysis.
