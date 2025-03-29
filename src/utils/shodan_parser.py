"""
Utility script for parsing and analyzing Shodan response data.
"""

import json
import os
import re
import logging
from typing import Dict, List, Any, Optional, Union, Tuple

logger = logging.getLogger(__name__)

class ShodanResponseParser:
    """Parser for Shodan response data, especially for converting text responses to structured data."""

    @staticmethod
    def parse_text_file(filepath: str, output_filepath: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse a Shodan text file response into structured data.
        
        Args:
            filepath: Path to the text file containing the Shodan response
            output_filepath: Optional path to save the parsed JSON result
            
        Returns:
            Dictionary containing the parsed data
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
            
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                
            # Basic structure for parsed data
            parsed_data = {
                "hosts": [],
                "total": 0,
                "metadata": {
                    "source_file": filepath,
                    "parsed_timestamp": None  # Will be set during parsing
                }
            }
            
            # Implement parsing logic based on the specific format of your Shodan response
            # This is a placeholder implementation that should be customized
            # based on the actual format of your 3MB text file
            
            # Example parsing logic - customize based on actual format
            host_blocks = re.split(r'\n\n+', content)
            
            for block in host_blocks:
                if not block.strip():
                    continue
                    
                host_data = {}
                lines = block.split('\n')
                
                # Basic parsing logic - customize based on actual format
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        host_data[key.strip()] = value.strip()
                
                if host_data:
                    parsed_data["hosts"].append(host_data)
            
            parsed_data["total"] = len(parsed_data["hosts"])
            
            # Save to JSON file if output path is provided
            if output_filepath:
                os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
                with open(output_filepath, 'w') as f:
                    json.dump(parsed_data, f, indent=2)
                logger.info(f"Saved parsed Shodan data to {output_filepath}")
                
            return parsed_data
            
        except Exception as e:
            logger.error(f"Error parsing Shodan text file: {e}")
            raise

    @staticmethod
    def extract_ports_services(parsed_data: Dict[str, Any]) -> Dict[int, List[str]]:
        """
        Extract unique ports and services from parsed Shodan data.
        
        Args:
            parsed_data: Previously parsed Shodan data
            
        Returns:
            Dictionary mapping ports to lists of services found on them
        """
        port_services = {}
        
        for host in parsed_data.get("hosts", []):
            port = host.get("Port")
            service = host.get("Service")
            
            if port and service:
                try:
                    port_num = int(port)
                    if port_num not in port_services:
                        port_services[port_num] = []
                    if service not in port_services[port_num]:
                        port_services[port_num].append(service)
                except ValueError:
                    pass
                    
        return port_services
        
    @staticmethod
    def extract_vulnerabilities(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract vulnerability information from parsed Shodan data.
        
        Args:
            parsed_data: Previously parsed Shodan data
            
        Returns:
            List of vulnerability information dictionaries
        """
        vulnerabilities = []
        
        for host in parsed_data.get("hosts", []):
            # This logic needs to be customized based on how vulnerabilities
            # are represented in your Shodan data
            if "CVE" in host or "Vulnerability" in host:
                vuln_info = {
                    "ip": host.get("IP", "Unknown"),
                    "port": host.get("Port"),
                    "service": host.get("Service"),
                    "cve": host.get("CVE"),
                    "description": host.get("Vulnerability")
                }
                vulnerabilities.append(vuln_info)
                
        return vulnerabilities
        
    @staticmethod
    def generate_summary(parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a summary of the Shodan data.
        
        Args:
            parsed_data: Previously parsed Shodan data
            
        Returns:
            Dictionary with summary information
        """
        hosts_count = len(parsed_data.get("hosts", []))
        unique_ips = set()
        countries = set()
        orgs = set()
        
        for host in parsed_data.get("hosts", []):
            if "IP" in host:
                unique_ips.add(host["IP"])
            if "Country" in host:
                countries.add(host["Country"])
            if "Organization" in host:
                orgs.add(host["Organization"])
                
        return {
            "total_hosts": hosts_count,
            "unique_ips": len(unique_ips),
            "countries": list(countries),
            "organizations": list(orgs)
        } 