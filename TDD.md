# Test-Driven Development Plan - Maritime Port Digital Twin

## Objective:
Implement tests to validate the functionality of IoT device handling, RAG score calculation, and attack vector analysis.

### Tests:

1. **Test IoT Device Data Loading**:
   - **Test**: Ensure that the `data.json` file is loaded correctly.
   - **Expected Outcome**: The system should correctly load a list of devices with attributes (name, type, location, vuln_score, cves).

2. **Test RAG Score Calculation**:
   - **Test**: Validate that the RAG status is calculated correctly based on the `vuln_score`.
   - **Expected Outcome**: Devices with vuln_score >= 7 should return "RED", >=4 should return "AMBER", else "GREEN".

3. **Test Attack Vector Generation**:
   - **Test**: Ensure that the attack vector generation logic prioritizes the highest-vulnerability devices.
   - **Expected Outcome**: The system should suggest the highest scoring device as the entry point, and display potential attack paths.

### Testing Framework:
- **pytest** or **unittest** can be used to run the tests locally.
- Tests should be added under the `/tests` directory.

## Future Tests:
- Test integration with the Shodan API (Phase 1.2).
- Test dynamic addition of new ship devices.
