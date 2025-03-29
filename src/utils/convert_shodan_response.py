#!/usr/bin/env python
"""
Command-line utility for converting a Shodan text response file to JSON format.
Usage: python convert_shodan_response.py <input_file> [<output_file>]

If <output_file> is not specified, it will use the same name as the input file but with .json extension.
"""

import sys
import os
import logging
import argparse
import json
from datetime import datetime
from shodan_parser import ShodanResponseParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Parse command-line arguments and convert the Shodan text file to JSON."""
    parser = argparse.ArgumentParser(
        description="Convert Shodan text response to JSON format"
    )
    parser.add_argument(
        "input_file", 
        help="Path to the Shodan text response file"
    )
    parser.add_argument(
        "-o", "--output-file", 
        help="Path to save the parsed JSON output (default: input_file with .json extension)"
    )
    parser.add_argument(
        "-s", "--summarize", 
        action="store_true",
        help="Generate and print a summary of the parsed data"
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input_file):
        logger.error(f"Input file not found: {args.input_file}")
        return 1
        
    # Determine output file path
    output_file = args.output_file
    if not output_file:
        base_name = os.path.splitext(args.input_file)[0]
        output_file = f"{base_name}.json"
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    logger.info(f"Converting Shodan text response from {args.input_file} to {output_file}")
    
    try:
        # Parse the text file
        start_time = datetime.now()
        parsed_data = ShodanResponseParser.parse_text_file(
            args.input_file, 
            output_file
        )
        duration = (datetime.now() - start_time).total_seconds()
        
        # Add metadata
        parsed_data["metadata"]["parsed_timestamp"] = datetime.now().isoformat()
        parsed_data["metadata"]["processing_time_seconds"] = duration
        
        # Save the updated data
        with open(output_file, 'w') as f:
            json.dump(parsed_data, f, indent=2)
        
        logger.info(f"Successfully parsed and saved to {output_file}")
        logger.info(f"Processed {parsed_data['total']} hosts in {duration:.2f} seconds")
        
        # Print summary if requested
        if args.summarize:
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
        
        return 0
        
    except Exception as e:
        logger.error(f"Error processing Shodan response: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 