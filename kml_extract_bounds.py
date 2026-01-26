#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
KML File Boundary Extraction Tool
Function: Extract boundary information from KML files (maximum/minimum latitude and longitude)
Usage: python kml_extract_bounds.py <input.kml> or ./kml_extract_bounds.py <input.kml>
"""

import sys
import os
import re
import xml.etree.ElementTree as ET
from typing import Tuple, Optional, List

# KML namespace
KML_NS = {
    'kml': 'http://www.opengis.net/kml/2.2',
    'gx': 'http://www.google.com/kml/ext/2.2'
}

def parse_coordinates(coords_text: str) -> List[Tuple[float, float]]:
    """Parse coordinates text, return list of (longitude, latitude)"""
    coordinates = []
    # Clean text, split coordinate points
    coords_text = coords_text.strip()
    
    # Split coordinate points (separated by spaces or newlines)
    points = re.split(r'[\s\n]+', coords_text)
    
    for point in points:
        point = point.strip()
        if not point:
            continue
            
        # Split coordinate values (KML format: longitude,latitude[,altitude])
        parts = point.split(',')
        if len(parts) >= 2:
            try:
                lon = float(parts[0].strip())
                lat = float(parts[1].strip())
                coordinates.append((lon, lat))
            except ValueError:
                continue
    
    return coordinates

def extract_bounds_from_kml(kml_file: str) -> Optional[Tuple[float, float, float, float]]:
    """
    Extract boundary information from KML file
    Return: (min_lon, min_lat, max_lon, max_lat)
    """
    try:
        tree = ET.parse(kml_file)
        root = tree.getroot()
        
        # Register namespace
        for prefix, uri in KML_NS.items():
            ET.register_namespace(prefix, uri)
        
        # Find all coordinates elements (consider namespace)
        coordinates_elements = []
        
        # Method 1: Use findall with namespace
        coordinates_elements = root.findall('.//{http://www.opengis.net/kml/2.2}coordinates')
        
        # Method 2: If method 1 fails, try other ways
        if not coordinates_elements:
            coordinates_elements = root.findall('.//coordinates')
        
        # Method 3: Use iter to find all coordinates tags (ignore namespace)
        if not coordinates_elements:
            for elem in root.iter():
                if 'coordinates' in elem.tag:
                    coordinates_elements.append(elem)
        
        if not coordinates_elements:
            print(f"Warning: No coordinates elements found in file {kml_file}")
            return None
        
        # Initialize boundary values
        min_lon, min_lat = float('inf'), float('inf')
        max_lon, max_lat = float('-inf'), float('-inf')
        coordinate_count = 0
        
        # Process all coordinates elements
        for coords_elem in coordinates_elements:
            if coords_elem.text:
                coords_list = parse_coordinates(coords_elem.text)
                coordinate_count += len(coords_list)
                
                for lon, lat in coords_list:
                    min_lon = min(min_lon, lon)
                    min_lat = min(min_lat, lat)
                    max_lon = max(max_lon, lon)
                    max_lat = max(max_lat, lat)
        
        if coordinate_count == 0:
            print(f"Warning: No valid coordinate points found")
            return None
        
        return (min_lon, min_lat, max_lon, max_lat)
        
    except ET.ParseError as e:
        print(f"Error: Unable to parse KML file - {e}")
        return None
    except Exception as e:
        print(f"Error: Error processing file - {e}")
        return None

def extract_bounds_from_kml_simple(kml_file: str) -> Optional[Tuple[float, float, float, float]]:
    """
    Simplified version: Use regular expressions to extract coordinates directly (suitable for simple KML files)
    """
    try:
        with open(kml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all coordinates tag content
        pattern = r'<coordinates[^>]*>([^<]+)</coordinates>'
        matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
        
        if not matches:
            # Try another format (might have CDATA)
            pattern = r'<coordinates[^>]*><!\[CDATA\[([^\]]+)\]\]></coordinates>'
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
        
        if not matches:
            print(f"Warning: No coordinates tags found")
            return None
        
        # Initialize boundary values
        min_lon, min_lat = float('inf'), float('inf')
        max_lon, max_lat = float('-inf'), float('-inf')
        coordinate_count = 0
        
        # Process all matches
        for coords_text in matches:
            coords_list = parse_coordinates(coords_text)
            coordinate_count += len(coords_list)
            
            for lon, lat in coords_list:
                min_lon = min(min_lon, lon)
                min_lat = min(min_lat, lat)
                max_lon = max(max_lon, lon)
                max_lat = max(max_lat, lat)
        
        if coordinate_count == 0:
            print(f"Warning: No valid coordinate points found")
            return None
        
        return (min_lon, min_lat, max_lon, max_lat)
        
    except Exception as e:
        print(f"Error: Error processing file - {e}")
        return None

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("KML Boundary Extraction Tool")
        print("Usage: {} <KML file path>".format(sys.argv[0]))
        print("Example: {} sample.kml".format(sys.argv[0]))
        sys.exit(1)
    
    kml_file = sys.argv[1]
    
    if not os.path.exists(kml_file):
        print(f"Error: File '{kml_file}' does not exist")
        sys.exit(1)
    
    if not kml_file.lower().endswith('.kml'):
        print(f"Warning: File '{kml_file}' may not be a KML file")
    
    print(f"Processing file: {kml_file}")
    print("-" * 50)
    
    # Try XML parsing method first
    bounds = extract_bounds_from_kml(kml_file)
    
    # If XML parsing fails, try regular expression method
    if bounds is None:
        print("XML parsing failed, trying regular expression method...")
        bounds = extract_bounds_from_kml_simple(kml_file)
    
    if bounds:
        min_lon, min_lat, max_lon, max_lat = bounds
        
        print("Boundary extraction successful!")
        print("-" * 50)
        print(f"Minimum Latitude (South): {min_lat:.6f}")
        print(f"Maximum Latitude (North): {max_lat:.6f}")
        print(f"Minimum Longitude (West): {min_lon:.6f}")
        print(f"Maximum Longitude (East): {max_lon:.6f}")

        print("-" * 50)
        print(f"Bounding Box (S N W E): {min_lat:.6f} {max_lat:.6f} {min_lon:.6f} {max_lon:.6f}")
        
    else:
        print("Error: Unable to extract boundary information from KML file")
        sys.exit(1)

if __name__ == "__main__":
    main()



###-------------------------------------------------- test example --------------------------------------------------###
## ./kml_extract_bounds.py /mnt/c/Users/ADMIN/桌面/QLDburst.kml
##------------------------- output -------------------------##
# Processing file: /mnt/c/Users/ADMIN/桌面/QLDburst.kml
# --------------------------------------------------
# Boundary extraction successful!
# --------------------------------------------------
# Minimum Latitude (South): -27.566890
# Maximum Latitude (North): -26.684138
# Minimum Longitude (West): 150.700003
# Maximum Longitude (East): 151.777964
# --------------------------------------------------
# Bounding Box (S N W E): -27.566890 -26.684138 150.700003 151.777964
