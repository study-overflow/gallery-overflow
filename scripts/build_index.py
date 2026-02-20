#!/usr/bin/env python3
"""
Script to generate index.json for image gallery from meta.json
"""
import json
import os
from datetime import datetime
import hashlib

def generate_image_id(file_path):
    """Generate a unique ID for an image based on file path and timestamp"""
    # Create a hash of the file path to ensure uniqueness
    file_hash = hashlib.md5(file_path.encode()).hexdigest()
    return f"img_{file_hash[:8]}_{int(datetime.now().timestamp())}"

def get_file_modification_time(file_path):
    """Get the modification time of a file"""
    if os.path.exists(file_path):
        mod_timestamp = os.path.getmtime(file_path)
        return datetime.fromtimestamp(mod_timestamp).strftime('%Y-%m-%d')
    else:
        return datetime.now().strftime('%Y-%m-%d')

def generate_index():
    # Load metadata from meta.json
    with open('meta.json', 'r', encoding='utf-8') as f:
        metadata_list = json.load(f)

    # Generate index data
    index_data = []
    for meta in metadata_list:
        file_path = meta['file']

        # Generate unique ID for the image
        img_id = generate_image_id(file_path)

        # Get file modification time
        mod_date = get_file_modification_time(file_path)
        date = meta.get('date', mod_date)  # Use provided date if available, otherwise use file mod time

        # Build CDN URL
        cdn_url = f"https://cdn.jsdelivr.net/gh/study-overflow/gallery-overflow@main/{file_path}"

        # Create index entry
        index_entry = {
            "id": img_id,
            "title": meta.get('title', ''),
            "body": meta.get('body', ''),
            "tags": meta.get('tags', []),
            "date": date,
            "file": file_path,
            "cdn_url": cdn_url
        }

        index_data.append(index_entry)

    # Write index.json
    with open('index.json', 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)

    print(f"Generated index.json with {len(index_data)} images")

if __name__ == "__main__":
    generate_index()