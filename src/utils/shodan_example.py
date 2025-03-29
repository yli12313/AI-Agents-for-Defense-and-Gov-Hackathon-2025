#!/usr/bin/env python
"""
Example script demonstrating the use of the Shodan client and parser modules.
This script can be used to:
1. Load an existing Shodan text response from a file
2. Parse and convert it to structured JSON
3. Perform basic analysis on the data
4. Optionally query the Shodan API directly
"""

import os
import sys
import logging
import argparse
from datetime import datetime
import json

from src.utils.shodan_client import ShodanClient
from src.utils.shodan_parser import ShodanResponseParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def load_and_parse_example(input_file: str, output_file: str = None):
    """
    Example function demonstrating how to load and parse a Shodan text response file.
    
    Args:
        input_file: Path to the Shodan text response file
        output_file: Optional path to save the parsed JSON output
    """
    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
        return
        
    # Determine output file path if not provided
    if not output_file:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.json"
    
    logger.info(f"Parsing Shodan text response from {input_file}")
    
    # Parse the text file
    try:
        start_time = datetime.now()
        parsed_data = ShodanResponseParser.parse_text_file(input_file, output_file)
        duration = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"Successfully parsed {parsed_data['total']} hosts in {duration:.2f} seconds")
        
        # Generate and print a summary
        summary = ShodanResponseParser.generate_summary(parsed_data)
        logger.info("Summary of parsed data:")
        for key, value in summary.items():
            if isinstance(value, list) and len(value) > 5:
                logger.info(f"  {key}: {len(value)} items including {', '.join(value[:5])}...")
            else:
                logger.info(f"  {key}: {value}")
        
        # Extract ports and services
        port_services = ShodanResponseParser.extract_ports_services(parsed_data)
        logger.info(f"Found {len(port_services)} unique ports")
        for port, services in sorted(port_services.items())[:10]:  # Show top 10 ports
            logger.info(f"  Port {port}: {', '.join(services[:3])}" + 
                      (f" and {len(services)-3} more" if len(services) > 3 else ""))
        
        # Extract vulnerabilities
        vulns = ShodanResponseParser.extract_vulnerabilities(parsed_data)
        if vulns:
            logger.info(f"Found {len(vulns)} potential vulnerabilities")
            
        return parsed_data
            
    except Exception as e:
        logger.error(f"Error processing Shodan response: {e}", exc_info=True)
        return None

def api_query_example(api_key: str, query: str, limit: int = 100):
    """
    Example function demonstrating how to query the Shodan API directly.
    
    Args:
        api_key: Shodan API key
        query: The search query to execute
        limit: Maximum number of results to return
    """
    if not api_key:
        logger.error("No API key provided. Please provide a Shodan API key.")
        return
        
    client = ShodanClient(api_key)
    logger.info(f"Executing Shodan search query: '{query}'")
    
    try:
        results = client.search(query, limit)
        logger.info(f"Received {len(results.get('matches', []))} results")
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"shodan_query_{timestamp}.json"
        filepath = os.path.join("src", "data", "shodan", "samples", filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
            
        logger.info(f"Saved query results to {filepath}")
        return results
        
    except Exception as e:
        logger.error(f"Error querying Shodan API: {e}", exc_info=True)
        return None

def main():
    """Parse command-line arguments and run the example functions."""
    parser = argparse.ArgumentParser(
        description="Shodan API and parser example script"
    )
    parser.add_argument(
        "--input-file",
        help="Path to an existing Shodan text response file to parse"
    )
    parser.add_argument(
        "--output-file",
        help="Path to save the parsed JSON output"
    )
    parser.add_argument(
        "--api-key",
        help="Shodan API key for direct queries (if not provided, will check SHODAN_API_KEY env var)"
    )
    parser.add_argument(
        "--query",
        help="Shodan search query to execute if using API"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of results to return for API queries (default: 100)"
    )
    
    args = parser.parse_args()
    
    # If an input file is provided, parse it
    if args.input_file:
        load_and_parse_example(args.input_file, args.output_file)
    
    # If API key and query are provided, execute a Shodan API query
    api_key = args.api_key or os.environ.get("SHODAN_API_KEY")
    if api_key and args.query:
        api_query_example(api_key, args.query, args.limit)
    
    # If no commands were executed, print help
    if not args.input_file and not (api_key and args.query):
        parser.print_help()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main()) 