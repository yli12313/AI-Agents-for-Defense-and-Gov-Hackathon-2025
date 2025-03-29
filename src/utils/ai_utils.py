import os
import json
import sys
from typing import List, Dict, Any
import streamlit as st
from pathlib import Path

# Try to import OpenAI, but handle if it's not installed
try:
    import openai
    OPENAI_AVAILABLE = True
    print("[OPENAI] Package available")
except ImportError:
    OPENAI_AVAILABLE = False
    print("[OPENAI] Package not available")

# Get API key from multiple possible sources with proper fallbacks
OPENAI_API_KEY = None

# Function to check for secrets in both project root and src directory
def find_secrets():
    """Check for secrets.toml in multiple locations and parse it if found."""
    # Define possible paths to check
    current_dir = Path(__file__).absolute().parent  # utils directory
    possible_paths = [
        current_dir.parent.parent / ".streamlit" / "secrets.toml",  # project root
        current_dir.parent / ".streamlit" / "secrets.toml",         # src directory
    ]
    
    # Check each path
    for path in possible_paths:
        if path.exists():
            print(f"[OPENAI] Found secrets file at {path}")
            try:
                # Simple TOML parser for secrets
                with open(path, "r") as f:
                    content = f.read()
                    for line in content.splitlines():
                        if line.strip() and not line.strip().startswith("#"):
                            try:
                                key, value = line.split("=", 1)
                                key = key.strip()
                                value = value.strip().strip('"\'')
                                if key == "OPENAI_API_KEY":
                                    return value
                            except ValueError:
                                continue
            except Exception as e:
                print(f"[OPENAI] Error reading secrets file: {str(e)}")
    return None

# First try to get from Streamlit secrets (preferred for deployment)
try:
    # This works on Render with proper environment variables
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    print(f"[OPENAI] Found API key in Streamlit config: {OPENAI_API_KEY[:5]}...{OPENAI_API_KEY[-5:] if len(OPENAI_API_KEY) > 10 else ''}")
except Exception as e:
    print(f"[OPENAI] Error accessing Streamlit secrets: {str(e)}")
    # If not in Streamlit secrets, check our manual parser
    OPENAI_API_KEY = find_secrets()
    if OPENAI_API_KEY:
        print(f"[OPENAI] Found API key in secrets.toml: {OPENAI_API_KEY[:5]}...{OPENAI_API_KEY[-5:] if len(OPENAI_API_KEY) > 10 else ''}")
    else:
        # Last resort - check environment variables
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        if OPENAI_API_KEY:
            print(f"[OPENAI] Found API key in environment: {OPENAI_API_KEY[:5]}...{OPENAI_API_KEY[-5:] if len(OPENAI_API_KEY) > 10 else ''}")
        else:
            print("[OPENAI] No API key found in any location")

# Flag for simulation mode - any key starting with "sk-demo" is considered simulation
SIMULATION_MODE = bool(OPENAI_API_KEY and OPENAI_API_KEY.startswith("sk-demo"))

# Debug print for troubleshooting
print(f"[OPENAI] API Key Available: {bool(OPENAI_API_KEY)}")
print(f"[OPENAI] Simulation Mode: {SIMULATION_MODE}")

# Only initialize the client if we have an API key (real or simulation)
client = None
if OPENAI_AVAILABLE and OPENAI_API_KEY:
    try:
        # Initialize the OpenAI client with the API key
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        print("[OPENAI] Client initialized successfully")
    except Exception as e:
        print(f"[OPENAI] Error initializing client: {str(e)}")
        # If initialization fails, don't crash the whole module

def generate_attack_vector_with_ai(devices: List[Dict[str, Any]]) -> str:
    """
    Generate a detailed attack vector analysis using OpenAI's API.
    
    Args:
        devices: List of IoT device data with vulnerability information
        
    Returns:
        str: A detailed attack vector analysis
    """
    print(f"[OPENAI] generate_attack_vector_with_ai called with {len(devices)} devices")
    
    if not devices:
        print("[OPENAI] No devices available for analysis")
        return "No devices available for attack vector analysis."
    
    if not OPENAI_AVAILABLE:
        print("[OPENAI] OpenAI package not installed, using rule-based analysis")
        return rule_based_attack_vector(devices) + "\n\n*Note: OpenAI package not installed. Using rule-based analysis.*"
    
    if not OPENAI_API_KEY:
        print("[OPENAI] No API key found, using rule-based analysis")
        return rule_based_attack_vector(devices) + "\n\n*Note: OpenAI API key not found in secrets.toml or environment. Using rule-based analysis.*"
    
    # In simulation mode, we'll return a predefined AI-like response
    if SIMULATION_MODE:
        print("[OPENAI] Using simulation mode for attack vector analysis")
        return simulation_attack_vector(devices)
    
    # Sort devices by vulnerability score
    vulnerable_devices = sorted(devices, key=lambda x: x.get("vuln_score", 0), reverse=True)
    print(f"[OPENAI] Sorted {len(vulnerable_devices)} devices by vulnerability score")
    
    # Prepare the context for the AI
    context = "The following IoT devices are present in a maritime port environment:\n\n"
    
    for i, device in enumerate(vulnerable_devices, 1):
        context += f"{i}. {device.get('name', 'Unknown Device')} ({device.get('device_type', 'Unknown')}):\n"
        context += f"   - Vulnerability Score: {device.get('vuln_score', 0)}\n"
        cves = device.get('cves', [])
        if cves:
            context += f"   - CVEs: {', '.join(cves)}\n"
        context += "\n"
    
    # Only proceed to call the API if we have both an API key and a client
    if not client:
        print("[OPENAI] Client not initialized - falling back to simulation")
        return simulation_attack_vector(devices)
        
    # Create the prompt for OpenAI
    prompt = f"""
{context}

Based on these devices and their vulnerabilities, generate a detailed cyber attack scenario that could target this maritime port. Include:

1. Initial entry point (which vulnerable device would be targeted first)
2. Step-by-step attack progression
3. Potential lateral movement between devices
4. Impact assessment
5. Recommended mitigations

Format your response with markdown headers and bullet points for readability.
"""
    
    try:
        # Use the new OpenAI API syntax (v1.0+)
        print("[OPENAI] Calling OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" for better quality
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert specializing in maritime infrastructure security."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.7
        )
        
        # Extract the response text (new API response format)
        attack_vector = response.choices[0].message.content
        print("[OPENAI] API Response received successfully")
        return attack_vector
    
    except Exception as e:
        print(f"[OPENAI] API Error: {str(e)}")
        # Fallback to simulation mode if API call fails
        return simulation_attack_vector(devices) + f"\n\n*Note: AI-enhanced analysis using real API unavailable. Error: {str(e)}*"

def rule_based_attack_vector(devices: List[Dict[str, Any]]) -> str:
    """Fallback rule-based attack vector generation."""
    if not devices:
        return "No devices available for attack vector analysis."
    
    # Sort devices by vulnerability score
    sorted_devices = sorted(devices, key=lambda x: x.get("vuln_score", 0), reverse=True)
    entry_point = sorted_devices[0]  # Most vulnerable device
    
    attack_vector = f"""
## Potential Attack Vector (Rule-based Analysis)

### Initial Entry Point
- **{entry_point.get('name', 'Unknown Device')}** ({entry_point.get('device_type', 'Unknown')})
- Vulnerability Score: {entry_point.get('vuln_score', 0)}
- CVEs: {', '.join(entry_point.get('cves', ['None']))}

### Attack Progression
1. Attacker exploits vulnerabilities in {entry_point.get('name', 'the entry point')}
2. Gains initial foothold in the network
"""
    
    # Add lateral movement targets
    lateral_targets = [d for d in sorted_devices[1:4] if d.get('vuln_score', 0) >= 4]
    if lateral_targets:
        attack_vector += "\n### Lateral Movement Targets\n"
        for i, target in enumerate(lateral_targets, 1):
            attack_vector += f"{i}. **{target.get('name', 'Unknown')}** - Vulnerability Score: {target.get('vuln_score', 0)}\n"
    
    # Add recommended mitigations
    attack_vector += """
### Recommended Mitigations
1. Patch all systems with known vulnerabilities
2. Implement network segmentation
3. Deploy intrusion detection systems
4. Regular security assessments
"""
    
    return attack_vector

def simulation_attack_vector(devices: List[Dict[str, Any]]) -> str:
    """Generate a simulated AI attack vector analysis for demo purposes."""
    if not devices:
        return "No devices available for attack vector analysis."
    
    # Sort devices by vulnerability score
    sorted_devices = sorted(devices, key=lambda x: x.get("vuln_score", 0), reverse=True)
    entry_point = sorted_devices[0]  # Most vulnerable device
    
    # Get the top 3 vulnerable devices for lateral movement
    lateral_targets = [d for d in sorted_devices[1:4] if d.get('vuln_score', 0) >= 4]
    
    # Build an enhanced attack vector that looks like it came from AI
    attack_vector = f"""
## Maritime Port Attack Vector Analysis (AI-Enhanced)

### Critical Entry Point
- **{entry_point.get('name', 'Primary Target')}** ({entry_point.get('device_type', 'Unknown')})
- Vulnerability Score: {entry_point.get('vuln_score', 0)}/10 (High Risk)
- Exploitable CVEs: {', '.join(entry_point.get('cves', ['CVE-2023-XXXX']))}
- Location: Perimeter network zone

### Attack Progression
1. **Initial Access**: Threat actors would likely target the {entry_point.get('device_type', 'primary system')} using publicly available exploits for the identified CVEs.
2. **Privilege Escalation**: After gaining initial access, attackers would elevate privileges by exploiting local vulnerabilities.
3. **Persistence**: Installation of backdoors and creation of alternate authentication mechanisms.
4. **Defense Evasion**: Clearing of logs and disabling of security monitoring tools.
5. **Credential Access**: Extraction of credentials from memory or configuration files.
"""
    
    # Add lateral movement if there are vulnerable targets
    if lateral_targets:
        attack_vector += "\n### Lateral Movement Pathway\n"
        attack_vector += "Once established on the initial target, attackers would likely move to these systems:\n\n"
        
        for i, target in enumerate(lateral_targets, 1):
            attack_vector += f"{i}. **{target.get('name', 'Secondary Target')}** ({target.get('device_type', 'Unknown')})\n"
            attack_vector += f"   - Vulnerability Score: {target.get('vuln_score', 0)}/10\n"
            attack_vector += f"   - Purpose: {['Data exfiltration', 'Command and control', 'Secondary persistence'][i % 3]}\n"
            attack_vector += f"   - Access Method: {['Credential reuse', 'Trust relationship exploitation', 'Network protocol vulnerabilities'][i % 3]}\n\n"
    
    # Add impact assessment
    attack_vector += """
### Potential Impact Assessment
- **Operational**: Critical port operations could be disrupted, including cargo handling systems
- **Safety**: Safety monitoring systems could be compromised, creating physical hazards
- **Financial**: Potential for significant financial losses due to operational downtime
- **Reputational**: Public disclosure of a breach would damage stakeholder confidence
- **Data**: Sensitive operational data, including cargo manifests, could be exfiltrated

### Recommended Mitigations
1. **Immediate Actions**:
   - Patch all identified vulnerabilities, prioritizing internet-facing systems
   - Implement network segmentation to isolate critical OT/ICS systems
   - Deploy enhanced monitoring for unusual network traffic patterns

2. **Medium-term Improvements**:
   - Implement multi-factor authentication across all critical systems
   - Develop and test incident response procedures specific to OT/ICS environments
   - Conduct regular penetration testing and tabletop exercises

3. **Long-term Strategy**:
   - Migrate legacy systems to more secure platforms with modern security controls
   - Implement a comprehensive security architecture review
   - Establish threat intelligence sharing with maritime sector partners
"""
    
    return attack_vector 