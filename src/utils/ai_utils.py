import os
import json
import sys
from typing import List, Dict, Any

# Try to import OpenAI, but handle if it's not installed
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# This would normally come from environment variables
# For demo purposes, we'll use a placeholder
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
if OPENAI_AVAILABLE and OPENAI_API_KEY:
    # Initialize the OpenAI client with the API key
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_attack_vector_with_ai(devices: List[Dict[str, Any]]) -> str:
    """
    Generate a detailed attack vector analysis using OpenAI's API.
    
    Args:
        devices: List of IoT device data with vulnerability information
        
    Returns:
        str: A detailed attack vector analysis
    """
    if not devices:
        return "No devices available for attack vector analysis."
    
    if not OPENAI_AVAILABLE:
        return rule_based_attack_vector(devices) + "\n\n*Note: OpenAI package not installed. Using rule-based analysis.*"
    
    if not OPENAI_API_KEY:
        return rule_based_attack_vector(devices) + "\n\n*Note: OpenAI API key not provided. Using rule-based analysis.*"
    
    # Sort devices by vulnerability score
    vulnerable_devices = sorted(devices, key=lambda x: x.get("vuln_score", 0), reverse=True)
    
    # Prepare the context for the AI
    context = "The following IoT devices are present in a maritime port environment:\n\n"
    
    for i, device in enumerate(vulnerable_devices, 1):
        context += f"{i}. {device.get('name', 'Unknown Device')} ({device.get('device_type', 'Unknown')}):\n"
        context += f"   - Vulnerability Score: {device.get('vuln_score', 0)}\n"
        cves = device.get('cves', [])
        if cves:
            context += f"   - CVEs: {', '.join(cves)}\n"
        context += "\n"
    
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
        return attack_vector
    
    except Exception as e:
        # Fallback to rule-based approach if API call fails
        return rule_based_attack_vector(vulnerable_devices) + f"\n\n*Note: AI-enhanced analysis unavailable. Error: {str(e)}*"

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