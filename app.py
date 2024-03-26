from flask import Flask, request as req , send_file
from markupsafe import escape
from werkzeug.utils import secure_filename
import os
import subprocess


def compress_pdf(input_path, output_path, quality='ebook'):
    """
    Compresses a PDF file using Ghostscript.

    Parameters:
        input_path (str): Path to the input PDF file.
        output_path (str): Path to save the compressed PDF file.
        quality (str): Quality level for compression.
                      Possible values: 'screen', 'ebook', 'printer', 'prepress'.
    """
    args = [
        "gs",
        "-sDEVICE=pdfwrite",
        f"-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/" + quality,
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]

    subprocess.run(args)
    return "file compressed successfully"

app = Flask(__name__)


@app.route('/')
def hello_world():
    # print("hello")
    return 'Hello World!'


@app.route("/user/<username>", methods=['POST'])
def show_username(username):
    if req.method == "POST":
        return f'user {escape(username)}'
    else:
        return "not proper method"


@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in req.files:
        return "No files uploaded", 400
    file = req.files["file"]
    if file.filename == '':
        return "No file selected", 400

    file.save("uploads/" + file.filename)
    return "File saved successfully!"


@app.route("/compresspdf", methods=['POST'])
def upload_file():
    if 'file' not in req.files:
        return "No files uploaded", 400
    file = req.files['file']
    if file.filename == '':
        return "No file selected", 400
    input_file_path = os.path.join("uploads",secure_filename(file.filename))
    output_file_path = os.path.join("uploads","compressed_"+secure_filename(file.filename))
    file.save(input_file_path)

    quality = req.form.get('quality', 'screen')
    print("quality is ", quality)
    message = compress_pdf(input_file_path , output_file_path, quality)
    return message

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_file(os.path.join("uploads", filename), as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404



if __name__ == '__main__':
    app.run()
