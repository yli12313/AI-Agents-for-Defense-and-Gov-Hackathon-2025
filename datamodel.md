# Data Model - Maritime Port Digital Twin

## IoT Device:
- **name** (string): Name of the device (e.g., "Crane_1").
- **device_type** (string): Type of device (e.g., "PLC", "Camera").
- **location** (array): Coordinates for device location on the port map (e.g., [0.3, 0.6]).
- **vuln_score** (float): Vulnerability score based on CVEs (e.g., 8.2).
- **status** (string): RAG status ("RED", "AMBER", "GREEN").
- **cves** (array): List of CVEs associated with the device.

## Ship Arrival Data (Optional):
- **name** (string): Name of the ship.
- **devices** (array): List of devices onboard the ship.

## Example:
```json
{
  "name": "Crane_1",
  "device_type": "PLC",
  "location": [0.3, 0.6],
  "vuln_score": 8.2,
  "cves": ["CVE-2022-1234", "CVE-2023-5678"]
}
