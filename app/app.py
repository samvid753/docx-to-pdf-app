from flask import Flask, render_template, request, send_from_directory
import os
from werkzeug.utils import secure_filename
from docx import Document
from fpdf import FPDF
from PyPDF2 import PdfWriter  # Add this for password protection
from datetime import datetime

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Check if file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Convert DOCX to PDF with password protection
def convert_docx_to_pdf(docx_path, password="securepassword"):
    # Read the DOCX file
    doc = Document(docx_path)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Extract text from DOCX and add to PDF
    for para in doc.paragraphs:
        pdf.multi_cell(0, 10, para.text)
    
    # Save to a temporary unprotected PDF file
    unprotected_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_unprotected.pdf')
    pdf.output(unprotected_pdf_path)

    # Add password protection
    protected_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.pdf')
    pdf_writer = PdfWriter()
    with open(unprotected_pdf_path, "rb") as input_pdf:
        pdf_writer.append(input_pdf)
        pdf_writer.encrypt(password)  # Set the password here

        with open(protected_pdf_path, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

    # Clean up the unprotected file
    os.remove(unprotected_pdf_path)

    return protected_pdf_path

@app.route('/')
def index():
    return render_template('index.html', download_url=None, file_metadata=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return 'No selected file or invalid file format', 400

    # Save the file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Get metadata of the uploaded file
    file_size = os.path.getsize(filepath)  # Size in bytes
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
    
    # Get password from user input (optional)
    password = request.form.get('password', 'securepassword')  # Default password if none provided

    # Convert to PDF with password protection
    pdf_file = convert_docx_to_pdf(filepath, password)

    # Prepare file metadata
    file_metadata = {
        'filename': filename,
        'size': file_size,
        'upload_time': upload_time
    }

    return render_template('index.html', download_url=f'/download/{os.path.basename(pdf_file)}', file_metadata=file_metadata)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
