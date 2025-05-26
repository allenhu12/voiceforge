#!/usr/bin/env python3
"""
Get All Voice IDs from Fish Audio

This script fetches all available voice IDs from Fish Audio API.
Usage: python get_all_voice_ids.py [--limit N] [--save-to-file]
"""

import argparse
import json
import sys
from pathlib import Path

import httpx

def get_voice_ids(api_key: str, limit: int = None, save_to_file: bool = False):
    """Fetch voice IDs from Fish Audio API."""
    
    base_url = "https://api.fish.audio"
    endpoint = "/model"
    
    all_voice_ids = []
    page_number = 1
    page_size = 100  # Maximum allowed by Fish Audio
    
    print(f"🔄 Fetching voice IDs from Fish Audio...")
    
    with httpx.Client() as client:
        while True:
            params = {
                "page_size": page_size,
                "page_number": page_number
            }
            
            try:
                response = client.get(
                    f"{base_url}{endpoint}",
                    params=params,
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    print(f"❌ API Error: {response.status_code}")
                    return []
                
                data = response.json()
                items = data.get("items", [])
                total = data.get("total", 0)
                
                # Extract voice IDs from TTS models
                page_voice_ids = []
                for item in items:
                    if item.get("type") == "tts":
                        voice_id = item.get("_id")
                        title = item.get("title", "Unknown")
                        author = item.get("author", {}).get("nickname", "Unknown")
                        languages = ", ".join(item.get("languages", []))
                        
                        page_voice_ids.append({
                            "id": voice_id,
                            "title": title,
                            "author": author,
                            "languages": languages
                        })
                
                all_voice_ids.extend(page_voice_ids)
                
                print(f"📄 Page {page_number}: Found {len(page_voice_ids)} voices (Total so far: {len(all_voice_ids)})")
                
                # Check if we've reached the limit or end of results
                if limit and len(all_voice_ids) >= limit:
                    all_voice_ids = all_voice_ids[:limit]
                    break
                
                if len(items) < page_size:  # Last page
                    break
                
                page_number += 1
                
            except Exception as e:
                print(f"❌ Error fetching page {page_number}: {e}")
                break
    
    print(f"\n✅ Total voices found: {len(all_voice_ids)}")
    
    # Save to file if requested
    if save_to_file:
        output_file = Path("fish_audio_voice_ids.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_voice_ids, f, indent=2, ensure_ascii=False)
        print(f"💾 Voice data saved to: {output_file}")
        
        # Also save just the IDs
        ids_file = Path("fish_audio_voice_ids.txt")
        with open(ids_file, 'w') as f:
            for voice in all_voice_ids:
                f.write(f"{voice['id']}\n")
        print(f"📝 Voice IDs saved to: {ids_file}")
    
    return all_voice_ids

def main():
    parser = argparse.ArgumentParser(description="Get all voice IDs from Fish Audio")
    parser.add_argument("--api-key", help="Fish Audio API key (or set FISH_API_KEY env var)")
    parser.add_argument("--limit", type=int, help="Limit number of voices to fetch")
    parser.add_argument("--save-to-file", action="store_true", help="Save results to files")
    parser.add_argument("--ids-only", action="store_true", help="Print only voice IDs")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key
    if not api_key:
        import os
        api_key = os.getenv("FISH_API_KEY")
    
    if not api_key:
        print("❌ No API key provided. Use --api-key or set FISH_API_KEY environment variable.")
        sys.exit(1)
    
    # Fetch voice IDs
    voices = get_voice_ids(api_key, limit=args.limit, save_to_file=args.save_to_file)
    
    if not voices:
        print("❌ No voices found.")
        sys.exit(1)
    
    # Display results
    if args.ids_only:
        print("\n📋 Voice IDs:")
        for voice in voices:
            print(voice["id"])
    else:
        print("\n📋 Voice Details:")
        for voice in voices:
            print(f"ID: {voice['id']}")
            print(f"Title: {voice['title']}")
            print(f"Author: {voice['author']}")
            print(f"Languages: {voice['languages']}")
            print("-" * 50)

if __name__ == "__main__":
    main() 