from flask import Flask, request, redirect, url_for, send_file, render_template, flash
import os
from werkzeug.utils import secure_filename
import subprocess
import logging

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'xls', 'xlsx'}
app.secret_key = 'supersecretkey'

logging.basicConfig(level=logging.INFO)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'file1' not in request.files or 'file2' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file1 = request.files['file1']
    file2 = request.files['file2']
    if file1.filename == '' or file2.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        file1_path = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        file2_path = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
        file1.save(file1_path)
        file2.save(file2_path)
        output_file = os.path.join(app.config['UPLOAD_FOLDER'], 'combined_output.xlsx')
        try:
            subprocess.run(['python3', 'main.py', file1_path, file2_path, output_file], check=True)
            return send_file(output_file, as_attachment=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error combining files: {e}")
            flash('Error combining files')
            return redirect(request.url)
    else:
        flash('Invalid file type')
        return redirect(request.url)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=5000, debug=False)