"""
Shodan API client module for querying and processing Shodan data.
"""

import os
import json
import requests
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class ShodanClient:
    """Client for interacting with the Shodan API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Shodan client.
        
        Args:
            api_key: Shodan API key. If not provided, will look for SHODAN_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("SHODAN_API_KEY")
        if not self.api_key:
            logger.warning("No Shodan API key provided. API requests will not work.")
        self.base_url = "https://api.shodan.io"
    
    def search(self, query: str, limit: int = 100) -> Dict[str, Any]:
        """
        Search Shodan for the given query.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
            
        Returns:
            Dictionary containing search results
        """
        if not self.api_key:
            raise ValueError("API key required for Shodan searches")
            
        url = f"{self.base_url}/shodan/host/search"
        params = {
            "key": self.api_key,
            "query": query,
            "limit": limit
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching Shodan: {e}")
            raise
    
    def host_info(self, ip: str) -> Dict[str, Any]:
        """
        Get information about a specific IP address.
        
        Args:
            ip: The IP address to lookup
            
        Returns:
            Dictionary containing host information
        """
        if not self.api_key:
            raise ValueError("API key required for Shodan host lookups")
            
        url = f"{self.base_url}/shodan/host/{ip}"
        params = {"key": self.api_key}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting host info from Shodan: {e}")
            raise
    
    def save_response_to_file(self, data: Dict[str, Any], filename: str) -> str:
        """
        Save Shodan response data to a file.
        
        Args:
            data: The response data to save
            filename: Name of the file to save to (without path)
            
        Returns:
            Full path to the saved file
        """
        os.makedirs("src/data/shodan/samples", exist_ok=True)
        filepath = f"src/data/shodan/samples/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Saved Shodan response to {filepath}")
        return filepath
    
    def load_response_from_file(self, filename: str) -> Dict[str, Any]:
        """
        Load Shodan response data from a file.
        
        Args:
            filename: Name of the file to load (without path)
            
        Returns:
            Dictionary containing the loaded data
        """
        filepath = f"src/data/shodan/samples/{filename}"
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return data
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Error loading Shodan response from {filepath}: {e}")
            raise

    @staticmethod
    def parse_text_response(filepath: str) -> Dict[str, Any]:
        """
        Parse a text-based Shodan response file into a structured format.
        
        Args:
            filepath: Path to the text file containing Shodan response
            
        Returns:
            Dictionary containing the parsed data
        """
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                
            # Simple parsing logic - would need to be adapted based on
            # the actual format of your text file
            # This is a placeholder for the actual parsing logic
            parsed_data = {"raw_content": content[:1000]}  # First 1000 chars as preview
            
            # TODO: Implement actual parsing logic based on the format of your Shodan response
            
            return parsed_data
        except FileNotFoundError as e:
            logger.error(f"Error loading Shodan text response from {filepath}: {e}")
            raise 