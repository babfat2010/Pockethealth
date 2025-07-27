import os
import pydicom
import numpy as np
from PIL import Image
from datetime import datetime

STORAGE_DIR = 'storage'

def save_dicom_file(file, file_id):
    """Save uploaded DICOM file to storage"""
    filepath = os.path.join(STORAGE_DIR, f"{file_id}.dcm")
    file.save(filepath)
    
    # Validate that it's actually a DICOM file
    try:
        pydicom.dcmread(filepath)
    except Exception as e:
        # Clean up invalid file
        if os.path.exists(filepath):
            os.remove(filepath)
        raise ValueError(f"Invalid DICOM file: {str(e)}")

def extract_metadata(file_id, tag):
    """Extract specific metadata from DICOM file by tag"""
    filepath = os.path.join(STORAGE_DIR, f"{file_id}.dcm")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"DICOM file with ID {file_id} not found")
    
    try:
        ds = pydicom.dcmread(filepath)
        
        # Parse tag format (e.g., "0010,0010" or "0010,0010")
        if ',' not in tag:
            raise ValueError("Tag must be in format 'XXXX,XXXX' (e.g., '0010,0010')")
            
        group, element = tag.split(',')
        tag_tuple = (int(group, 16), int(element, 16))

        if tag_tuple in ds:
            return str(ds[tag_tuple].value)
        return "Tag not found"
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError("Tag must contain valid hexadecimal values")
        raise e
    except Exception as e:
        raise Exception(f"Error reading DICOM file: {str(e)}")

def convert_to_png(file_id):
    """Convert DICOM file to PNG format"""
    dicom_path = os.path.join(STORAGE_DIR, f"{file_id}.dcm")
    output_path = os.path.join(STORAGE_DIR, f"{file_id}.png")

    if not os.path.exists(dicom_path):
        raise FileNotFoundError(f"DICOM file with ID {file_id} not found")

    try:
        ds = pydicom.dcmread(dicom_path)
        
        # Check if pixel data exists
        if not hasattr(ds, 'pixel_array'):
            raise ValueError("DICOM file does not contain pixel data")
            
        arr = ds.pixel_array

        # Normalize pixel values to 0-255 range
        arr = (arr - np.min(arr)) / (np.max(arr) - np.min(arr)) * 255
        arr = arr.astype(np.uint8)

        image = Image.fromarray(arr)
        image.save(output_path)
        return output_path
    except Exception as e:
        raise Exception(f"Error converting DICOM to PNG: {str(e)}")

def list_tags(file_id):
    """List all tags and their names for a DICOM file"""
    filepath = os.path.join(STORAGE_DIR, f"{file_id}.dcm")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"DICOM file with ID {file_id} not found")
    
    try:
        ds = pydicom.dcmread(filepath)
        tag_dict = {}

        for elem in ds.iterall():
            tag_str = f"{elem.tag.group:04X},{elem.tag.element:04X}"
            tag_dict[tag_str] = {
                'name': str(elem.name),
                'value': str(elem.value) if hasattr(elem, 'value') else 'N/A'
            }

        return tag_dict
    except Exception as e:
        raise Exception(f"Error reading DICOM tags: {str(e)}")

def get_dicom_files():
    """Get list of all DICOM files with basic information"""
    if not os.path.exists(STORAGE_DIR):
        return []
    
    files = []
    for filename in os.listdir(STORAGE_DIR):
        if filename.endswith('.dcm'):
            file_id = filename[:-4]  # Remove .dcm extension
            try:
                info = get_dicom_info(file_id)
                files.append(info)
            except Exception:
                # Skip corrupted files
                continue
    
    return files

def get_dicom_info(file_id):
    """Get basic information about a specific DICOM file"""
    filepath = os.path.join(STORAGE_DIR, f"{file_id}.dcm")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"DICOM file with ID {file_id} not found")
    
    try:
        ds = pydicom.dcmread(filepath)
        
        # Get file stats
        file_stats = os.stat(filepath)
        
        info = {
            'id': file_id,
            'filename': f"{file_id}.dcm",
            'size_bytes': file_stats.st_size,
            'created_at': datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
            'modified_at': datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
            'dicom_info': {}
        }
        
        # Extract common DICOM metadata
        common_tags = {
            'PatientName': (0x0010, 0x0010),
            'PatientID': (0x0010, 0x0020),
            'StudyDate': (0x0008, 0x0020),
            'StudyDescription': (0x0008, 0x1030),
            'Modality': (0x0008, 0x0060),
            'SOPInstanceUID': (0x0008, 0x0018),
        }
        
        for name, tag in common_tags.items():
            if tag in ds:
                info['dicom_info'][name] = str(ds[tag].value)
            else:
                info['dicom_info'][name] = None
                
        # Add image dimensions if available
        if hasattr(ds, 'pixel_array'):
            info['dicom_info']['ImageDimensions'] = {
                'rows': int(ds.Rows) if hasattr(ds, 'Rows') else None,
                'columns': int(ds.Columns) if hasattr(ds, 'Columns') else None,
            }
        
        return info
    except Exception as e:
        raise Exception(f"Error reading DICOM file info: {str(e)}")

def delete_dicom_file(file_id):
    """Delete a DICOM file and its associated PNG if it exists"""
    dicom_path = os.path.join(STORAGE_DIR, f"{file_id}.dcm")
    png_path = os.path.join(STORAGE_DIR, f"{file_id}.png")
    
    if not os.path.exists(dicom_path):
        raise FileNotFoundError(f"DICOM file with ID {file_id} not found")
    
    try:
        # Remove DICOM file
        os.remove(dicom_path)
        
        # Remove PNG file if it exists
        if os.path.exists(png_path):
            os.remove(png_path)
            
    except Exception as e:
        raise Exception(f"Error deleting DICOM file: {str(e)}")
