from flask import Flask, render_template, request, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename
from docx import Document
from fpdf import FPDF
from PyPDF2 import PdfWriter  
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_docx_to_pdf(docx_path, password="securepassword"):
    try:
        doc = Document(docx_path)
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for para in doc.paragraphs:
            pdf.multi_cell(0, 10, para.text)
        
        unprotected_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_unprotected.pdf')
        pdf.output(unprotected_pdf_path)

        protected_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.pdf')
        pdf_writer = PdfWriter()
        with open(unprotected_pdf_path, "rb") as input_pdf:
            pdf_writer.append(input_pdf)
            pdf_writer.encrypt(password)  

            with open(protected_pdf_path, "wb") as output_pdf:
                pdf_writer.write(output_pdf)

        os.remove(unprotected_pdf_path)

        return protected_pdf_path
    except Exception as e:
        print(f"Error during conversion: {e}")
        raise RuntimeError("An error occurred while converting the DOCX file to PDF.")

@app.route('/')
def index():
    return render_template('index.html', download_url=None, file_metadata=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify(error="No file part"), 400

        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify(error="No selected file or invalid file format"), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        file_size = os.path.getsize(filepath)  
        upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
        
        password = request.form.get('password', 'securepassword')  # Default password if none provided

        pdf_file = convert_docx_to_pdf(filepath, password)

        file_metadata = {
            'filename': filename,
            'size': file_size,
            'upload_time': upload_time
        }

        return render_template('index.html', download_url=f'/download/{os.path.basename(pdf_file)}', file_metadata=file_metadata)

    except Exception as e:
        print(f"Error during file upload or conversion: {e}")
        return jsonify(error="An error occurred while processing the file."), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return jsonify(error="File not found"), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
