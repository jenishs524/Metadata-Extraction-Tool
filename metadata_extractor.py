#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from datetime import datetime

def extract_metadata(filepath):
    """Use exiftool to extract metadata in JSON format."""
    if not os.path.exists(filepath):
        print(f"[!] File not found: {filepath}")
        return None
    
    try:
        # Run exiftool and get JSON output
        result = subprocess.run(
            ['exiftool', '-j', filepath],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data[0]  # exiftool returns a list with one dict per file
        else:
            print(f"[!] exiftool error: {result.stderr}")
            return None
    except Exception as e:
        print(f"[!] Error: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 metadata_extractor.py <file_path>")
        print("Example: python3 metadata_extractor.py image.jpg")
        sys.exit(1)
    
    filepath = sys.argv[1]
    print(f"[*] Extracting metadata from: {filepath}")
    print("-" * 50)
    
    metadata = extract_metadata(filepath)
    if metadata:
        # Pretty print the metadata
        print(json.dumps(metadata, indent=2, default=str))
        
        # Save to a file
        output_file = f"metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
        print(f"\n[*] Metadata saved to: {output_file}")
        
        # Highlight interesting fields
        interesting = ['GPS', 'Latitude', 'Longitude', 'CreateDate', 'ModifyDate',
                       'Artist', 'Copyright', 'CameraModel', 'Make', 'Software']
        print("\n[+] Interesting findings:")
        for key in interesting:
            if key in metadata and metadata[key]:
                print(f"    {key}: {metadata[key]}")
    else:
        print("[!] No metadata extracted.")

if __name__ == "__main__":
    main()
