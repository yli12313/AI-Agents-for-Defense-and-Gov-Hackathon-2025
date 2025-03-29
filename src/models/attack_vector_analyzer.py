from typing import List, Dict, Any
import json
import os
from pathlib import Path
import random
import sys
import os

# Add the project root to the Python path to fix imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Use absolute import
from src.utils.ai_utils import generate_attack_vector_with_ai, rule_based_attack_vector, OPENAI_AVAILABLE

class AttackVectorAnalyzer:
    """
    A class to analyze potential attack vectors based on IoT device vulnerabilities.
    """
    
    def __init__(self, devices: List[Dict[str, Any]] = None):
        """
        Initialize the attack vector analyzer.
        
        Args:
            devices: List of IoT devices with vulnerability information
        """
        self.devices = devices or []
        print(f"[ANALYZER] Initialized with {len(self.devices)} devices")
        
    def set_devices(self, devices: List[Dict[str, Any]]):
        """Set the devices to analyze."""
        self.devices = devices
        print(f"[ANALYZER] Updated devices, now has {len(self.devices)} devices")
        
    def analyze(self, use_ai: bool = True) -> Dict[str, Any]:
        """
        Analyze potential attack vectors.
        
        Args:
            use_ai: Whether to use AI for analysis or fallback to rule-based
            
        Returns:
            Dict containing analysis results
        """
        print(f"[ANALYZER] Starting analysis with use_ai={use_ai}, OPENAI_AVAILABLE={OPENAI_AVAILABLE}")
        
        if not self.devices:
            print("[ANALYZER] No devices available for analysis")
            return {
                "success": False,
                "error": "No devices available for analysis",
                "attack_vector": "No devices available for attack vector analysis."
            }
        
        try:
            # In simulation mode, we'll use the use_ai flag directly without checking the API key
            if use_ai and OPENAI_AVAILABLE:
                # Use AI-powered analysis
                print("[ANALYZER] Using AI-powered analysis")
                attack_vector = generate_attack_vector_with_ai(self.devices)
            else:
                # Use rule-based analysis as fallback
                print("[ANALYZER] Using rule-based analysis")
                attack_vector = rule_based_attack_vector(self.devices)
                
            # Calculate risk score based on device vulnerabilities
            avg_vuln_score = sum(d.get("vuln_score", 0) for d in self.devices) / len(self.devices)
            high_vuln_count = sum(1 for d in self.devices if d.get("vuln_score", 0) >= 7)
            
            risk_score = min(10, (avg_vuln_score * 0.7) + (high_vuln_count * 0.3 * 2))
            print(f"[ANALYZER] Analysis complete: risk_score={risk_score}, high_vuln_count={high_vuln_count}")
            
            return {
                "success": True,
                "attack_vector": attack_vector,
                "risk_score": round(risk_score, 1),
                "high_vuln_count": high_vuln_count,
                "avg_vuln_score": round(avg_vuln_score, 1)
            }
            
        except Exception as e:
            print(f"[ANALYZER] Error during analysis: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "attack_vector": f"Error generating attack vector: {str(e)}"
            }
    
    def save_analysis(self, analysis_result: Dict[str, Any], filename: str = "attack_analysis.json"):
        """Save analysis results to a file."""
        output_dir = Path("src/data/analysis")
        output_dir.mkdir(exist_ok=True, parents=True)
        
        output_path = output_dir / filename
        with open(output_path, "w") as f:
            json.dump(analysis_result, f, indent=2)
            
        print(f"[ANALYZER] Analysis saved to {output_path}")
        return output_path 