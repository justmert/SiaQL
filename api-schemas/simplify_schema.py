import json
import argparse
from typing import Dict, Any, List
from copy import deepcopy

def extract_pattern(data: Any, max_array_items: int = 1) -> Any:
    """
    Recursively extract the structural pattern from data by keeping only one example
    of each unique structure.
    """
    if isinstance(data, (str, int, float, bool)) or data is None:
        return data
    
    if isinstance(data, list):
        if not data:
            return []
            
        # Group items by their structure
        patterns = {}
        for item in data:
            if isinstance(item, dict):
                key = tuple(sorted(item.keys()))
            elif isinstance(item, list):
                key = 'list'
            else:
                key = str(type(item))
            patterns[key] = item
            
        # Return one example of each pattern
        return [extract_pattern(item) for item in list(patterns.values())[:max_array_items]]
    
    if isinstance(data, dict):
        return {key: extract_pattern(value) for key, value in data.items()}
    
    return data

def parse_body(body_data: Any) -> Any:
    """Parse body data from various formats."""
    if not body_data:
        return None
        
    if isinstance(body_data, dict):
        if 'raw' in body_data:
            try:
                return json.loads(body_data['raw'])
            except json.JSONDecodeError:
                return body_data['raw']
        return body_data
        
    if isinstance(body_data, str):
        try:
            return json.loads(body_data)
        except json.JSONDecodeError:
            return body_data
            
    return body_data

def extract_responses(responses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract unique response patterns based on status code and body structure."""
    if not responses:
        return []
        
    # Group responses by status code
    responses_by_status = {}
    for resp in responses:
        status = resp.get('code', 200)
        if status not in responses_by_status:
            responses_by_status[status] = []
        responses_by_status[status].append(resp)
    
    # For each status code, extract unique body patterns
    unique_responses = []
    for status, resps in responses_by_status.items():
        body_patterns = {}
        for resp in resps:
            body = parse_body(resp.get('body'))
            if body:
                # Use the structure of the body as a key
                if isinstance(body, dict):
                    pattern_key = tuple(sorted(body.keys()))
                elif isinstance(body, list):
                    pattern_key = 'list'
                else:
                    pattern_key = str(type(body))
                    
                if pattern_key not in body_patterns:
                    body_patterns[pattern_key] = {
                        'name': resp.get('name', ''),
                        'status': status,
                        'body': extract_pattern(body)
                    }
        
        unique_responses.extend(body_patterns.values())
    
    return unique_responses

def simplify_request(item: Dict[str, Any]) -> Dict[str, Any]:
    """Simplify a request item to include essential API details."""
    request = item.get('request', {})
    
    simplified = {
        'name': item.get('name', ''),
        'method': request.get('method', 'GET'),
        'url': request.get('url', {}).get('raw', ''),
        'description': request.get('description', '')
    }
    
    # Handle request body if it exists
    if 'body' in request:
        body = parse_body(request['body'])
        if body:
            simplified['requestBody'] = body
    
    # Handle multiple responses
    if 'response' in item:
        responses = extract_responses(item['response'])
        if responses:
            simplified['responses'] = responses
        
        # Add variables if they exist
        if 'variable' in request:
            simplified['variable'] = request['variable']
    
    return simplified

def process_collection(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Process all items in the collection recursively."""
    result = []
    
    # Group similar endpoints
    patterns = {}
    for item in items:
        if 'item' in item:
            # This is a folder
            processed_items = process_collection(item['item'])
            if processed_items:
                result.append({
                    'name': item['name'],
                    'item': processed_items
                })
        else:
            # This is an endpoint
            simplified = simplify_request(item)
            # Create pattern key based on method and url structure
            pattern_key = f"{simplified.get('method')}_{simplified.get('url', '')}"
            patterns[pattern_key] = simplified
    
    # Add all unique endpoints
    result.extend(patterns.values())
    return result

def main():
    parser = argparse.ArgumentParser(description='Extract API patterns from Postman collection')
    parser.add_argument('input_file', help='Path to input Postman collection JSON file')
    parser.add_argument('--output', '-o', help='Output file path (default: pattern_collection.json)')
    
    args = parser.parse_args()
    output_file = args.output or 'pattern_collection.json'
    
    try:
        # Read input file
        with open(args.input_file, 'r', encoding='utf-8') as f:
            collection = json.load(f)
        
        if 'item' not in collection:
            raise ValueError("Invalid Postman collection format: 'item' key not found")
        
        # Process the collection
        simplified = {
            'item': process_collection(collection['item'])
        }
        
        # Write output file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(simplified, f, indent=2)
        
        print(f"Successfully created pattern collection at: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in input file '{args.input_file}'")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()