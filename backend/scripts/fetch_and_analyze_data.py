"""
Script to fetch and analyze data from orar.usv.ro
"""
import sys
import os
from pathlib import Path
import asyncio
import aiohttp
import json

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# URLs for external data
PROFESSORS_URL = "https://orar.usv.ro/orar/vizualizare/data/cadre.php?json"
ROOMS_URL = "https://orar.usv.ro/orar/vizualizare/data/sali.php?json"
FACULTIES_URL = "https://orar.usv.ro/orar/vizualizare/data/facultati.php?json"
SUBGROUPS_URL = "https://orar.usv.ro/orar/vizualizare/data/subgrupe.php?json"

async def fetch_json_data(url):
    """
    Fetch JSON data from a given URL
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Failed to fetch data from {url}. Status: {response.status}")
                    return []
    except Exception as e:
        print(f"Error fetching data from {url}: {str(e)}")
        return []

async def analyze_data():
    """
    Fetch and analyze data from orar.usv.ro
    """
    print("Fetching data from orar.usv.ro...")
    
    # Fetch data
    professors_data = await fetch_json_data(PROFESSORS_URL)
    rooms_data = await fetch_json_data(ROOMS_URL)
    faculties_data = await fetch_json_data(FACULTIES_URL)
    subgroups_data = await fetch_json_data(SUBGROUPS_URL)
    
    # Analyze professors data
    print(f"\nFetched {len(professors_data)} professors")
    if professors_data:
        print("Sample professor data:")
        sample = professors_data[0]
        print(json.dumps(sample, indent=2))
        print("\nProfessor fields:")
        for key in sample.keys():
            print(f"  {key}")
    
    # Analyze rooms data
    print(f"\nFetched {len(rooms_data)} rooms")
    if rooms_data:
        print("Sample room data:")
        sample = rooms_data[0]
        print(json.dumps(sample, indent=2))
        print("\nRoom fields:")
        for key in sample.keys():
            print(f"  {key}")
    
    # Analyze faculties data
    print(f"\nFetched {len(faculties_data)} faculties")
    if faculties_data:
        print("Sample faculty data:")
        sample = faculties_data[0]
        print(json.dumps(sample, indent=2))
        print("\nFaculty fields:")
        for key in sample.keys():
            print(f"  {key}")
    
    # Analyze subgroups data
    print(f"\nFetched {len(subgroups_data)} subgroups")
    if subgroups_data:
        print("Sample subgroup data:")
        sample = subgroups_data[0]
        print(json.dumps(sample, indent=2))
        print("\nSubgroup fields:")
        for key in sample.keys():
            print(f"  {key}")

if __name__ == "__main__":
    asyncio.run(analyze_data())
