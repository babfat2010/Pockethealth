from flask import Blueprint, request, jsonify, send_file
from services.dicom_service import (
    save_dicom_file, 
    extract_metadata, 
    convert_to_png, 
    list_tags,
    get_dicom_files,
    get_dicom_info,
    delete_dicom_file
)
import uuid

dicom_bp = Blueprint('dicom', __name__)

@dicom_bp.route('/dicom', methods=['POST'])
def create_dicom():
    """Upload a new DICOM file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.lower().endswith(('.dcm', '.dicom')):
        return jsonify({'error': 'File must be a DICOM file (.dcm or .dicom)'}), 400

    file_id = str(uuid.uuid4())
    try:
        save_dicom_file(file, file_id)
        return jsonify({
            'id': file_id,
            'filename': file.filename,
            'message': 'DICOM file uploaded successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': f'Failed to save file: {str(e)}'}), 500

@dicom_bp.route('/dicom', methods=['GET'])
def list_dicoms():
    """List all DICOM files"""
    try:
        files = get_dicom_files()
        return jsonify({
            'count': len(files),
            'files': files
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dicom_bp.route('/dicom/<file_id>', methods=['GET'])
def get_dicom(file_id):
    """Get basic information about a specific DICOM file"""
    try:
        info = get_dicom_info(file_id)
        return jsonify(info), 200
    except FileNotFoundError:
        return jsonify({'error': 'DICOM file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dicom_bp.route('/dicom/<file_id>/attributes', methods=['GET'])
def get_dicom_attributes(file_id):
    """Get DICOM attributes/tags, optionally filtered by specific tag"""
    tag = request.args.get('tag')
    
    try:
        if tag:
            # Get specific attribute by tag
            value = extract_metadata(file_id, tag)
            return jsonify({
                'tag': tag,
                'value': value
            }), 200
        else:
            # Get all attributes
            attributes = list_tags(file_id)
            return jsonify({
                'count': len(attributes),
                'attributes': attributes
            }), 200
    except FileNotFoundError:
        return jsonify({'error': 'DICOM file not found'}), 404
    except ValueError as e:
        return jsonify({'error': f'Invalid tag format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dicom_bp.route('/dicom/<file_id>/png', methods=['GET'])
def get_dicom_png(file_id):
    """Get PNG conversion of the DICOM file"""
    try:
        png_path = convert_to_png(file_id)
        return send_file(png_path, mimetype='image/png')
    except FileNotFoundError:
        return jsonify({'error': 'DICOM file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dicom_bp.route('/dicom/<file_id>', methods=['DELETE'])
def delete_dicom(file_id):
    """Delete a DICOM file"""
    try:
        delete_dicom_file(file_id)
        return jsonify({'message': 'DICOM file deleted successfully'}), 200
    except FileNotFoundError:
        return jsonify({'error': 'DICOM file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500 