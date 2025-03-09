#!/usr/bin/env python3
import argparse
import requests
import json
import os
import sys
from pathlib import Path

def upload_log_file(file_path, n8n_webhook_url):
    """
    Upload a log file to the n8n webhook for analysis
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found")
        return False
    
    try:
        # Read the log file
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            log_content = file.read()
        
        print(f"File size: {len(log_content)} bytes")
        print(f"First 100 characters: {log_content[:100]}")
        
        # Send to n8n webhook
        print(f"Sending to webhook: {n8n_webhook_url}")
        
        response = requests.post(
            n8n_webhook_url,
            data=log_content,
            headers={
                'Content-Type': 'text/plain',
                'Content-Length': str(len(log_content))
            }
        )
        
        # Check if successful
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                # Parse JSON response, handling both object and array formats
                result_json = response.json()
                
                # Handle array response (convert to object by taking first item)
                if isinstance(result_json, list) and len(result_json) > 0:
                    result = result_json[0]
                else:
                    result = result_json
                
                # Print response for debugging
                print(f"Response type: {type(result)}")
                
                # Print summary
                print("\n=== Log Analysis Summary ===")
                summary = result.get('summary', {})
                if not isinstance(summary, dict):
                    print(f"Unexpected summary format: {type(summary)}")
                    print(f"Full response: {result}")
                    return False
                    
                print(f"Total logs analyzed: {summary.get('totalLogs', 0)}")
                print(f"Abnormal events detected: {summary.get('abnormalEvents', 0)}")
                print(f"MITRE ATT&CK findings: {summary.get('mitreFindings', 0)}")
                print(f"Error count: {summary.get('errorCount', 0)}")
                print(f"Warning count: {summary.get('warningCount', 0)}")
                
                # Save HTML report
                output_file = Path(file_path).stem + "_analysis.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result.get('reportHtml', ''))
                print(f"\nDetailed HTML report saved to: {output_file}")
                
                # Print text report
                print("\n=== Analysis Report ===")
                print(result.get('reportText', 'No text report available'))
                
                return True
            except json.JSONDecodeError:
                print("Error: Response was not valid JSON")
                print(f"Response content: {response.text[:200]}...")
                return False
            except Exception as e:
                print(f"Error processing response: {str(e)}")
                print(f"Response: {response.text[:500]}")
                return False
        else:
            print(f"Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error uploading log file: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload a log file for AI analysis with MITRE ATT&CK mapping')
    parser.add_argument('log_file', help='Path to the log file to analyze')
    parser.add_argument('--webhook', required=True, help='URL of the n8n webhook')
    
    args = parser.parse_args()
    upload_log_file(args.log_file, args.webhook)
