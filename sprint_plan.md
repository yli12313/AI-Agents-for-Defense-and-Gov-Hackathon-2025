---

### **Sprint_Plan.md**

```markdown
# Sprint Plan - Maritime Port Digital Twin (Phase 1)

## Sprint Goal:
- Build the foundational user interface and integrate dummy IoT device data.
- Focus on visualizing devices and displaying RAG (Red-Amber-Green) vulnerability statuses.
- Enable attack vector analysis with a basic AI recommendation.

## Timebox:
**Duration**: 2 hours  
**Team Members**:  
- **Y**: Frontend focus (Streamlit components, UI design).  
- **S**: Assist Y with frontend tasks.  
- **K (User)**: Backend focus (Load and process dummy IoT data, integrate backend logic for attack vector analysis).

### Tasks Breakdown:

1. **Frontend UI (Y & S)**:
   - Set up Streamlit and display the port map image.
   - Overlay dummy IoT devices on the map with RAG status (Red, Amber, Green).
   - Display device information like name, type, vulnerability score, and CVEs.

2. **Backend (K)**:
   - Prepare dummy IoT device data (e.g., `data.json` with device names, types, vulnerability scores, etc.).
   - Implement logic for calculating RAG statuses based on device vulnerability scores.
   - Create a simple attack vector generator (e.g., analyze the highest-scoring device as an entry point).

3. **AI Attack Vector Advisor**:
   - Add a button to trigger the attack vector analysis.
   - Display AI-generated or rule-based attack strategies based on device vulnerabilities.

### Deliverables:
- Streamlit app running locally with dummy data and RAG status visualization.
- Functional attack vector analysis button with basic logic.

## Next Steps (Phase 1.1):
- Once Phase 1 is complete, we will prepare to integrate the Shodan API for real-time device data.
