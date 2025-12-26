from flask import Flask
from routes.dicom import dicom_bp
import os

app = Flask(__name__)
os.makedirs('storage', exist_ok=True)

# Register the RESTful DICOM API blueprint
app.register_blueprint(dicom_bp)

if __name__ == '__main__':
    app.run(debug=True)
#This app is good