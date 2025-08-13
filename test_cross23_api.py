#!/usr/bin/env python3
import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append('.')

from utils.rapidapi import RapidAPICall

def test_cross23_api_calls():
    print("Testing Cross-23 API calls that failed in the log...")
    
    # Load tool info
    with open("utils/tool_info.json", 'r') as f:
        tool_info = json.load(f)
    
    tool_info = tool_info['booking-com15']
    api_call = RapidAPICall(tool="booking-com15", tool_info=tool_info)
    
    # Test cases from Cross-23.log
    test_cases = [
        {
            "name": "Model Query (with USA)",
            "func_call": {
                "name": "Search_Hotel_Destination",
                "arguments": {
                    "query": "Statue of Liberty, New York, USA"
                }
            }
        },
        {
            "name": "Golden Query (without USA)",
            "func_call": {
                "name": "Search_Hotel_Destination", 
                "arguments": {
                    "query": "Statue of Liberty, New York"
                }
            }
        }
    ]
    
    results = {}
    
    for i, test_case in enumerate(test_cases):
        print(f"\n{'='*60}")
        print(f"Test {i+1}: {test_case['name']}")
        print(f"Function Call: {test_case['func_call']}")
        print("-" * 60)
        
        try:
            response = api_call._call(test_case['func_call'])
            
            if response is not None:
                print("✅ API call successful!")
                print(f"Response: {json.dumps(response, indent=2)}")
                results[test_case['name']] = response
            else:
                print("❌ API call returned None")
                results[test_case['name']] = None
                
        except Exception as e:
            print(f"❌ Exception during API call: {e}")
            results[test_case['name']] = None
    
    # Compare responses
    print(f"\n{'='*60}")
    print("COMPARISON ANALYSIS")
    print(f"{'='*60}")
    
    hotel_model = results.get("Model Query (with USA)")
    hotel_golden = results.get("Golden Query (without USA)")
    
    print(f"\n🏨 Hotel Destination Search:")
    print(f"Model (USA) == Golden: {hotel_model == hotel_golden}")
    if hotel_model != hotel_golden:
        print(f"Model result: {hotel_model}")
        print(f"Golden result: {hotel_golden}")
    
    return results

if __name__ == "__main__":
    test_cross23_api_calls()