# Dicom API

This repo contains the solution to the take-home coding challenge
The solution was implemented using python 
Please note that dicom library doesn't support version of python higher than 3.13.x. 

This API is a RESTful API that allows you to upload, list, get, and delete dicom files.

# Installation

1. Install the requirements
```bash
pip install -r requirements.txt
```

2. Run the app
```bash
python app.py
```

# How to test

You can test at least the get requests. in a browser:

To see a list of all the dicom files visit:
```bash
http://localhost:5000/dicom
```

To see a list of all the attributes of a specific dicom file (e.g. 5efb7e40-5880-4a82-88c3-b52644c4f703) visit:
```bash
http://127.0.0.1:5000/dicom/5efb7e40-5880-4a82-88c3-b52644c4f703/attributes
```

To see the png image of a specific dicom file visit:
```bash
http://127.0.0.1:5000/dicom/5efb7e40-5880-4a82-88c3-b52644c4f703/png
```

You can also test all endpoints using curl:

### 1. Upload DICOM File
**POST /dicom**
- **Purpose**: Upload and store a new DICOM file
- **Request**: `multipart/form-data` with file field
- **Response**: JSON with file ID and confirmation
- **Status Codes**: 201 (Created), 400 (Bad Request), 500 (Server Error)

**Example Request:**
```bash
curl -X POST -F "file=@sample.dcm" http://localhost:5000/dicom
```

**Example Response:**
```json
{
  "id": "5efb7e40-5880-4a82-88c3-b52644c4f703",
  "filename": "sample.dcm", 
  "message": "DICOM file uploaded successfully"
}
```

### 2. List All DICOM Files
**GET /dicom**
- **Purpose**: Retrieve a list of all stored DICOM files with metadata
- **Response**: JSON array with file information
- **Status Codes**: 200 (OK), 500 (Server Error)

**Example Request:**
```bash
curl -X GET http://localhost:5000/dicom
```

**Example Response:**
```json
{
  "count": 2,
  "files": [
    {
      "id": "5efb7e40-5880-4a82-88c3-b52644c4f703",
      "filename": "sample.dcm",
      "size_bytes": 280620,
      "created_at": "2025-01-26T15:06:35.474368",
      "modified_at": "2025-01-26T15:06:35.474368",
      "dicom_info": {
        "PatientName": "DOE^JOHN",
        "PatientID": "12345",
        "StudyDate": "20231215",
        "StudyDescription": "MRI BRAIN",
        "Modality": "MR",
        "ImageDimensions": {
          "rows": 512,
          "columns": 512
        }
      }
    }
  ]
}
```

### 3. Get Specific DICOM File Information
**GET /dicom/{id}**
- **Purpose**: Retrieve detailed information about a specific DICOM file
- **Response**: JSON with comprehensive file metadata
- **Status Codes**: 200 (OK), 404 (Not Found), 500 (Server Error)

**Example Request:**
```bash
curl -X GET http://localhost:5000/dicom/5efb7e40-5880-4a82-88c3-b52644c4f703
```

### 4. Get DICOM Attributes/Tags
**GET /dicom/{id}/attributes**
- **Purpose**: Retrieve DICOM header attributes
- **Query Parameters**: 
  - `tag` (optional): Specific DICOM tag in format "XXXX,XXXX" (e.g., "0010,0010")
- **Response**: JSON with attributes data
- **Status Codes**: 200 (OK), 400 (Bad Request), 404 (Not Found), 500 (Server Error)

**Get All Attributes:**
```bash
curl -X GET http://localhost:5000/dicom/5efb7e40-5880-4a82-88c3-b52644c4f703/attributes
```

**Get Specific Attribute:**
```bash
curl -X GET "http://localhost:5000/dicom/5efb7e40-5880-4a82-88c3-b52644c4f703/attributes?tag=0010,0010"
```

**Example Response (specific tag):**
```json
{
  "tag": "0010,0010",
  "value": "DOE^JOHN"
}
```

**Example Response (all attributes):**
```json
{
  "count": 125,
  "attributes": {
    "0010,0010": {
      "name": "Patient's Name",
      "value": "DOE^JOHN"
    },
    "0010,0020": {
      "name": "Patient ID",
      "value": "12345"
    }
  }
}
```

### 5. Get PNG Conversion
**GET /dicom/{id}/png**
- **Purpose**: Retrieve PNG conversion of the DICOM file for browser viewing
- **Response**: Binary PNG image data
- **Status Codes**: 200 (OK), 404 (Not Found), 500 (Server Error)

**Example Request:**
```bash
curl -X GET http://localhost:5000/dicom/5efb7e40-5880-4a82-88c3-b52644c4f703/png --output image.png
```

### 6. Delete DICOM File
**DELETE /dicom/{id}**
- **Purpose**: Delete a DICOM file and its associated PNG conversion
- **Response**: JSON confirmation message
- **Status Codes**: 200 (OK), 404 (Not Found), 500 (Server Error)

**Example Request:**
```bash
curl -X DELETE http://localhost:5000/dicom/5efb7e40-5880-4a82-88c3-b52644c4f703
```

**Example Response:**
```json
{
  "message": "DICOM file deleted successfully"
}
```
